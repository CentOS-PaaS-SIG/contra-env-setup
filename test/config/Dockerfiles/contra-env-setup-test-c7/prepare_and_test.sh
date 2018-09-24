#!/bin/bash

base_dir=/home

# Set log dir to the WORKSPACE where it can be archived
if [ ! -z "${WORKSPACE}" ]; then
    log_dir=${WORKSPACE}
else
    log_dir=${base_dir}/logs
fi

# Set environment to use ara with ansible
export ara_location=$(python -c "import os,ara; print(os.path.dirname(ara.__file__))")
export ANSIBLE_CALLBACK_PLUGINS=$ara_location/plugins/callbacks
export ANSIBLE_ACTION_PLUGINS=$ara_location/plugins/actions
export ANSIBLE_LIBRARY=$ara_location/plugins/modules

export USER=$(whoami)

cd ${base_dir}

# Prepare repo and logs directories
mkdir -p ${log_dir}

git clone https://github.com/CentOS-PaaS-SIG/contra-env-setup.git

pushd ${PROJECT_REPO}

# Sync the repository
if [ -z ${PR_NUM} ]; then
  git fetch origin ${ACTUAL_COMMIT}
  git checkout FETCH_HEAD
else
  # PR was specified so we need to fetch it
  git fetch origin pull/${PR_NUM}/head:local-testing-branch
  git checkout local-testing-branch
fi

popd

# Run the playbook locally with added hook for debugging variables needed for testing
/usr/bin/ansible-playbook -vv -i "localhost," ${base_dir}/contra-env-setup/playbooks/setup.yml -e user=root \
                          -e ansible_connection=local -e setup_nested_virt=false -e setup_playbook_hooks=true \
                          --extra-vars='{"hooks": ["/home/debug_vars.yml"], "os_template_whitelist": ["jenkins-persistent", "jenkins-contra-sample-project-slave-builder"]}'

# Run tests with pytest
python -m pytest ${base_dir}/test_contra_env_setup.py -v --junitxml=${log_dir}/contra_env_setup_centos7.xml > ${log_dir}/contra_env_setup_centos7.log
