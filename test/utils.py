"""
contra-env-setup - utils

libraries used in the tests
"""
import os
import tempfile

from command import get_command
from avocado.utils import process


_VIRSH_BIN = get_command('virsh', package='libvirt-client')
_SSH_BIN = get_command('ssh', package='openssh-clients')
_GENISOIMAGE_BIN = get_command('genisoimage', package='genisoimage')


def ip_available(domain):
    """
    check if the IP of the virtual machine created to tests is available
    """
    cmd = ['%s' % _VIRSH_BIN,
           '--connect', 'qemu:///system',
           'domifaddr', domain]
    result = process.run(' '.join(cmd))

    return (False, True)['ipv4' in result.stdout_text]


def ssh_available(vm_ip, username):
    """
    check if ssh is available on the virtual machine created to tests
    """
    ssh_args = ['-o UserKnownHostsFile=/dev/null',
                '-o StrictHostKeyChecking=no']

    cmd = ('{ssh} {username}@{ip} '
           '{ssh_args} true').format(ssh=_SSH_BIN,
                                     username=username,
                                     ip=vm_ip,
                                     ssh_args=' '.join(ssh_args))

    result = process.run(cmd, ignore_status=True)

    return (True, False)[bool(result.exit_status)]


def create_cloudinit_cdrom(domain, username, password):
    """
    creates a CDROM ISO image with the required cloudinit files
    (meta-data and user-data) to make the initial Cloud Image
    configuration, attaching the CDROM to the VM.
    """
    data_dir = tempfile.mkdtemp()
    os.chmod(data_dir, 755)

    metadata_path = os.path.join(data_dir, 'meta-data')
    userdata_path = os.path.join(data_dir, 'user-data')
    iso_path = os.path.join(data_dir, 'cdrom.iso')

    id_rsa_pub_path = os.path.join('~/.ssh/id_rsa.pub')

    with open(os.path.expanduser(id_rsa_pub_path), 'r') as file_obj:
        id_rsa_pub = file_obj.read().strip()

    metadata_content = ['instance-id: %s' % domain,
                        'local-hostname: %s' % domain]

    userdata_content = ['#cloud-config',
                        'ssh_authorized_keys:',
                        ' - %s' % id_rsa_pub,
                        'password: %s' % password,
                        'ssh_pwauth: True',
                        'chpasswd: { expire: False }',
                        'system_info:',
                        '  default_user:',
                        '    name: %s' % username]

    with open(metadata_path, 'w') as metadata_file:
        metadata_file.write('\n'.join(metadata_content))

    with open(userdata_path, 'w') as userdata_file:
        userdata_file.write('\n'.join(userdata_content))

    cmd = [_GENISOIMAGE_BIN,
           '-output', iso_path,
           '-volid', 'cidata',
           '-joliet',
           '-rock', metadata_path, userdata_path]
    process.run(' '.join(cmd))

    return iso_path
