# Contra Pipeline Environment Setup :: minishift or OpenShift + OpenShift s2i templates + Jenkins pipelines
![CI-Pipeline](continuous-infra-logo.png)

## Overview

The intent of this setup is to provide a generic way to setup a minishift environment if required or provide
an OpenShift endpoint to setup OpenShift s2i templates and Jenkins 2.0 pipelines from some other projects
repo.  Then the process is automated and a developer or project team can setup their environment with ease.

## Getting Started

You need to have some sort of inventory file just as you do for running any ansible inventory.
This can be a static file, dynamic inventory, or a comma separated list of machines.

### Ansible Inventory

- "10.10.10.1,10.10.10.2,"
- [ansible inventory](http://docs.ansible.com/ansible/intro_inventory.html)
- [ansible dynamic inventory](http://docs.ansible.com/ansible/intro_dynamic_inventory.html)

### Generic Examples

```
ansible-playbook -i "10.8.170.204," contra-env-setup/playbooks/setup.yml \
 -e project_repo=https://github.com/CentOS-PaaS-SIG/contra-env-sample-project \
 -e project_branch=master -K -k

```

## Ansible Playbook Role Structure
````
├── continuous-infra-logo.png
├── LICENSE
├── playbooks
│   ├── group_vars
│   │   └── all
│   │       └── global.yml
│   ├── roles
│   │   ├── cleanup
│   │   │   └── tasks
│   │   │       ├── cleanup.yml
│   │   │       └── main.yml
│   │   ├── create
│   │   │   └── tasks
│   │   │       └── main.yml
│   │   ├── minishift
│   │   │   └── tasks
│   │   │       ├── init_minishift.yml
│   │   │       ├── install_minishift_bin.yml
│   │   │       ├── main.yml
│   │   │       └── set_minishift_path.yml
│   │   ├── os_temps
│   │   │   ├── tasks
│   │   │   │   ├── add_scc.yml
│   │   │   │   ├── build_new_app.yml
│   │   │   │   ├── clone_project_repo.yml
│   │   │   │   ├── get_set_project.yml
│   │   │   │   ├── login_to_cluster.yml
│   │   │   │   ├── main.yml
│   │   │   │   ├── set_oc_client.yml
│   │   │   │   ├── setup_containers.yml
│   │   │   │   ├── setup_os_templates.yml
│   │   │   │   └── start_mcluster.yml
│   │   │   └── templates
│   │   │       └── contra-env-setup-scc.yaml.j2
│   │   ├── pipeline
│   │   │   ├── files
│   │   │   │   └── JenkinsfileContraSample1
│   │   │   ├── tasks
│   │   │   │   ├── main.yml
│   │   │   │   └── setup_sample_pipelines.yml
│   │   │   └── templates
│   │   │       └── contra-sample-pipeline1.xml.j2
│   │   └── prereqs
│   │       └── tasks
│   │           ├── install_kvm_plugin.yml
│   │           ├── install_virtual_reqs.yml
│   │           ├── main.yml
│   │           └── setup_nested_virt.yml
│   └── setup.yml
└── README.md
````

### Playbooks

####  setup.yml

This will setup the minishift + pipeline development environment.  It can setup the entire environment
or only certain components.  ex. minishift, jenkins infra, pipeline containers, and fed-msg relay

##### default variables
```
contra-env-setup/playbooks/group_vars/all/global.yml

```
##### Pre-Setup options

* run_cleanup: Run clean up of previous setup : default=false
* run_prereqs: Run setting up virtualization and kvm-driver : default=true
* contra_env_setup_dir: Directory to store the contra-env-setup :  default "{{ ansible_env.HOME }}/.contra-env-setup
* 

##### Override options

* force_minishift_install: Override an existing install of minishift : default=false
* force_repo_clone: Force cloning of project repo

##### Minishift and OpenShift setup options

##### Minishift setup options
* setup_minishift: Setup a minishift cluster : default=true
* start_minishift: Start existing minishift cluster : default=true
* minishift_version: Minishift version to use : default=v1.12.0
* minishift_dest_dir: Minishift binary and ISO directory : default={{ contra_env_setup_dir }}/minishift
* profile: Minishift profile : default=minishift
* disk_size: Disk size to use for minishift : default=40gb
* memory_size: Memory size to use for the VM : default=6400mb
* minishift_iso: ISO image to use : default=http://artifacts.ci.centos.org/fedora-atomic/minishift/iso/minishift.iso 

##### oc setup options
* openshift_project: OpenShift project name : default:contra-sample-project
* modify_tags: Modify tags of containers : default=true
* tag: Add a tag besides latest : default=stable
* modify_scc: Create/update the security context constraints : default=true
* oc_version: oc version to use to communicate to the OpenShift cluster : default=V3.6.1

#### Project repo options that has s2i templates and Jenkins Pipelines
* project_repo: Project repo to import templates and pipelines from : default=https://github.com/CentOS-PaaS-SIG/contra-env-sample-project
* project_refspec: Project refspec : default=+refs/pull/*:refs/heads/* 
* project_branch: Project branch : default=master
* project_dir: Project directory where repo is stored locally : default={{ contra_env_setup_dir }}/{{ project_repo.split('/')[-1] }}

#### OpenShift s2i template setup options
* setup_containers: Setup OpenShift s2i templates : default=true
* os_template_dir: Relative directory in the repo where OpenShift s2i templates are stored: default=config/s2i

#### Jenkins 2.0 pipeline setup options
* setup_pipelines: Setup Jenkins 2.0 pipelines : default=false
* setup_sample_pipelines: Setup sample pipelines from this repo : default=false
* pipeline_dir: Relative directory in the project repo where Jenkins pipelines are stored: default=config/pipelines

#### Usage examples

###### Example 1: Setup on a local server :: setup Minishift + OS templates 

 1. Install on a local server as user cloud-user.
 2. Setup pre-reqs (kvm driver and nested virtualization)
 3. Setup a minishift cluster.
 4. Setup OpenShift s2i templates
 5. Modify my container tags with the default tag. tag=stable
 6. Override the project_repo with another one then the default in global.yml
 7. The -K is used to prompt you for your password for sudo (if you require one)
 8. The -k is used to prompt you for your ssh password can hit enter if using -K and they are the same<br>
    _Note: Instead of -k you could use --private-key=<absolute_path_to_ssh_private_key>_
    
```
    ansible-playbook -vv -i "localhost," \
    ~/CentOS-PaaS-SIG/contra-env-setup/playbooks/setup.yml \
    -e remote_user=cloud-user 
    -e project_repo=https://github.com/arilivigni/ci-pipeline -K -k

```

###### Example 2: Setup on a local server :: Cleanup previous contra-env-setup + Force clone of project repo

 
 1. Install on a local server as user ari.
 2. Run cleanup of previous setup
 3. Don't setup pre-reqs (kvm driver and nested virtualization)
 4. Don't setup a minishift cluster.
 5. Don't setup OpenShift s2i templates.
 6. Don't modify my container tags and 
 7. Don't clone the pipeline repo even if it exists.

```
    ansible-playbook -vv -i "localhost," --private-key=/home/cloud-user/my-key \
    ~/CentOS-PaaS-SIG/contra-env-setup/playbooks/setup.yml \
    -e remote_user=ari -e run_cleanup=true
    -e run_prereqs=false -e setup_minishift=false \
    -e setup_containers=false -e force_clone=true -K
```