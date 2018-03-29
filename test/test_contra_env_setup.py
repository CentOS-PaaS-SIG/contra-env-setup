"""
contra-env-setup continuous integration test
"""
from avocado_qemu import QemuTest
from avocado_qemu import GetConsole

from avocado.utils import vmimage
from avocado.utils import git
from avocado.utils import process
from avocado.utils import path as utils_path


class TestMinishift(QemuTest):
    """
    :avocado: enable
    """
    def setUp(self):
        # getting parameters from test_contra_env_setup.yaml
        self.distro = self.params.get('distro', default='Fedora')
        self.pkg_mgm = self.params.get('pkg_mgm', default='dnf')
        self.debug = self.params.get('DEBUG', default=None)
        self.iso_src = self.params.get('minishift_iso_src_path', default=None)
        self.iso_dest = self.params.get('minishift_iso_dest_path', default=None)
        self.cmd_run = self.params.get('command', default=None)
        self.extra_cmd_run = self.params.get('extra_command', default=None)

        project = 'https://github.com/CentOS-PaaS-SIG/contra-env-setup.git'
        repo = self.params.get('repo', default='{0}'.format(project))
        branch = self.params.get('branch', default='master')

        # cloning the repo defined in the parameter file
        git.get_repo(repo,
                     branch=branch,
                     destination_dir=self.workdir)

        # getting the VM image qcow2
        image = vmimage.get(self.distro, cache_dir='~/avocado/data/cache/')

        # resize storage of VM
        qemu_img_bin = utils_path.find_command('qemu-img')
        process.run('%s resize %s +20G' % (qemu_img_bin, image.path))

        # adding the VM image
        self.vm.add_image(image.path, cloudinit=True, snapshot=False)

        # network
        self.vm.args.extend(['-device', 'virtio-net-pci,id=avocado_nic,netdev=device_avocado_nic'])
        self.vm.args.extend(['-netdev', 'user,id=device_avocado_nic,hostfwd=tcp::12345-:22'])

        # CPU/Memmory
        self.vm.args.extend(['-m', '7168'])
        self.vm.args.extend(['-cpu', 'host'])
        self.vm.args.extend(['-accel', 'kvm'])

        # headless
        self.vm.args.extend(['-display', 'none', '-vga', 'none'])

        # run!
        self.vm.launch()

        # wait VM to be UP
        with GetConsole(self.vm) as console:
            console.sendline('sudo resize2fs /dev/sda1')


    def test(self):
        """
        contra-env-setup test
        """
        # set the SSH options and port
        env = {'ANSIBLE_CONFIG': 'test/ansible.cfg'}
        ssh_args = ['-o UserKnownHostsFile=/dev/null',
                    '-o StrictHostKeyChecking=no']

        # install python, git and update nettle to libvirt network
        cmd = (' ansible localhost -i "localhost," --become '
               ' -m raw -a "%s install -y python libselinux-python git; '
               ' dnf update -y nettle" --user %s --ssh-common-args="%s" ' %
               (self.pkg_mgm, self.vm.username, ' '.join(ssh_args)))
        process.run(cmd, env=env)

        if self.debug is True:
            # Create the directory to storage the ISO in VM
            cmd = (' ansible localhost -i "localhost," '
                   ' -m raw -a "mkdir -p %s" '
                   ' --user %s --ssh-common-args="%s" ' %
                   (self.iso_src, self.vm.username, ' '.join(ssh_args)))
            process.run(cmd, env=env)

            # Copy the minishift.iso of host to VM
            cmd = (' ansible localhost -i "localhost," '
                   ' -m copy -a "src=%s/minishift.iso dest=%s/" '
                   ' --user %s --ssh-common-args="%s" ' %
                   (self.iso_src, self.iso_dest, self.vm.username, ' '.join(ssh_args)))
            process.run(cmd, env=env)

        # Run the contra-env-setup playbook
        cmd = (' %s'
               ' --ssh-common-args="%s"' %
               (self.cmd_run, ' '.join(ssh_args)))
        process.run(cmd, env=env)

        # Used to DEBUG mode to VM continue UP waiting user interaction
        if self.debug is True:
            self.log.debug(' Sleeping 10s. Press Ctrl+Z is you want to '
                           ' stop the test to interact with the VM. '
                           ' A new Ctrl+Z will resume the test calling to '
                           ' the extra command defined. ')
            import time
            time.sleep(10)

            cmd = (' %s'
                   ' --ssh-common-args="%s"' %
                   (self.extra_cmd_run, ' '.join(ssh_args)))
            process.run(cmd, env=env)


    def tearDown(self):
        self.vm.shutdown()
