# Contra Environment Setup
![CI-Pipeline](continuous-infra-logo.png)

## Goal of this repository
This tool is normally used locally to create an environment with Minishift and Helm.
It use Ansible to download, install and configure all requirements to this environment. All users will have the same structure basic to install, test and improve your CI/CD Pipelines.

Components used in this deployment:
* [Minishift CentOS ISO](https://github.com/CentOS-PaaS-SIG/minishift-centos-iso)
* [Minishift](https://github.com/minishift/minishift)


The tool automated all projects above in an unique deployment.

## Requirements

* ansible

## Ansible Playbook Role Structure
````
├── continuous-infra-logo.png
├── LICENSE
├── playbooks
│   ├── group_vars
│   │   └── all
│   │       └── global.yml
│   ├── roles
│   │   ├── artifacts
│   │   │   └── tasks
│   │   │       ├── main.yml
│   │   │       └── minishift.yml
│   │   ├── clean
│   │   │   └── tasks
│   │   │       ├── clean.yml
│   │   │       └── main.yml
│   │   ├── minishift
│   │   │   └── tasks
│   │   │       ├── init_minishift.yml
│   │   │       ├── main.yml
│   │   │       └── setup_minishift.yml
│   │   └── prereqs
│   │       ├── install_kvm_plugin.yml
│   │       ├── install_virtual_reqs.yml
│   │       ├── main.yml
│   │       └── setup_nested_virt.yml
│   └── setup.yml
└── README.md
````

### Example
```
ansible-playbook -i "localhost," contra-env-setup/playbooks/setup.yml -k -K
```

if you have all artifacts downloaded in the latest version used for this repository do you can skip this step using:

```
ansible-playbook -i "localhost," contra-env-setup/playbooks/setup.yml -e skip_artifacts=true -k -K
```

## Videos

Installing the Fedora 27 with NESTED enabled to prepare the VM to run contra-env-setup:

[![Install Fedora 27 Nested](http://img.youtube.com/vi/RwJLfyxxD0Y/0.jpg)](http://www.youtube.com/watch?v=RwJLfyxxD0Y "Install Fedora 27 Nested")

Running contra-env-setup in the Fedora 27 VM with NESTED enabled:

[![contra-env-setup](http://img.youtube.com/vi/-C-hKz4s4Xk/0.jpg)](http://www.youtube.com/watch?v=-C-hKz4s4Xk "contra-env-setup")

**NOTE** In both videos have the full transcription about all commands used in each video.


## Playbooks

###  setup.yml
This will setup the whole development environment. It can setup the entire environment
or only certain components. ex. `clean`, `prereqs`, `artifacts` and `minishift`.

### default variables
```
contra-env-setup/playbooks/group_vars/all/global.yml
```

### Key options
_______
* skip_clean: Skip clean up all previous or old deployments : default=false
* skip_prereqs: Skip setting up virtualization and kvm-driver : default=false
* skip_artifacts: Skip artifacts will download, extract and copy all requirements : default=false
* skip_minishift: Skip minishift will configure and start the local cluster : default=false
_______

### All Variables

| Variable Name | Description | Example | Default | Required |
|:------------------------------:|:-----------------------------------------------------------------------:|:--------------------------------------------------:|:-----------------------------------------:|:--------:|
| skip_clean                     |     Skip clean up all previous or old deployments                       | skip_clean=true                                    |   false                                   | No       |
| skip_prereqs                   |     Skip setting up virtualization and kvm-driver                       | skip_prereqs=true                                  |   false                                   | No       |
| skip_artifacts                 |     Skip artifacts will download, extract and copy all requirements     | skip_artifacts=true                                |   false                                   | No       |
| skip_minishift                 |     Skip minishift will configure and start the local cluster           | skip_minishift=true                                |   false                                   | No       |
| remote_user                    |     Define your local username to interact with libvirt                 | remote_user=username                               |   check global.yml                        | No       |
| kvm_plugin_url                 |     URL of the kvm plugin to install                                    | kvm_plugin_url=[url]                               |   check global.yml                        | No       |
| minishift_dest_dir             |     Directory to store minishift binary & helm binary & ISO             | minishift_dest_dir=/home/cloud-user/test           |   "{{ ansible_env.HOME }}/minishift"      | No       |
| minishift_release              |     Release used of minishift                                           | minishift_release="1.14.0"                         |   check global.yml                        | No       |
| minishift_url                  |     URL of the minishift to install                                     | minishift_url=[url]                                |   check global.yml                        | No       |
| minishift_iso                  |     URL of minishift centos ISO to download                             | minishift_iso=[url]                                |   check global.yml                        | No       |
| profile                        |     Profile of minishift for start a new cluster                        | profile=minishift                                  |   minishift                               | No       |
| disk_size                      |     Disk size used for minishift cluster                                | disk_size=20gb                                     |   disk_size=40gb                          | No       |
| memory                         |     Memory used for minishift cluster                                   | memory=4096mb                                      |   memory=6400mb                           | No       |
