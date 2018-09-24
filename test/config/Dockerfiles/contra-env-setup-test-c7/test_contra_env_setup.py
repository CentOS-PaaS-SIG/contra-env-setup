#!/usr/bin/python

import pytest
import json
import requests
import os.path
from subprocess import check_output
from requests.packages.urllib3.exceptions import InsecureRequestWarning


@pytest.fixture
def run_info():
    playbook_id = None
    profile = None
    minishift_bin = None
    oc_bin = None
    
    # Get Playbook ID from ara
    playbook_list_cmd = '/usr/bin/ara playbook list -f json'
    playbook_list = json.loads(check_output(playbook_list_cmd.split()))

    for playbook in playbook_list:
        if 'contra-env-setup' in playbook.get('Path'):
            playbook_id = playbook.get('ID')

    # Get list of all playbook tasks from ara
    result_list_cmd = '/usr/bin/ara result list -b %s -f json' % playbook_id
    result_list = json.loads(check_output(result_list_cmd.split()))

    # Get profile, Minishift binary and oc binary from the debug playbook step
    debug_result_id = None

    for result in result_list:
        if result.get('Name') == 'playbook_hooks : debug-vars':
            debug_result_id = result.get('ID')
            break
    
    if debug_result_id is not None:
        debug_result_cmd = '/usr/bin/ara result show %s --raw -f json' % debug_result_id
        debug_result = json.loads(check_output(debug_result_cmd.split()))
        if debug_result.get('Result'):
            test_run_info = debug_result.get('Result').get('test_run_info')
            profile = test_run_info.get('profile')
            minishift_bin = test_run_info.get('minishift_bin')
            oc_bin = test_run_info.get('oc_bin')

    return {
               'playbook_id': playbook_id,
               'profile': profile,
               'minishift_bin': minishift_bin,
               'oc_bin': oc_bin,
           }


def test_playbook_success(run_info):
    playbook_id = run_info.get('playbook_id')
    tasks_skipped = None
    tasks_ok = None
    tasks_changed = None
    tasks_failed = None

    assert(playbook_id is not None)

    # Get stats for the playbook run
    stats_list_cmd = '/usr/bin/ara stats list -f json'
    stats_list = json.loads(check_output(stats_list_cmd.split()))

    for stats in stats_list:
        if 'contra-env-setup' in stats.get('Playbook') and 'localhost' == stats.get('Host'):
            tasks_skipped = stats.get('Skipped')
            tasks_ok = stats.get('Ok')
            tasks_changed = stats.get('Changed')
            tasks_failed = stats.get('Failed')
    
    assert(tasks_failed == 0)
    assert(tasks_changed > 0)
    assert(tasks_ok > 0)


def test_binary_locations(run_info):
    minishift_bin = run_info.get('minishift_bin')
    oc_bin = run_info.get('oc_bin')
 
    assert(minishift_bin is not None)
    assert(os.path.isfile(minishift_bin))
    assert(oc_bin is not None)
    assert(os.path.isfile(oc_bin))


def test_minishift_profile(run_info):
    minishift_bin = run_info.get('minishift_bin')
    profile = run_info.get('profile')

    minishift_success = False

    if minishift_bin is not None:
        minishift_cmd = '%s profile list' % minishift_bin
        minishift_result = check_output(minishift_cmd.split())

        for line in minishift_result.splitlines():
            if '- %s' % profile in line and 'Running' in line:
                minishift_success = True

    assert(minishift_success)


def test_buildconfigs(run_info):
    oc_bin = run_info.get('oc_bin')
    oc_result = None

    if oc_bin is not None:
        oc_cmd = '%s get buildconfigs' % oc_bin
        oc_result = check_output(oc_cmd.split())

    assert(oc_result and 'jenkins-contra-sample-project-slave' in oc_result)
    assert(oc_result and 'jenkins ' in oc_result)


def test_builds(run_info):
    oc_bin = run_info.get('oc_bin')
    jenkins_success = False
    jenkins_contra_slave_success = False

    if oc_bin is not None:
        oc_cmd = '%s get builds' % oc_bin
        oc_result = check_output(oc_cmd.split())
        for line in oc_result.splitlines():
            if 'jenkins-' in line and 'Complete' in line and 'slave' not in line:
                jenkins_success = True
            if 'jenkins-contra-sample-project-slave-' in line and 'Complete' in line:
                jenkins_contra_slave_success = True

    assert(jenkins_success)
    assert(jenkins_contra_slave_success)


def test_imagestreams(run_info):
    oc_bin = run_info.get('oc_bin')
    oc_result = None

    if oc_bin is not None:
        oc_cmd = '%s get imagestreams' % oc_bin
        oc_result = check_output(oc_cmd.split())

    assert(oc_result and 'jenkins-contra-sample-project-slave' in oc_result)
    assert(oc_result and 'jenkins' in oc_result)


def test_services(run_info):
    oc_bin = run_info.get('oc_bin')
    oc_result = None

    if oc_bin is not None:
        oc_cmd = '%s get services' % oc_bin
        oc_result = check_output(oc_cmd.split())

    assert(oc_result and 'jenkins ' in oc_result)
    assert(oc_result and 'jenkins-jnlp' in oc_result)


def test_jenkins_master_pod(run_info):
    oc_bin = run_info.get('oc_bin')
    jenkins_master_pod_running = False

    if oc_bin is not None:
        oc_cmd = '%s get pods' % oc_bin
        oc_result = check_output(oc_cmd.split())

        for line in oc_result.splitlines():
            if 'jenkins' in line and 'Running' in line:
                jenkins_master_pod_running = True

    assert(jenkins_master_pod_running)

def test_jenkins_running(run_info):
    oc_bin = run_info.get('oc_bin')
    route_exists = False
    jenkins_running = False

    if oc_bin is not None:
        oc_cmd = '%s get routes' % oc_bin
        oc_result = check_output(oc_cmd.split())

        route_exists = True if ('jenkins' in oc_result) else False

        jenkins_running = False
        for line in oc_result.splitlines():
            if 'jenkins' in line:
                route = line.split()[1]
                requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
                request = requests.get('https://%s/login' % route, verify=False)
                jenkins_running = True if request.status_code == 200 else False

    assert(route_exists)
    assert(jenkins_running)

