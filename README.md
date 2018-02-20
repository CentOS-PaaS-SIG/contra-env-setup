# contra-env-setup
This repository provides a tool to automate the deploy of your Jenkins Pipeline locally or in OpenShift.


## Resources
This repository is the starting point for a deploy from scratch. You can use this tool to configure locally:

* Configurations for Fedora 27 or higher to support minishift with kvm and nested. (prereqs)
* Installation and configuration of Minishift. (minishift)
* Clone your image, configurations, plugins and slaves from your Jenkins (pipeline).

**NOTE** In this last step we strongly recommend the use of the image provided, tested and certified by the Openshift project: https://github.com/openshift/jenkins


## locally
You can run contra-env-setup after installing Ansible on your Fedora 27 or higher. Examples of use:


### Prerequisites + Minisihft + Clone Jenkins Pipeline
`$ ansible-playbook -i" localhost, "setup.yml`


### Skip all requirements preparation
`$ ansible-playbook -i" localhost, "setup.yml -e skip_prereqs = true`


### Options for Minishift
`$ ansible-playbook -i" localhost, "setup.yml -e skip_minishift = true`

`$ ansible-playbook -i" localhost, "setup.yml -e install_minishift = true`

`$ ansible-playbook -i" localhost, "setup.yml -e start_minishift = true`

`$ ansible-playbook -i" localhost, "setup.yml -e stop_minishift = true`


### Options for Jenkins Pipeline
`$ ansible-playbook -i" localhost, "setup.yml -e skip_pipeline = true`

**NOTE** For more variables see `group_vars/all/global.yml`
