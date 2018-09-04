# Changelog

## v1.2.1 (03/09/2018)
- use github api [#75](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/75)
- Support the case where project does not contain a display name [#73](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/73)
- Log and cleanup failed builds [#65](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/65)
- Fix backslash escaping for failed build cleanup filters [#60](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/60)
- Fix the query command for the minishift and oc compressed binaries [#69](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/69)
- CI for contra-env-setup [#71](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/71)
- Bump version of OpenShift from 3.9 to 3.10 [#70](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/70)
- Remove duplicated pkg install [#68](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/68)
- Create new minishift profile in case it was never created before [#67](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/67)
- Adjust indent on when to align [#66](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/66)
- Changed README and going to use package instead of yum and dnf [#64](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/64)
- Revert change of using package [#63](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/63)
- Change from using yum or dnf to use package [#62](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/62)
- Add missing reference to user for kvm setup [#61](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/61)

---

## v1.2.0 (29/06/2018)
- Build container images in parallel [#59](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/59)
- Updated versions of minishift and minishift.iso [#57](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/57)

---

## v1.1.7 (21/06/2018)
- use Running to detect queued [#56](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/56)

---

## v1.1.6 (20/06/2018)
- Detect New state when querying for queued build [#55](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/55)
- Allow to set insecure registry with minishift [#52](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/52)
- Added option to disable loading of the helper containers [#51](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/51)

---

## v1.1.5 (14/06/2018)
- Skip non template yaml files when setting up containers [#50](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/50)
-  Rework importing of os templates [#49](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/49)

---

## v1.1.4 (06/06/2018)
- Fixed type-o of option [#47](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/47)

---

## v1.1.3 (31/05/2018)
- Load helper containers and add start_minishift option [#44](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/44)

---

## v1.1.2 (30/05/2018)
- Use longer version for imagestream [#42](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/42)

---

## v1.1.1 (23/05/2018)
- Add the ability to specify adhoc oc commands [#40](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/40)

---

## v1.1.0 (18/05/2018)
- Allow setting of Project Display Name [#38](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/38)

---

## v1.0.1 (14/05/2018)
- Increase default version of OpenShift and up memory to 8092 [#36](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/36)

---

## v1.0.0 (10/05/2018)
- Support use case when not using minishift [#35](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/35)
- add support for setting # of cpus [#34](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/34)
- fixing some issues from ansible-lint in setup_pipelines.yml [#31](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/31)
- Add ability to use ansible variables in s2i templates [#32](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/32)
-  Change to use oc and minishift binaries full path [#30](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/30)
- Correct memory parameter name [#29](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/29)
- [**bug**][**enhancement**] support for running tests on centos 7 [v2] [#28](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/28)
-  Updated README and changing options [#26](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/26)
- Setup pipelines through OpenShift buildconfig templates  [#25](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/25)
- [**enhancement**] Some improvements in the test automation [v2] [#22](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/22)
-  Update README and fix pipeline template destination [#24](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/24)
- Setup sample_os_templates and sample_pipelines [#23](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/23)
- [**enhancement**] Improved the test automation [#19](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/19)
- Add http.sslVerify false for git and fix loading templates [#18](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/18)
- Change to compare filename to scc name [#17](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/17)
- Update README [#16](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/16)
- contra-env-setup stability [#15](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/15)
- fixed warning about deprecated 'include' [#5](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/5)
- Updated README with a better heading [#3](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/3)
- Added logo [#2](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/2)
- Initial commit to setup the repo [#1](https://github.com/CentOS-PaaS-SIG/contra-env-setup/pull/1)
