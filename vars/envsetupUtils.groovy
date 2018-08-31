import org.contraenvsetup.pipeline.EnvSetupUtils

/**
 * A class of methods used in the contra-env-setup CI pipeline.
 * These methods are wrappers around methods in the ci-pipeline library.
 */
class envsetupUtils implements Serializable {

    def envsetupUtils = new EnvSetupUtils()
    def cimetrics

    /**
     * Method to set default environmental variables. Performed once at start of Jenkinsfile
     * @param envMap Key/value pairs which will be set as environmental variables.
     * @return
     */
    def setDefaultEnvVars(Map envMap = null) {
        envsetupUtils.setDefaultEnvVars(envMap)
    }

    /**
     * Method to set stage specific environmental variables.
     * @param stage Current stage
     * @return
     */
    def setStageEnvVars(String stage) {
        envsetupUtils.setStageEnvVars(stage)
    }


    /**
     * Wrap the pipeline with timestamps and ansiColor
     * @param body Pipeline goes in here
     */
    def ciPipeline(Closure body) {
        try {
            envsetupUtils.ciPipeline(body)
        } catch(e) {
            throw e
        } finally {
            //cimetrics.writeToInflux()
        }
    }

    def timedPipelineStep(Map config, Closure body) {
        def measurement = timedMeasurement()
        cimetrics.timed measurement, config.stepName, {
            envsetupUtils.handlePipelineStep(config, body)
        }
    }

    /**
     * Function to return the job name
     * @return
     */
    def timedMeasurement() {
        return "${influxDBPrefix()}_${envsetupUtils.timedMeasurement()}"
    }

    def influxDBPrefix() {
        return "contra-env-setup-ci-pipeline"
    }
}
