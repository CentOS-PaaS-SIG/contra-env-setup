"""
contra-env-setup continuous integration test
"""
import os

from avocado import main
from avocado import Test
from avocado.utils import vmimage
from avocado.utils import git
from avocado.utils import process
from avocado.utils import wait
from utils import ip_available
from utils import create_cloudinit_cdrom
from utils import ssh_available
from utils import get_command


_VIRTINST_BIN = get_command('virt-install', package='virt-install')
_VIRSH_BIN = get_command('virsh', package='libvirt-client')
_ANSIBLE_BIN = get_command('ansible', package='ansible')
_QEMU_BIN = get_command('qemu-img', package='qemu-img')


class TestMinishift(Test):
    """
    class to test the contra-env-setup
    """

    def setUp(self):
        """
        configure the virtual machine that will be used in the tests
        """
        self.cmd_run = self.params.get('command', default=None)
        self.debug = self.params.get('debug', default=False)
        self.iso_src = self.params.get('minishift_iso_src_path',
                                       default='~/.contra-env-setup/minishift')
        self.iso_dest = self.params.get('minishift_iso_dest_path',
                                        default='~/.contra-env-setup/minishift')
        self.username = self.params.get('username', default='avocado')
        self.password = self.params.get('password', default='avocado')
        self.vm_name = self.params.get('vm_name', default='contra-env-setup-01')
        self.extra_cmd_run = self.params.get('extra_command', default=None)
        self.distro = self.params.get('distro', default='Fedora')
        self.pkg_mgm = self.params.get('pkg_mgm', default='dnf')
        self.os_variant = self.params.get('os_variant', default='fedora27')

        project = 'https://github.com/CentOS-PaaS-SIG/contra-env-setup.git'
        repo = self.params.get('repo', default=project)
        branch = self.params.get('branch', default='master')

        git.get_repo(repo,
                     branch=branch,
                     destination_dir=self.workdir)

        self.image = vmimage.get(self.distro, cache_dir='~/avocado/data/cache/')

        process.run('{qemu} resize '
                    '{image_path} 40G'.format(qemu=_QEMU_BIN,
                                              image_path=self.image.path))

        cmd = [_VIRTINST_BIN,
               '--import', '--noautoconsole',
               '--connect', 'qemu:///system',
               '--name', self.vm_name,
               '--disk', '%s,size=40' % self.image.path,
               '--graphics', 'vnc',
               '--cpu', 'host',
               '--memory', '7168',
               '--vcpus', '4',
               '--os-variant', self.os_variant,
               '--disk', '%s,device=cdrom,format=iso' %
               create_cloudinit_cdrom(self.vm_name, self.username,
                                      self.password)]

        process.run(' '.join(cmd))

        wait.wait_for(ip_available, timeout=60, args=[self.vm_name])

        cmd = [_VIRSH_BIN,
               '--connect', 'qemu:///system',
               'domifaddr', self.vm_name]
        result = process.run(' '.join(cmd))

        for line in result.stdout_text.splitlines():
            if 'ipv4' in line:
                self.vm_ip = line.split()[3].split('/')[0]

        wait.wait_for(ssh_available, timeout=60, args=[self.vm_ip, self.username])


    def test(self):
        """
        contra-env-setup test
        """
        ssh_args = ['-o UserKnownHostsFile=/dev/null',
                    '-o StrictHostKeyChecking=no']

        cmd = (' {pkg_mgm} install -y python libselinux-python git; '
               ' {pkg_mgm} update -y nettle; ').format(pkg_mgm=self.pkg_mgm)

        if self.debug:
            cmd += (' mkdir -p {dir}; '
                    ' chown avocado:avocado {dir} ').format(dir=self.iso_dest)

        ansible_cmd = (' {ansible} {ip} -i "{ip}," --become '
                       ' -m raw -a "{cmd}" --user {user} '
                       ' --ssh-common-args="{ssh_args}" ')

        ansible_cmd = ansible_cmd.format(ansible=_ANSIBLE_BIN,
                                         ip=self.vm_ip,
                                         cmd=cmd,
                                         user=self.username,
                                         ssh_args=' '.join(ssh_args))

        process.run(ansible_cmd)

        if self.debug is True:
            cmd = ('{ansible} {ip} -i "{ip}," '
                   '-m copy -a "src={src}/minishift.iso dest={dest}/" '
                   '--user {user} '
                   '--ssh-common-args="{ssh}" '.format(ansible=_ANSIBLE_BIN,
                                                       ip=self.vm_ip,
                                                       src=self.iso_src,
                                                       dest=self.iso_dest,
                                                       user=self.username,
                                                       ssh=' '.join(ssh_args)))
            process.run(cmd)

        self.cmd_run = self.cmd_run.replace('localhost', '{ip}'.format(ip=self.vm_ip))

        if self.cmd_run is not None:
            cmd = (' %s'
                   ' --ssh-common-args="%s"' %
                   (self.cmd_run, ' '.join(ssh_args)))
            process.run(cmd)

        if self.debug is True:
            self.log.debug(' Sleeping 10s. Press Ctrl+Z if you want to '
                           ' stop the test to interact with the VM. '
                           ' A new Ctrl+Z will resume the test. ')
            import time
            time.sleep(10)

            if self.extra_cmd_run is not None:
                cmd = (' %s'
                       ' --ssh-common-args="%s"' %
                       (self.extra_cmd_run, ' '.join(ssh_args)))
                process.run(cmd)


    def tearDown(self):
        process.run('virsh --connect qemu:///system destroy %s' %
                    self.vm_name)
        process.run('virsh --connect qemu:///system undefine %s' %
                    self.vm_name)
        os.remove(self.image.path)


if __name__ == '__main__':
    main()
