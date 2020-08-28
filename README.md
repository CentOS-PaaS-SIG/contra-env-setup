<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Contra Environment Setup](#contra-environment-setup)
- [minishift or OpenShift + OpenShift s2i templates + Jenkins pipelines](#minishift-or-openshift--openshift-s2i-templates--jenkins-pipelines)
  - [Overview](#overview)
  - [Getting Started](#getting-started)
    - [Ansible Inventory](#ansible-inventory)
  - [Playbooks](#playbooks)
    - [setup.yml](#setupyml)
    - [default variables](#default-variables)
  - [Pre-Setup options](#pre-setup-options)
  - [Override options](#override-options)
  - [Minishift and OpenShift setup options](#minishift-and-openshift-setup-options)
    - [Minishift setup options](#minishift-setup-options)
    - [oc setup options](#oc-setup-options)
  - [Project repo options that has s2i templates and Jenkins Pipelines](#project-repo-options-that-has-s2i-templates-and-jenkins-pipelines)
    - [OpenShift s2i template setup options](#openshift-s2i-template-setup-options)
    - [Jenkins 2.0 pipeline setup options](#jenkins-20-pipeline-setup-options)
    - [Metrics setup options](#metrics-setup-options)
    - [Jenkins Job DSL setup options](#jenkins-job-dsl-setup-options)
  - [Templates](#templates)
  - [Usage examples](#usage-examples)
    - [Example 1: Basic setup on a local machine :: Setup Minishift + Helper infra OS templates](#example-1-basic-setup-on-a-local-machine--setup-minishift--helper-infra-os-templates)
    - [Example 2: Setup on a local machine :: Setup Minishift + Helper infra OS templates + OS templates from some project](#example-2-setup-on-a-local-machine--setup-minishift--helper-infra-os-templates--os-templates-from-some-project)
    - [Example 3: Setup on a local machine :: Setup Minishift + Helper infra OS templates + Jenkins 2.0 pipelines](#example-3-setup-on-a-local-machine--setup-minishift--helper-infra-os-templates--jenkins-20-pipelines)
    - [Example 4: Setup on a local machine :: Setup Minishift + OS templates + Jenkins 2.0 pipelines](#example-4-setup-on-a-local-machine--setup-minishift--os-templates--jenkins-20-pipelines)
    - [Example 5: Setup on a local machine :: Start Minishift w/profile mysetup + OS templates + Jenkins 2.0 pipelines](#example-5-setup-on-a-local-machine--start-minishift-wprofile-mysetup--os-templates--jenkins-20-pipelines)
    - [Example 6: Setup on a local machine :: Using the playbook hooks on contra-env-setup](#example-6-setup-on-a-local-machine--using-the-playbook-hooks-on-contra-env-setup)
    - [Example 7: Setup on a local machine :: Start Minishift w/profile mysetup + OS templates + Jenkins 2.0 pipelines](#example-7-setup-on-a-local-machine--start-minishift-wprofile-mysetup--os-templates--jenkins-20-pipelines)
    - [Example 8: Setup on a local machine :: Setup Jenkins with metrics enabled](#example-8-setup-on-a-local-machine--setup-jenkins-with-metrics-enabled)
    - [Example 9a: OpenShift cluster instance endpoint + Helper infra OS templates + OS templates from some project](#example-9a-openshift-cluster-instance-endpoint--helper-infra-os-templates--os-templates-from-some-project)
    - [Example 9b: From a File ex. my-project-example.yml](#example-9b-from-a-file-ex-my-project-exampleyml)
      - [File my-project-example.yml](#file-my-project-exampleyml)
      - [Command Execution with file my-project-example.yml](#command-execution-with-file-my-project-exampleyml)
  - [Mac Users](#mac-users)
  - [Debugging Issues](#debugging-issues)
    - [Issue #1: Can't push images to the Minishift cluster](#issue-1-cant-push-images-to-the-minishift-cluster)
      - [Solution #1:](#solution-1)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->
![my-project-example](continuous-infra-logo.png "continuous-infra")
# Contra Environment Setup
# minishift or OpenShift + OpenShift s2i templates + Jenkins pipelines


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

## Playbooks

###  setup.yml

This will setup the minishift + pipeline development environment.  It can setup the entire environment
or only certain components.  ex. minishift, jenkins infra, pipeline containers, and fed-msg relay

### default variables
`contra-env-setup/playbooks/group_vars/all/global.yml`

## Pre-Setup options

* run_cleanup: Run clean up of previous setup : default=false
* run_prereqs: Run setting up virtualization and kvm-driver : default=true
* setup_nested_virt: Run setting up of nested virtualization : default=true
* shell_rc: Set your shell configuration file : default=.bashrc
* contra_env_setup_dir: Directory to store the contra-env-setup :  default "{{ ansible_env.HOME }}/.contra-env-setup

## Override options

* force_minishift_install: Override an existing install of minishift : default=false
* force_repo_clone: Force cloning of project repo : default=false
* force_template_overwrite: Force overwriting of OpenShift templates and their resources if they already exist : default=false

## Minishift and OpenShift setup options

### Minishift setup options
* setup_minishift: Setup a minishift cluster : default=true
* minishift_version: Minishift version to use : default=v1.12.0
* minishift_dest_dir: Minishift binary and ISO directory : default={{ contra_env_setup_dir }}/minishift
* profile: Minishift profile : default=minishift
* user: account to use for libvirt setup
* disk_size: Disk size to use for minishift : default=40gb
* memory: Recommended memory size to use for the VM : default=8092mb
* cpus: Number of cpus to use for minishift VM: default=2
* minishift_iso: ISO image to use : default=http://artifacts.ci.centos.org/fedora-atomic/minishift/iso/minishift.iso
* minishift_insecure_registry: Additional insecure registries : default="" (not used)
* minishift_registry_mirror: Optional mirror for registries : default="" (not used)

### oc setup options
* openshift_project: OpenShift project name : default:contra-sample-project
* openshift_project_display_name: OpenShift project display name : default:Contra Sample Project
* openshift_cluster_ip: Cluster IP of OpenShift console. Set this if not using Minishift : default: <empty string>
* modify_tags: Modify tags of containers : default=true
* tag: Add a tag besides latest : default=stable
* modify_scc: Create/update the security context constraints : default=true
* oc_version: oc version to use to communicate to the OpenShift cluster : default=V3.6.1

## Project repo options that has s2i templates and Jenkins Pipelines
* project_repo: Project repo to import templates and pipelines from : default=https://github.com/CentOS-PaaS-SIG/contra-env-sample-project
* project_refspec: Project refspec : default=+refs/pull/*:refs/heads/*
* project_branch: Project branch : default=master
* project_dir: Project directory where repo is stored locally : default={{ contra_env_setup_dir }}/{{ project_repo.split('/')[-1] }}
* setup_sample_project: Sample profect to setup

### OpenShift s2i template setup options
* setup_containers: Setup OpenShift s2i templates : default=true
* os_template_dir: Relative directory in the project repo where OpenShift s2i templates are stored: default=config/s2i
* os_template_whitelist: List of OpenShift template names which will be built exclusively (other templates will be skipped) if this list isn't empty : default=[]
* os_template_blacklist: List of Openshift template names which will be skipped, takes precedence over the os_template_whitelist : default=[]
* sample_os_template_dir: Relative directory in the sample project repo where OpenShift s2i templates are stored: default=config/s2i

### Jenkins 2.0 pipeline setup options
* setup_pipelines: Setup Jenkins 2.0 pipelines : default=false
* pipeline_dir: Relative directory in the project repo where Jenkins pipelines are stored: default=config/pipelines/buildconfigs
* sample_pipeline_dir: Relative directory in the sample project repo where Jenkins pipelines are stored: default=config/pipelines/buildconfigs

### Metrics setup options
* jenkins_enable_metrics: Used to configure the Jenkins Influxdb plugin
* influxdb_admin_user: The admin username for Influxdb
* influxdb_admin_password: The password to give the admin user
* influxdb_api_route: The route that Jenkins will use to contact Influxdb
* grafana_admin_user: The admin username for Grafana
* grafana_admin_password: The password to give the Grafana admin

### Jenkins Job DSL setup options
* jenkins_dsl_job_repo: The repo to pull jobs from. Configured as GitHubORG/repoName
* jenkins_dsl_repo_branch: The branch of the job dsl repo

## Templates

Note that it is possible to use {{ ansible_vars }} in your Openshift Templates.

## Usage examples

### Example 1: Basic setup on a local machine :: Setup Minishift + Helper infra OS templates

 1. Install on a local machine as user $USER.
 2. Setup a minishift cluster
 3. Setup helper infrastructure containers such as:
    1. Jenkins
    2. Jenkins-slave
    3. ansible-execeutor
    4. linchpin-executor
    5. container-tools<br>
    _Note: Exclude other helper containers influxdb and grafana_
 4. Modify my container tags with the default tag. tag=stable

```
ansible-playbook -vv -i "localhost," contra-env-setup/playbooks/setup.yml \
    -e user=$USER \
    -e openshift_project=my-project-example -K -k
```
_Note: The -K is used to prompt you for your password for sudo (if you require one) <br>
       The -k is used to prompt you for your ssh password can hit enter if using -K and they are the same<br>
       Instead of -k you could use --private-key=<absolute_path_to_ssh_private_key>_
       
       
### Example 2: Setup on a local machine :: Setup Minishift + Helper infra OS templates + OS templates from some project

 1. Install on a local machine as user $USER.
 2. Setup pre-reqs (kvm driver and nested virtualization)
 3. Setup a minishift cluster
 4. Setup helper infrastructure containers such as:
    1. Jenkins
    2. Jenkins-slave
    3. ansible-execeutor
    4. linchpin-executor
    5. container-tools<br>
    _Note: Exclude other helper containers influxdb and grafana_
 5. Setup OpenShift s2i templates from the -e project_repo=https://github.com/arilivigni/my-project-example
    1. Override the project_repo with another one then the default in global.yml
    2. OpenShift project -e openshift_project=my-project-example 
 6. Modify my container tags with the default tag. tag=stable

```
    ansible-playbook -vv -i "localhost," contra-env-setup/playbooks/setup.yml \
    -e user=$USER \
    -e project_repo=https://github.com/arilivigni/my-project-example
    -e openshift_project=my-project-example -K -k
```
_Note: The -K is used to prompt you for your password for sudo (if you require one) <br>
       The -k is used to prompt you for your ssh password can hit enter if using -K and they are the same<br>
       Instead of -k you could use --private-key=<absolute_path_to_ssh_private_key>_


### Example 3: Setup on a local machine :: Setup Minishift + Helper infra OS templates + Jenkins 2.0 pipelines

 1. Install on a local machine as user $USER.
 2. Setup pre-reqs (kvm driver and nested virtualization)
 3. Setup a minishift cluster
 4. Setup helper infrastructure containers such as:
    1. Jenkins
    2. Jenkins-slave
    3. ansible-execeutor
    4. linchpin-executor
    5. container-tools<br>   
 5. Exclude my-test-app template
 6. Modify my container tags with the default tag. tag=stable
 7. Setup Jenkins 2.0 pipelines from the sample project

```
ansible-playbook -vv -i "localhost," contra-env-setup/playbooks/setup.yml \
    -e user=$USER \
    -e os_template_blacklist=['my-test-app'] \
    -e openshift_project=my-project-example \
    -e setup_pipelines=true -K -k
```
_Note: The -K is used to prompt you for your password for sudo (if you require one) <br>
       The -k is used to prompt you for your ssh password can hit enter if using -K and they are the same<br>
       Instead of -k you could use --private-key=<absolute_path_to_ssh_private_key>_


### Example 4: Setup on a local machine :: Setup Minishift + OS templates + Jenkins 2.0 pipelines

 1. Install on a local machine as user $USER.
 2. Setup pre-reqs (kvm driver and nested virtualization)
 3. Setup a minishift cluster
 4. Setup OpenShift s2i templates from the -e project_repo=https://github.com/arilivigni/my-project-example
    1. Override the project_repo with another one then the default in global.yml
    2. OpenShift project -e openshift_project=my-project-example
 5. Modify my container tags with the tag=develop
 6. Setup Jenkins 2.0 pipelines from the project_repo=https://github.com/arilivigni/my-project-example
 7. Setup sample project templates and pipelines
    from the project_repo=https://github.com/CentOS-PaaS-SIG/contra-env-sample-project
```
ansible-playbook -vv -i "localhost," contra-env-setup/playbooks/setup.yml \
    -e user=$USER \
    -e project_repo=https://github.com/arilivigni/my-project-example \
    -e openshift_project=my-project-example \
    -e tag=develop \
    -e setup_pipelines=true \
    -e setup_sample_project=true -K -k
```
_Note: The -K is used to prompt you for your password for sudo (if you require one) <br>
       The -k is used to prompt you for your ssh password can hit enter if using -K and they are the same<br>
       Instead of -k you could use --private-key=<absolute_path_to_ssh_private_key>_

### Example 5: Setup on a local machine :: Start Minishift w/profile mysetup + OS templates + Jenkins 2.0 pipelines

 1. Install on a local machine as user $USER.
 2. Setup pre-reqs (kvm driver and nested virtualization)
 3. Start minishift cluster with profile mysetup
 4. Setup OpenShift s2i templates from the -e project_repo=https://github.com/arilivigni/my-project-example
    1. Override the project_repo with another one then the default in global.yml
    2. OpenShift project -e openshift_project=my-project-example
 5. Modify my container tags with the tag=develop
 6. Setup Jenkins 2.0 pipelines from the project_repo=https://github.com/arilivigni/my-project-example
 7. Setup sample project templates and pipelines
    from the project_repo=https://github.com/CentOS-PaaS-SIG/contra-env-sample-project
```
ansible-playbook -vv -i "localhost," contra-env-setup/playbooks/setup.yml \
    -e user=$USER \
    -e project_repo=https://github.com/arilivigni/my-project-example \
    -e openshift_project=my-project-example \
    -e tag=develop \
    -e setup_pipelines=true \
    -e setup_sample_project=true \
    -e start_minishift=true \
    -e profile=mysetup -K -k
```
_Note: The -K is used to prompt you for your password for sudo (if you require one) <br>
       The -k is used to prompt you for your ssh password can hit enter if using -K and they are the same<br>
       Instead of -k you could use --private-key=<absolute_path_to_ssh_private_key>_

### Example 6: Setup on a local machine :: Using the playbook hooks on contra-env-setup

This resource permit to create your playbooks to included as the last role that will be
executed on contra-env-setup.

```
ansible-playbook -vv -i "localhost," contra-env-setup/playbooks/setup.yml \
    -e user=$USER \
    -e project_repo=https://github.com/arilivigni/my-project-example \
    -e openshift_project=my-project-example-example \
    -e tag=develop \
    -e setup_pipelines=true \
    -e setup_sample_project=true \
    --extra-vars='{"hooks": ["/contra-env-setup/playbook_a.yml","/contra-env-setup/playbook_b.yml"]}' -K -k
```

### Example 7: Setup on a local machine :: Start Minishift w/profile mysetup + OS templates + Jenkins 2.0 pipelines

 1. Install on a local machine as user $USER.
 2. Setup pre-reqs (kvm driver and nested virtualization)
 3. Start minishift cluster with profile mysetup
 4. Setup OpenShift s2i templates from the -e project_repo=https://github.com/arilivigni/my-project-example
    1. Override the project_repo with another one then the default in global.yml
    2. OpenShift project -e openshift_project=my-project-example
 5. Disable setup of the helper containers ansible-executor and linchpin-executor
 6. Setup Jenkins 2.0 pipelines from the project_repo=https://github.com/arilivigni/my-project-example
 7. Setup sample project templates and pipelines
    from the project_repo=https://github.com/CentOS-PaaS-SIG/contra-env-sample-project
```
ansible-playbook -vv -i "localhost," contra-env-setup/playbooks/setup.yml \
    -e user=$USER \
    -e project_repo=https://github.com/arilivigni/my-project-example \
    -e openshift_project=my-project-example-example \ 
    -e setup_helper_containers=false \
    -e setup_pipelines=true \
    -e start_minishift=true \
    -e profile=mysetup -K -k
```
_Note: The -K is used to prompt you for your password for sudo (if you require one) <br>
       The -k is used to prompt you for your ssh password can hit enter if using -K and they are the same<br>
       Instead of -k you could use --private-key=<absolute_path_to_ssh_private_key>_

### Example 8: Setup on a local machine :: Setup Jenkins with metrics enabled

 1. Install on a local machine as current user
 2. Start minishift cluster with profile minishift
 3. Run Jenkins with metrics enabled
 4. Load containers from a user defined as project_repo from joejstuart/contra-demo
 5. Load helper containers from CentOS-PaaS-SIG/contra-env-infra
 6. Setup Jenkins with a a job DSL seed job and sample jobs from CentOS-PaaS-SIG/contra-env-sample-project
 7. Disable the linchpin-executor container
 
```
ansible-playbook -vv -i "localhost," contra-env-setup/playbooks/setup.yml \
    -e user=$USER \
    -e profile=minishift \
    -e run_prereqs=false \
    -e setup_minishift=true \
    -e start_minishift=true \
    -e setup_containers=true \
    -e helper_project_repo=https://github.com/CentOS-PaaS-SIG/contra-env-infra \
    -e helper_project_branch=master \
    --extra-vars='{"os_template_blacklist": ["linchpin-executor", "ansible-executor"]}' \
    -e project_repo=https://github.com/joejstuart/contra-demo \
    -e project_branch=master \
    -e jenkins_enable_metrics=true \
    -e jenkins_dsl_job_repo=CentOS-PaaS-SIG/contra-env-sample-project -K -k
```
_Note: The -K is used to prompt you for your password for sudo (if you require one) <br>
       The -k is used to prompt you for your ssh password can hit enter if using -K and they are the same<br>
       Instead of -k you could use --private-key=<absolute_path_to_ssh_private_key>_

### Example 9a: OpenShift cluster instance endpoint + Helper infra OS templates + OS templates from some project

 1. Install on an OpenShift cluster endpoint.
 2. Setup helper infrastructure containers such as:
    1. Jenkins
    2. Jenkins-slave
    3. ansible-execeutor
    4. linchpin-executor
    5. container-tools<br>
    _Note: Exclude other helper containers influxdb and grafana_
 3. Setup OpenShift s2i templates from the -e project_repo=https://github.com/arilivigni/my-project-example
    1. Override the project_repo with another one then the default in global.yml
    2. OpenShift project -e openshift_project=my-project-example 
 4. Modify my container tags with the default tag. tag=stable
 5. Don't setup or start minishift
 6. Don't run pre-reqs

```
ansible-playbook -vv -i "localhost," contra-env-setup/playbooks/setup.yml \
    -e user=$USER \
    -e project_repo=https://github.com/arilivigni/my-project-example \
    -e openshift_project=my-project-example-example \
    -e setup_minishift=false \
    -e start_minishift=true \
    -e run_prereqs=false -K -k
```
_Note: The -K is used to prompt you for your password for sudo (if you require one) <br>
       The -k is used to prompt you for your ssh password can hit enter if using -K and they are the same<br>
       Instead of -k you could use --private-key=<absolute_path_to_ssh_private_key>_

### Example 9b: From a File ex. my-project-example.yml

#### File my-project-example.yml
```

---
# run roles based on certain params
run_cleanup: true
run_prereqs: false
setup_nested_virt: false
setup_minishift: false
start_minishift: false
setup_containers: true
setup_helper_containers: true
setup_pipelines: false
setup_sample_project: false 
setup_playbook_hooks: false
force_minishift_install: false
force_repo_clone: false

# Default location to store contra-env-setup
contra_env_setup_dir: "{{ ansible_env.HOME }}/.contra-env-setup"


# cluster username
username: developer

# cluster password
password: developer

# cluster admin username
admin_username: system

# cluster admin password
admin_password: admin

# project name and display name for openshift
openshift_project: my-project-example
openshift_project_display_name: "my-project-example"

# modify tags on images
modify_tags: true

# tag to use
tag: stable

# modify security context contraints (SCC) to run privileged containers
modify_scc: false

## oc cli vars
# oc version
oc_version: v3.11.0

# Path to oc binary directory
oc_bin_path: "{{ ansible_env.HOME }}/.minishift/cache/oc/{{ oc_version }}/{{ host_os }}"

# Path to oc binary
oc_bin: "{{ oc_bin_path }}/oc"

## Project repo setup

# Project repo
project_repo: https://github.com/arilivigni/my-project-example

# Project repo refspec
project_refspec: '+refs/pull/*:refs/heads/*'

# Project repo branch or sha
project_branch: 'development'

# Project directory
project_dir: "{{ contra_env_setup_dir }}/{{ project_repo.split('/')[-1] | replace('.git', '') }}"

# OpenShift template directory
os_template_dir: "config/templates"

# OpenShift template blacklist, not used if whitelist is set
os_template_blacklist:
  - influxdb
  - grafana

```
 
#### Command Execution with file my-project-example.yml


```
ansible-playbook -vv -i "localhost," contra-env-setup/playbooks/setup.yml \
    -e user=$USER \
    -e @my-project-example.yml -K -k
```
_Note: The -K is used to prompt you for your password for sudo (if you require one) <br>
       The -k is used to prompt you for your ssh password can hit enter if using -K and they are the same<br>
       Instead of -k you could use --private-key=<absolute_path_to_ssh_private_key>_


### Example 10: Setup on an existing generic virtual machine :: Setup Jenkins with metrics enabled

 1. Prepare an existing generic centos7/fedora27+ VM with VM_IP as a USER with paswordless sudo privileges
 2. Install on an existing VM as a USER, enable nested virtualization
 3. Start minishift cluster with profile minishift
 4. Run Jenkins with metrics enabled
 5. Load containers from a user defined as project_repo from joejstuart/contra-demo
 6. Load helper containers from CentOS-PaaS-SIG/contra-env-infra
 7. Setup Jenkins with a a job DSL seed job and sample jobs from CentOS-PaaS-SIG/contra-env-sample-project
 8. Disable the linchpin-executor container

```
ansible-playbook -vv -i "VM_IP," -u USER contra-env-setup/playbooks/prepare_vm_for_minishift.yml \
    -e setup_nested_virt=true --private-key=PATH_TO_PRIVATE_KEY

ansible-playbook -vv -i "localhost," contra-env-setup/playbooks/setup.yml \
    -e user=$USER \
    -e profile=minishift \
    -e minishift_external_vm_user=USER \
    -e minishift_external_vm_ssh_key_location=PATH_TO_PRIVATE_KEY \
    -e minishift_external_vm_ip=VM_IP \
    -e run_prereqs=false \
    -e setup_minishift=true \
    -e start_minishift=true \
    -e setup_containers=true \
    -e helper_project_repo=https://github.com/CentOS-PaaS-SIG/contra-env-infra \
    -e helper_project_branch=master \
    --extra-vars='{"os_template_blacklist": ["linchpin-executor", "ansible-executor"]}' \
    -e project_repo=https://github.com/joejstuart/contra-demo \
    -e project_branch=master \
    -e jenkins_enable_metrics=true \
    -e jenkins_dsl_job_repo=CentOS-PaaS-SIG/contra-env-sample-project -K -k
```

## Mac Users

In order to run this setup when using a mac, a few other steps must be taken.
* When running the `setup.yml` add `--connection=local` to end of command

Example:
```
    ansible-playbook -vv -i "localhost," playbooks/setup.yml \
    -e user=$USER -e setup_pipelines=true \
    -e setup_sample_project=true -K -k --connection=local
```

## Debugging Issues

### Issue #1: Can't push images to the Minishift cluster

This issue reveals itself as not being able to pull images from the docker registry.  This is because your minishift VM can't reach outside addresses.

Pinpointing if you are hitting this issue:
1. In the output of the following task:
```    
    TASK [minishift : Initialization of minishift cluster with profile minishiftpipeline]
```
2.  Task contains:
```
    Pinging 8.8.8.8 ... FAIL
```

3. Full example output: http://pastebin.centos.org/620286/

#### Solution #1:

Make sure you can ping outside addresses from within the minishift vm.  

1. Test pinging an outside address from the minishift VM

```
    minishift ssh
    ping www.google.com
```

If the above fails try switching network connection being used from wireless to wired or checking the firewall on that network if it is blocking the traffic
