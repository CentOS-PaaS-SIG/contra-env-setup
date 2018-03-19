from avocado_qemu import test
from avocado.utils import vmimage
from avocado.utils import git
from avocado.utils import process


class TestMinishift(test.QemuTest):
    """
    :avocado: enable
    """
    def setUp(self):
        distro = self.params.get('distro', default='Fedora')
        image = vmimage.get(distro, cache_dir='~/minishift/')
        self.vm.add_image(image.path, cloudinit=True, snapshot=False)

        self.vm.args.extend(['-device', 'virtio-net-pci,id=avocado_nic,netdev=device_avocado_nic'])
        self.vm.args.extend(['-netdev', 'user,id=device_avocado_nic,hostfwd=tcp::12345-:22'])

        self.vm.args.extend(['-m', '6400'])
        self.vm.args.extend(['-cpu', 'host'])
        self.vm.args.extend(['-accel', 'kvm'])

        # Headless
        self.vm.args.extend(['-display', 'none', '-vga', 'none'])

        self.vm.launch()
        console = self.vm.get_console()
        console.close()

        git.get_repo('https://github.com/firemanxbr/contra-env-setup.git',
                     destination_dir=self.workdir)

    def test(self):
        print('WORKDIR: {0}'.format(self.workdir))

        ssh_args = ['-o UserKnownHostsFile=/dev/null',
                    '-o StrictHostKeyChecking=no',
                    '-p 12345']

        cmd = ('ansible localhost -i "localhost," --become '
               '-m raw -a "dnf install -y python" --user %s '
               '--ssh-common-args="%s"' %
              (self.vm.username, ' '.join(ssh_args)))
        process.run(cmd)

        cmd = ('ansible-playbook -i "localhost," playbooks/setup.yml '
               '-e remote_user=%s --ssh-common-args="%s"' %
              (self.vm.username, ' '.join(ssh_args)))
        process.run(cmd)


    def tearDown(self):
        self.vm.shutdown()
