# Contra-env-setup testing containers

The following containers are used for testing contra-env-setup in a variety of environments

## Centos7 testing container

The contra-env-setup-test-c7 container image is used for testing contra-env-setup on a centos7 based system.
The testing consists of a prepare-and-test.sh script which does the following:

- sets up the environment (prepares Ara, clones the repository and fetches the desired PR)
- runs the contra-env-setup playbook for the sample project with the included playbook hook which outputs some debug variables necessary for testing
- runs pytest on the test_contra_env_setup.py which tests the results of the playbook run
- saves the test logs for later archiving

### Tests

The test_contra_env_setup.py tests the following:

- results of the playbook run (did the playbook run succesfuly, did any tasks run etc.)
- if the installed binaries are in place (minishift and oc)
- if the minishift profile is created and active
- if key openshift buildconfigs, builds, imagestreams and services exist
- if the jenkins master pod is running
- the route to the jenkins master instance and if the login page is active