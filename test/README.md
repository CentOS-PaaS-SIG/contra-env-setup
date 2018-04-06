# contra-env-setup CI
This document describes how works the tests in the contra-env-setup repository.

## Avocado
We are using the avocado-framework to create and run our test of integrity in contra-env-setup. 

### How to install
Into the directory, `test/` have the file `requirements.txt` file to define what version we are using in our tests.

```
$ git clone https://github.com/CentOS-PaaS-SIG/contra-env-setup.git
$ cd contra-env-setup/test/
$ pip install -r requirements.txt --user
```

**NOTE** this version have support to `qemu-img` that is necessary to our tests.

Should install the packages are requirements:
```
$ sudo dnf install ansible libvirt-client qemu qemu-img genisoimage python2-aexpect virt-install
```

## Tests
To orchestrate the test we need use the parameter file to define the global variables and combinations in the test process:

[test_contra_env_setup.yaml:](test_contra_env_setup.yaml)
```
repo: https://github.com/CentOS-PaaS-SIG/contra-env-setup.git
branch: master

distros: !mux
    fedora:
        distro: Fedora
    centos:
        distro: CentOS
```

The steps included in the test will use the parameter file with the file [test_contra_env_setup.py:](test_contra_env_setup.py) that have included all steps that will be tested.

### Running the test
After all requirements are installed in your environment can run the testing using this command, for example:
```
$ avocado run test_contra_env_setup.py -m test_contra_env_setup.yaml
JOB ID     : d7fde860704f1644b44e59587049cf090d2b1458
JOB LOG    : /home/firemanxbr/avocado/job-results/job-2018-03-21T11.30-d7fde86/job.log
 (1/1) test_contra_env_setup.py:TestMinishift.test;fedora-2e56: PASS (633.73 s)
RESULTS    : PASS 1 | ERROR 0 | FAIL 0 | SKIP 0 | WARN 0 | INTERRUPT 0 | CANCEL 0
JOB TIME   : 633.85 s
```

## References
[Avocado Framework](http://avocado-framework.github.io)

[Avocado QEMU](https://github.com/apahim/avocado_qemu/)
