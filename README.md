# Contra Environment Setup
![CI-Pipeline](continuous-infra-logo.png)

## Goal of this repository
This tool is normally used locally to create an environment with Minishift and Helm.
It use Ansible to download, install and configure all requirements to this environment. All users will have the same structure basic to install, test and improve your CI/CD Pipelines.

Components used in this deployment:
* [Minishift CentOS ISO](https://github.com/CentOS-PaaS-SIG/minishift-centos-iso)
* [Minishift](https://github.com/minishift/minishift)
* [Helm](https://github.com/kubernetes/helm)
* [Minishift Addons Helm](https://github.com/minishift/minishift-addons/tree/master/add-ons/helm)

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
│   │   │       ├── helm.yml
│   │   │       ├── main.yml
│   │   │       └── minishift.yml
│   │   ├── clean
│   │   │   └── tasks
│   │   │       ├── clean.yml
│   │   │       └── main.yml
│   │   ├── helm
│   │   │   └── tasks
│   │   │       ├── main.yml
│   │   │       └── setup_helm.yml
│   │   ├── minishift
│   │   │   └── tasks
│   │   │       ├── init_minishift.yml
│   │   │       ├── main.yml
│   │   │       └── setup_minishift.yml
│   │   └── prereqs
│   │       └── tasks
│   │           ├── install_kvm_plugin.yml
│   │           ├── install_virtual_reqs.yml
│   │           ├── main.yml
│   │           └── setup_nested_virt.yml
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
or only certain components. ex. `clean`, `prereqs`, `artifacts`, `minishift`, and `helm`.

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
* skip_helm: Skip helm will configure and start : default=false
_______

### All Variables

| Variable Name                  | Description                                                             | Example                                            | Default                                   | Required |
|:------------------------------:|:-----------------------------------------------------------------------:|:--------------------------------------------------:|:-----------------------------------------:|:--------:|
| skip_clean                     |     Skip clean up all previous or old deployments                       | skip_clean=true                                    |   false                                   | No       |
| skip_prereqs                   |     Skip setting up virtualization and kvm-driver                       | skip_prereqs=true                                  |   false                                   | No       |
| skip_artifacts                 |     Skip artifacts will download, extract and copy all requirements     | skip_artifacts=true                                |   false                                   | No       |
| skip_minishift                 |     Skip minishift will configure and start the local cluster           | skip_minishift=true                                |   false                                   | No       |
| skip_helm                      |     Skip helm will configure and start                                  | skip_helm=true                                     |   false                                   | No       |
| remote_user                    |     Define your local username to interact with libvirt                 | remote_user=username                               |   check global.yml                        | No       |
| kvm_plugin_url                 |     URL of the kvm plugin to install                                    | kvm_plugin_url=[url]                               |   check global.yml                        | No       |
| minishift_dest_dir             |     Directory to store minishift binary & helm binary & ISO             | minishift_dest_dir=/home/cloud-user/test           |   "{{ ansible_env.HOME }}/minishift"      | No       |
| minishift_release              |     Release used of minishift                                           | minishift_release="1.14.0"                         |   check global.yml                        | No       |
| minishift_url                  |     URL of the minishift to install                                     | minishift_url=[url]                                |   check global.yml                        | No       |
| minishift_iso                  |     URL of minishift centos ISO to download                             | minishift_iso=[url]                                |   check global.yml                        | No       |
| profile                        |     Profile of minishift for start a new cluster                        | profile=minishift                                  |   minishift                               | No       |
| disk_size                      |     Disk size used for minishift cluster                                | disk_size=20gb                                     |   disk_size=40gb                          | No       |
| memory                         |     Memory used for minishift cluster                                   | memory=4096mb                                      |   memory=6400mb                           | No       |
| helm_release                   |     Release used of helm                                                | helm_release=2.8.1                                 |   helm_release=2.8.1                      | No       |
| helm_url                       |     URL of the helm to install                                          | helm_url=[url]                                     |   check global.yml                        | No       |

## Using Helm
To deploy your Chart into minishift/openshift using helm you can use some strategies.

### Chart
The Charts are packages and templates to yaml files creating better management your deployments in kubernetes to a high level. However OpenShift/Minishift extended the Kubernetes. In this case every Charts do you find outsite of Openshift world don't will works because you need adjust the caracteriscts of OpenShift into your yaml files.

### 1 - Repository
Helm have a repositories like rpm packages. For check which repositories are added in your tiller server:

```
$ helm repo list
NAME    URL
stable  https://kubernetes-charts.storage.googleapis.com
local   http://127.0.0.1:8879/charts
```

To add a new repository with your Charts:
```
$ helm repo add name-of-repository https://url
```

To add a Chart from a repository:
```
$ helm install name-of-repository/chart-name
```

### 2 - Packaged chart
This strategy to install a Chart packaged chart from any url, for example:
```
# helm install https://example.com/charts/nginx-1.2.3.tgz
```

### 3 - Unpacked chart
This strategy to install an unpacked chart locally in your filesystem:
```
$ helm install ./nginx
```

**NOTE** The `./nginx/` is a directory with your Chart files unpacked


## TL;DR Helm
Installing a new Chart locally:
```
$ helm install ./mongodb
NAME:   crazy-rabbit
LAST DEPLOYED: Wed Mar  7 13:37:14 2018
NAMESPACE: myproject
STATUS: DEPLOYED

RESOURCES:
==> v1/Secret
NAME                  TYPE    DATA  AGE
crazy-rabbit-mongodb  Opaque  2     1s

==> v1/PersistentVolumeClaim
NAME                  STATUS  VOLUME  CAPACITY  ACCESS MODES  STORAGECLASS  AGE
crazy-rabbit-mongodb  Bound   pv0039  100Gi     RWO,ROX,RWX   1s

==> v1/Service
NAME                  TYPE       CLUSTER-IP      EXTERNAL-IP  PORT(S)    AGE
crazy-rabbit-mongodb  ClusterIP  172.30.110.206  <none>       27017/TCP  1s

==> v1beta1/Deployment
NAME                  DESIRED  CURRENT  UP-TO-DATE  AVAILABLE  AGE
crazy-rabbit-mongodb  1        0        0           0          1s

==> v1/Pod(related)
NAME                                   READY  STATUS             RESTARTS  AGE
crazy-rabbit-mongodb-1788736808-d9mzl  0/1    ContainerCreating  0         1s


NOTES:
MongoDB can be accessed via port 27017 on the following DNS name from within your cluster:
crazy-rabbit-mongodb.myproject.svc.cluster.local

To connect to your database run the following command:

   kubectl run crazy-rabbit-mongodb-client --rm --tty -i --image bitnami/mongodb --command -- mongo --host crazy-rabbit-mongodb
```

Checking the status of deployment:
```
$ helm ls 
NAME            REVISION        UPDATED                         STATUS          CHART           NAMESPACE
crazy-rabbit    1               Wed Mar  7 13:37:14 2018        DEPLOYED        mongodb-0.4.26  myproject
```

Deleting the chart:
```
$ helm delete crazy-rabbit
crazy-rabbit
```
