/**
 * Contra env-setup Pipeline with trigger
 *
 * This is a scripted pipeline for the contra-env-setup Pipeline
 *
 */

timestamps {
    env.ghprbGhRepository = env.ghprbGhRepository ?: 'CentOS-PaaS-SIG/contra-env-setup'
    env.ghprbActualCommit = env.ghprbActualCommit ?: 'master'
    env.ghprbPullAuthorLogin = env.ghprbPullAuthorLogin ?: ''
    env.ghprbPullId = env.ghprbPullId ?: ''

    // Needed for podTemplate()
    env.SLAVE_TAG = env.SLAVE_TAG ?: 'stable'
    env.ENVSETUPTEST_C7_TAG = env.ENVSETUPTEST_C7_TAG ?: 'stable'
    env.ENVSETUPTEST_F28_TAG = env.ENVSETUPTEST_F28_TAG ?: 'stable'

    env.DOCKER_REPO_URL = env.DOCKER_REPO_URL ?: '172.30.254.79:5000'
    env.OPENSHIFT_NAMESPACE = env.OPENSHIFT_NAMESPACE ?: 'continuous-infra'
    env.OPENSHIFT_SERVICE_ACCOUNT = env.OPENSHIFT_SERVICE_ACCOUNT ?: 'jenkins'

    // Execution ID for this run of the pipeline
    executionID = UUID.randomUUID().toString()

    // Pod name to use
    podName = 'contra-env-setup-' + executionID

    // Get upstream libraries

    def libraries = ['cico-pipeline'           : ['master', 'https://github.com/CentOS/cico-pipeline-library.git'],
                     'ci-pipeline'             : ['master', 'https://github.com/CentOS-PaaS-SIG/ci-pipeline.git']]

    libraries.each { name, repo ->
        library identifier: "${name}@${repo[0]}",
                retriever: modernSCM([$class: 'GitSCMSource',
                                      remote: repo[1]])
    }

    library identifier: "contra-env-setup@${env.ghprbActualCommit}",
            retriever: modernSCM([$class: 'GitSCMSource',
                                  remote: "https://github.com/${env.ghprbGhRepository}.git",
                                  traits: [[$class: 'jenkins.plugins.git.traits.BranchDiscoveryTrait'],
                                           [$class: 'RefSpecsSCMSourceTrait',
                                            templates: [[value: '+refs/heads/*:refs/remotes/@{remote}/*'],
                                                        [value: '+refs/pull/*:refs/remotes/origin/pr/*']]]]])

    properties(
            [
                    buildDiscarder(logRotator(artifactDaysToKeepStr: '', artifactNumToKeepStr: '50', daysToKeepStr: '', numToKeepStr: '50')),
                    [$class: 'GithubProjectProperty', displayName: '', projectUrlStr: 'https://github.com/CentOS-PaaS-SIG/contra-env-setup/'],
                    [$class: 'org.jenkinsci.plugins.workflow.job.properties.PipelineTriggersJobProperty', triggers:[
                            [
                                    $class: 'org.jenkinsci.plugins.ghprb.GhprbTrigger',
                                    orgslist: 'CentOS-PaaS-SIG',
                                    cron: 'H/5 * * * *',
                                    triggerPhrase: '.*\\[test\\].*',
                                    onlyTriggerPhrase: false,
                                    useGitHubHooks: true,
                                    permitAll: true,
                                    autoCloseFailedPullRequests: false,
                                    displayBuildErrorsOnDownstreamBuilds: true,
                                    extensions: [
                                            [
                                                    $class: 'org.jenkinsci.plugins.ghprb.extensions.status.GhprbSimpleStatus',
                                                    commitStatusContext: 'Contra Env Setup Testing Job',
                                                    showMatrixStatus: false,
                                                    triggeredStatus: 'Starting job...',
                                                    startedStatus: 'Testing...',
                                            ]
                                    ]
                            ]
                    ]],
                    parameters(
                            [
                                    string(name: 'PROJECT_REPO',
                                            defaultValue: 'contra-env-setup',
                                            description: 'Main project repo'),
                                    string(name: 'ghprbActualCommit',
                                            defaultValue: 'master',
                                            description: 'The GitHub pull request commit'),
                                    string(name: 'ghprbGhRepository',
                                            defaultValue: '',
                                            description: 'The repo the PR is against'),
                                    string(name: 'sha1',
                                            defaultValue: '',
                                            description: ''),
                                    string(name: 'ghprbPullId',
                                            defaultValue: '',
                                            description: 'Pull Request Number'),
                                    string(name: 'ghprbPullAuthorLogin',
                                            defaultValue: '',
                                            description: 'Pull Request Author username'),
                                    string(name: 'SLAVE_TAG',
                                            defaultValue: 'stable',
                                            description: 'Tag for slave image'),
                                    string(name: 'ENVSETUPTEST_C7_TAG',
                                            defaultValue: 'stable',
                                            description: 'Tag for contra-env-setup-test-c7 image'),
                                    string(name: 'ENVSETUPTEST_F28_TAG',
                                            defaultValue: 'stable',
                                            description: 'Tag for contra-env-setup-test-f28 image'),
                                    string(name: 'DOCKER_REPO_URL',
                                            defaultValue: '172.30.254.79:5000',
                                            description: 'Docker repo url for Openshift instance'),
                                    string(name: 'OPENSHIFT_NAMESPACE',
                                            defaultValue: 'continuous-infra',
                                            description: 'Project namespace for Openshift operations'),
                                    string(name: 'OPENSHIFT_SERVICE_ACCOUNT',
                                            defaultValue: 'jenkins',
                                            description: 'Service Account for Openshift operations')
                            ]
                    ),
            ]
    )
    podTemplate(name: podName,
            label: podName,
            cloud: 'openshift',
            serviceAccount: OPENSHIFT_SERVICE_ACCOUNT,
            idleMinutes: 0,
            namespace: OPENSHIFT_NAMESPACE,

            containers: [
                    // This adds the custom slave container to the pod. Must be first with name 'jnlp'
                    containerTemplate(name: 'jnlp',
                            image: DOCKER_REPO_URL + '/' + OPENSHIFT_NAMESPACE + '/jenkins-continuous-infra-slave:' + SLAVE_TAG,
                            ttyEnabled: false,
                            args: '${computer.jnlpmac} ${computer.name}',
                            command: '',
                            workingDir: '/workDir'),
                    // This adds the contra-env-setup-test-c7 container to the pod.
                    containerTemplate(name: 'contra-env-setup-test-c7',
                            alwaysPullImage: true,
                            image: DOCKER_REPO_URL + '/' + OPENSHIFT_NAMESPACE + '/contra-env-setup-test-c7:' + ENVSETUPTEST_C7_TAG,
                            ttyEnabled: true,
                            privileged: true,
                            workingDir: '/workDir'),
                    // This adds the contra-env-setup-test-f28 container to the pod.
                    containerTemplate(name: 'contra-env-setup-test-f28',
                            alwaysPullImage: true,
                            image: DOCKER_REPO_URL + '/' + OPENSHIFT_NAMESPACE + '/contra-env-setup-test-f28:' + ENVSETUPTEST_F28_TAG,
                            ttyEnabled: true,
                            privileged: true,
                            workingDir: '/workDir'),
            ],
            volumes: [emptyDirVolume(memory: false, mountPath: '/sys/class/net')])
            {
                node(podName) {

                    // pull in ciMetrics from ci-pipeline
                    ciMetrics.prefix = envsetupUtils.influxDBPrefix()
                    envsetupUtils.cimetrics = ciMetrics
                    def jobMeasurement = envsetupUtils.timedMeasurement()

                    def buildResult = null

                    timeout(time: 3, unit: 'HOURS') {

                        def currentStage = ""

                        envsetupUtils.ciPipeline {
                            // We need to set env.HOME because the openshift slave image
                            // forces this to /home/jenkins and then ~ expands to that
                            // even though id == "root"
                            // See https://github.com/openshift/jenkins/blob/master/slave-base/Dockerfile#L5
                            //
                            // Even the kubernetes plugin will create a pod with containers
                            // whose $HOME env var will be its workingDir
                            // See https://github.com/jenkinsci/kubernetes-plugin/blob/master/src/main/java/org/csanchez/jenkins/plugins/kubernetes/KubernetesLauncher.java#L311
                            //
                            env.HOME = "/root"
                            //
                            try {
                                // Prepare our environment
                                currentStage = "prepare-environment"
                                stage(currentStage) {

                                    envsetupUtils.timedPipelineStep('stepName': currentStage, 'debug': true) {

                                        deleteDir()
                                        // Set our default env variables
                                        envsetupUtils.setDefaultEnvVars()
                                        // Gather some info about the node we are running on for diagnostics
                                        pipelineUtils.verifyPod(OPENSHIFT_NAMESPACE, env.NODE_NAME)
                                        checkout([$class: 'GitSCM',
                                            branches: [[name: env.ghprbActualCommit]],
                                            recursiveSubmodules: true,
                                            extensions         : [],
                                            submoduleCfg       : [],
                                            userRemoteConfigs  : [
                                                [refspec:
                                                    '+refs/heads/*:refs/remotes/origin/*  +refs/tags/*:refs/tags/*',
                                                    url: "https://github.com/${env.ghprbGhRepository}"]
                                                ]
                                        ])
                                        
                                    }
                                }

                                currentStage = "test-env-setup"
                                stage(currentStage) {
                                    parallel (
                                        'centos7': {
                                            stage("${currentStage}-centos7") {
                                                envsetupUtils.timedPipelineStep(stepName: "${currentStage}-centos7", debug: true) {
                                                    // Set stage specific vars
                                                    envsetupUtils.setStageEnvVars(currentStage)

                                                    // Run contra-env-setup test
                                                    pipelineUtils.executeInContainer("${currentStage}-centos7", "contra-env-setup-test-c7", "/home/prepare_and_test.sh")
                                                }
                                            }
                                        },
                                        'fedora28': {
                                            stage("${currentStage}-fedora28") {
                                                envsetupUtils.timedPipelineStep(stepName: "${currentStage}-fedora28", debug: true) {
                                                    // Set stage specific vars
                                                    envsetupUtils.setStageEnvVars(currentStage)

                                                    // Fix for minishift cgrups/cpuset bug
                                                    pipelineUtils.executeInContainer("${currentStage}-fedora28", "contra-env-setup-test-f28", "/home/fix-minishift.sh || true")

                                                    // Run contra-env-setup test
                                                    pipelineUtils.executeInContainer("${currentStage}-fedora28", "contra-env-setup-test-f28", "/home/prepare_and_test.sh")
                                                }
                                            }
                                        }
                                    )
                                }
                            } catch (e) {
                                // Set build result
                                buildResult = 'FAILURE'
                                currentBuild.result = buildResult

                                // Report the exception
                                echo "Error: Exception from " + currentStage + ":"
                                echo e.getMessage()

                                // Throw the error
                                throw e

                            } finally {
                                currentBuild.result = buildResult ?: 'SUCCESS'
                                pipelineUtils.getContainerLogsFromPod(OPENSHIFT_NAMESPACE, env.NODE_NAME)

                                // Archive our artifacts
                                step([$class: 'ArtifactArchiver', allowEmptyArchive: true, artifacts: '*.xml,*.log,**/job.*,**/inventory.*', excludes: '**/*.example', fingerprint: true])

                                // set the metrics we want
                                ciMetrics.setMetricTag(jobMeasurement, 'build_result', currentBuild.result)
                                ciMetrics.setMetricField(jobMeasurement, 'build_time', currentBuild.getDuration())

                                // Archive JUnit results
                                step([$class: 'JUnitResultArchiver', testResults: '*.xml'])

                            }
                        }
                    }
                }
            }
}
