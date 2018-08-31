#!/usr/bin/groovy
package org.contraenvsetup.pipeline

import org.centos.*

/**
 * Library to set default environmental variables. Performed once at start of Jenkinsfile
 * @param envMap: Key/value pairs which will be set as environmental variables.
 * @return
 */
def setDefaultEnvVars(Map envMap=null){
    // If we've been provided an envMap, we set env.key = value
    // Note: This may overwrite above specified values.
    envMap.each { key, value ->
        env."${key.toSTring().trim()}" = value.toString().trim()
    }
}

/**
 * Library to set stage specific environmental variables.
 * @param stage - Current stage
 * @return
 */
def setStageEnvVars(String stage){
    def stages =
             ["test-env-setup"       : [
                     PROJECT_REPO        : env.PROJECT_REPO,
                     PR_NUM              : env.ghprbPullId,
                     ACTUAL_COMMIT       : env.ghprbActualCommit,
             ],
            ]

    // Get the map of env var keys and values and write them to the env global variable
    if(stages.containsKey(stage)) {
        stages.get(stage).each { key, value ->
            env."${key}" = value
        }
    }
}

/**
 * Wrap the pipeline with timestamps and ansiColor
 * @param body Pipeline goes in here
 */
def ciPipeline(Closure body) {
    ansiColor('xterm') {
        deleteDir()
        body()
    }
}

def handlePipelineStep(Map config, Closure body) {
    try {

        if (config.debug) {
            echo "Starting ${config.stepName}"
        }

        body()

    } catch (Throwable err) {

        echo err.getMessage()
        throw err

    } finally {

        if (config.debug) {
            echo "end of ${config.stepName}"
        }
    }
}

/**
 * Function to return the job name
 * @return
 */
def timedMeasurement() {
    return env.JOB_NAME
}
