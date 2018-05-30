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
  - [Templates](#templates)
  - [Usage examples](#usage-examples)
    - [Example 1: Setup on a local machine :: Setup Minishift + OS templates](#example-1-setup-on-a-local-machine--setup-minishift--os-templates)
    - [Example 2: Setup on a local machine :: Setup Minishift + OS templates + Jenkins 2.0 pipelines](#example-2-setup-on-a-local-machine--setup-minishift--os-templates--jenkins-20-pipelines)
    - [Example 3: Setup on a local machine :: Setup Minishift + OS templates + Jenkins 2.0 pipelines](#example-3-setup-on-a-local-machine--setup-minishift--os-templates--jenkins-20-pipelines)
    - [Example 4: Setup on a local machine :: Start Minishift w/profile mysetup + OS templates + Jenkins 2.0 pipelines](#example-4-setup-on-a-local-machine--start-minishift-wprofile-mysetup--os-templates--jenkins-20-pipelines)
  - [Debugging Issues](#debugging-issues)
    - [Issue #1: Can't push images to the Minishift cluster](#issue-1-cant-push-images-to-the-minishift-cluster)
      - [Solution #1:](#solution-1)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->
![CI-Pipeline](continuous-infra-logo.png "continuous-infra")
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
```
contra-env-setup/playbooks/group_vars/all/global.yml

```
## Pre-Setup options

* run_cleanup: Run clean up of previous setup : default=false
* run_prereqs: Run setting up virtualization and kvm-driver : default=true
* contra_env_setup_dir: Directory to store the contra-env-setup :  default "{{ ansible_env.HOME }}/.contra-env-setup

## Override options

* force_minishift_install: Override an existing install of minishift : default=false
* force_repo_clone: Force cloning of project repo

## Minishift and OpenShift setup options

### Minishift setup options
* setup_minishift: Setup a minishift cluster : default=true
* minishift_version: Minishift version to use : default=v1.12.0
* minishift_dest_dir: Minishift binary and ISO directory : default={{ contra_env_setup_dir }}/minishift
* profile: Minishift profile : default=minishift
* disk_size: Disk size to use for minishift : default=40gb
* memory: Memory size to use for the VM : default=6400mb
* cpus: Number of cpus to use for minishift VM: default=2
* minishift_iso: ISO image to use : default=http://artifacts.ci.centos.org/fedora-atomic/minishift/iso/minishift.iso 

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
* sample_os_template_dir: Relative directory in the sample project repo where OpenShift s2i templates are stored: default=config/s2i

### Jenkins 2.0 pipeline setup options
* setup_pipelines: Setup Jenkins 2.0 pipelines : default=false
* pipeline_dir: Relative directory in the project repo where Jenkins pipelines are stored: default=config/pipelines/buildconfigs
* sample_pipeline_dir: Relative directory in the sample project repo where Jenkins pipelines are stored: default=config/pipelines/buildconfigs

## Templates

Note that it is possible to use {{ ansible_vars }} in your Openshift Templates.

## Usage examples

### Example 1: Setup on a local machine :: Setup Minishift + OS templates 

 1. Install on a local machine as user cloud-user.
 2. Setup pre-reqs (kvm driver and nested virtualization)
 3. Setup a minishift cluster
 4. Setup OpenShift s2i templates from the -e project_repo=https://github.com/arilivigni/ci-pipeline
    1. Override the project_repo with another one then the default in global.yml
    2. OpenShift project -e openshift_project=ari-ci-pipeline  
 5. Modify my container tags with the default tag. tag=stable
 
```
    ansible-playbook -vv -i "localhost," contra-env-setup/playbooks/setup.yml \
    -e user=cloud-user -e project_repo=https://github.com/arilivigni/ci-pipeline 
    -e openshift_project=ari-ci-pipeline -K -k

```
_Note: The -K is used to prompt you for your password for sudo (if you require one) <br>
       The -k is used to prompt you for your ssh password can hit enter if using -K and they are the same<br>
       Instead of -k you could use --private-key=<absolute_path_to_ssh_private_key>_

### Example 2: Setup on a local machine :: Setup Minishift + OS templates + Jenkins 2.0 pipelines

 1. Install on a local machine as user cloud-user.
 2. Setup pre-reqs (kvm driver and nested virtualization)
 3. Setup a minishift cluster
 4. Setup OpenShift s2i templates from the -e project_repo=https://github.com/arilivigni/ci-pipeline
    1. Override the project_repo with another one then the default in global.yml
    2. OpenShift project -e openshift_project=ari-ci-pipeline  
 5. Modify my container tags with the default tag. tag=stable
 6. Setup Jenkins 2.0 pipelines from the project_repo=https://github.com/arilivigni/ci-pipeline
 
```
    ansible-playbook -vv -i "localhost," contra-env-setup/playbooks/setup.yml \
    -e user=cloud-user -e project_repo=https://github.com/arilivigni/ci-pipeline \
    -e openshift_project=ari-ci-pipeline -e setup_pipelines=true -K -k

```
_Note: The -K is used to prompt you for your password for sudo (if you require one) <br>
       The -k is used to prompt you for your ssh password can hit enter if using -K and they are the same<br>
       Instead of -k you could use --private-key=<absolute_path_to_ssh_private_key>_
       
### Example 3: Setup on a local machine :: Setup Minishift + OS templates + Jenkins 2.0 pipelines

 1. Install on a local machine as user cloud-user.
 2. Setup pre-reqs (kvm driver and nested virtualization)
 3. Setup a minishift cluster
 4. Setup OpenShift s2i templates from the -e project_repo=https://github.com/arilivigni/ci-pipeline
    1. Override the project_repo with another one then the default in global.yml
    2. OpenShift project -e openshift_project=ari-ci-pipeline 
 5. Modify my container tags with the tag=develop
 6. Setup Jenkins 2.0 pipelines from the project_repo=https://github.com/arilivigni/ci-pipeline
 7. Setup sample project templates and pipelines 
    from the project_repo=https://github.com/CentOS-PaaS-SIG/contra-env-sample-project

 
```
    ansible-playbook -vv -i "localhost," contra-env-setup/playbooks/setup.yml \
    -e user=cloud-user -e project_repo=https://github.com/arilivigni/ci-pipeline \
    -e openshift_project=ari-ci-pipeline -e tag=develop -e setup_pipelines=true \
    -e setup_sample_project -K -k

```
_Note: The -K is used to prompt you for your password for sudo (if you require one) <br>
       The -k is used to prompt you for your ssh password can hit enter if using -K and they are the same<br>
       Instead of -k you could use --private-key=<absolute_path_to_ssh_private_key>_

### Example 4: Setup on a local machine :: Start Minishift w/profile mysetup + OS templates + Jenkins 2.0 pipelines

 1. Install on a local machine as user cloud-user.
 2. Setup pre-reqs (kvm driver and nested virtualization)
 3. Start minishift cluster with profile mysetup
 4. Setup OpenShift s2i templates from the -e project_repo=https://github.com/arilivigni/ci-pipeline
    1. Override the project_repo with another one then the default in global.yml
    2. OpenShift project -e openshift_project=ari-ci-pipeline 
 5. Modify my container tags with the tag=develop
 6. Setup Jenkins 2.0 pipelines from the project_repo=https://github.com/arilivigni/ci-pipeline
 7. Setup sample project templates and pipelines 
    from the project_repo=https://github.com/CentOS-PaaS-SIG/contra-env-sample-project

 
```
    ansible-playbook -vv -i "localhost," contra-env-setup/playbooks/setup.yml \
    -e user=cloud-user -e project_repo=https://github.com/arilivigni/ci-pipeline \
    -e openshift_project=ari-ci-pipeline -e tag=develop -e setup_pipelines=true \
    -e setup_sample_project -e start_minishift=true -e profile=mysetup -K -k

```
_Note: The -K is used to prompt you for your password for sudo (if you require one) <br>
       The -k is used to prompt you for your ssh password can hit enter if using -K and they are the same<br>
       Instead of -k you could use --private-key=<absolute_path_to_ssh_private_key>_

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
