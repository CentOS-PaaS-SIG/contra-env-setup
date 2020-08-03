# Automate Provisioning OpenStack Instance 

- The Ansible playbook will automate the creation of an openstack instance.
- The playbook contains the neccessary parameters to create the instance. 
- The parameters include: image, key_name, flavor, network, and security_groups
- The parameters image, flavor, network, and security groups must be passed in the command line as extra-vars when running the playbook.

### Steps to Create the OS Instance
1. Run the following commands to set up the OpenStack credentials:  
**export OS_AUTH_URL= < url-to-openstack-identity > #you can get this url from OS VM  
export OS_PROJECT_NAME= < project-name >   
export OS_USER_DOMAIN_NAME= < domain-name > *# (optional)*  
export OS_PROJECT_DOMAIN_ID= < domain-ID > *# (optional)*  
export OS_USERNAME= < user-name >  
export OS_PASSWORD= < password >  # *(optional)***  

2. Run the playbook with the following command and provide the parameters as extra-vars:   
**ansible-playbook -vv -i "localhost," --connection=local provision_openstack_instance.yml -e "vm_name=< give a name for the VM > image=< image name > flavor=< flavor name > network=< network name > sec_groups= < security groups name >"** 