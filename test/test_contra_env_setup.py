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
        repo = self.params.get('repo', default='https://github.com/CentOS-PaaS-SIG/contra-env-setup.git')
        branch = self.params.get('branch', default='master')
        git.get_repo(repo,
                     branch=branch,
                     destination_dir=self.workdir)
        
        # VM Image
        distro = self.params.get('distro', default='Fedora')
        image = vmimage.get(distro, cache_dir='~/avocado/data/cache/')
        
        # Resize storage of VM
        qemu_img_bin = utils_path.find_command('qemu-img')
        process.run('%s resize %s +20G' % (qemu_img_bin, image.path))
        
        self.vm.add_image(image.path, cloudinit=True, snapshot=False)

        # Network
        self.vm.args.extend(['-device', 'virtio-net-pci,id=avocado_nic,netdev=device_avocado_nic'])
        self.vm.args.extend(['-netdev', 'user,id=device_avocado_nic,hostfwd=tcp::12345-:22'])

        # CPU/Memmory
        self.vm.args.extend(['-m', '7168'])
        self.vm.args.extend(['-cpu', 'host'])
        self.vm.args.extend(['-accel', 'kvm'])

        # Headless
        self.vm.args.extend(['-display', 'none', '-vga', 'none'])

        # Run!
        self.vm.launch()

        # Wait VM to be UP
        with GetConsole(self.vm) as console:
            console.sendline('sudo resize2fs /dev/sda1')


    def test(self):
        # Set the SSH options and port
        env = {'ANSIBLE_CONFIG': 'test/ansible.cfg'}
        ssh_args = ['-o UserKnownHostsFile=/dev/null',
                    '-o StrictHostKeyChecking=no']

        # Install python and update nettle to libvirt network
        cmd = (' ansible localhost -i "localhost," --become '
               ' -m raw -a "dnf install -y python libselinux-python; '
               ' dnf update -y nettle" --user %s --ssh-common-args="%s" ' %
              (self.vm.username, ' '.join(ssh_args)))
        process.run(cmd, env=env)

        # Parameters used to DEBUG mode
        DEBUG = self.params.get('DEBUG', default=None)
        iso_src = self.params.get('minishift_iso_src_path', default=None)
        iso_dest = self.params.get('minishift_iso_dest_path', default=None)

        if DEBUG is not None:
            # Create the directory to storage the ISO in VM
            cmd = (' ansible localhost -i "localhost," '
                ' -m raw -a "mkdir -p %s" '
                ' --user %s --ssh-common-args="%s" ' %
                (iso_src, self.vm.username, ' '.join(ssh_args)))
            process.run(cmd, env=env)

            # Copy the minishift.iso of host to VM
            cmd = (' ansible localhost -i "localhost," '
                ' -m copy -a "src=%s/minishift.iso dest=%s/" '
                ' --user %s --ssh-common-args="%s" ' %
                (iso_src, iso_dest, self.vm.username, ' '.join(ssh_args)))
            process.run(cmd, env=env)


        # Run the contra-env-setup playbook
        cmd = (' ansible-playbook -vv -i "localhost," playbooks/setup.yml '
               ' -e remote_user=%s -e skip_cleanup=false '
               ' -e setup_pipelines=false --ssh-common-args="%s"' %
              (self.vm.username, ' '.join(ssh_args)))
        process.run(cmd, env=env)

        # Used to DEBUG mode to VM continue UP
        if DEBUG is not None:
            import time
            time.sleep(99999)


    def tearDown(self):
        self.vm.shutdown()
