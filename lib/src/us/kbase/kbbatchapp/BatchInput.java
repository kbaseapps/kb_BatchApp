
package us.kbase.kbbatchapp;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: BatchInput</p>
 * <pre>
 * The inputs for a batch run on a single app.
 * ----------
 * module_name - the name of the module to run. In an app like "MEGAHIT.run_megahit", this would be "MEGAHIT"
 * method_name - the name of the method to run in the module. In the above, this would be "run_megahit"
 * service_ver - the version of the app to run (or a github hash)
 * wsid - the id of the workspace to associate with the job for sharing purposes
 * meta - the job metadata
 * batch_params - the list of input parameters for the app.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "module_name",
    "method_name",
    "service_ver",
    "wsid",
    "meta",
    "batch_params"
})
public class BatchInput {

    @JsonProperty("module_name")
    private String moduleName;
    @JsonProperty("method_name")
    private String methodName;
    @JsonProperty("service_ver")
    private String serviceVer;
    @JsonProperty("wsid")
    private String wsid;
    /**
     * <p>Original spec-file type: MetaInput</p>
     * <pre>
     * Describes the metadata for a single batch run. Passed along to the Narrative Job Service on each child
     * job started.
     * ----------
     * cell_id - the unique id for the Narrative cell that starts the batch.
     * run_id - the unique id assigned to the run from the Narrative.
     * tag - the version tag (one of "release", "beta" or "dev") for the app being run in batch.
     * </pre>
     * 
     */
    @JsonProperty("meta")
    private MetaInput meta;
    @JsonProperty("batch_params")
    private List<ParamsInput> batchParams;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("module_name")
    public String getModuleName() {
        return moduleName;
    }

    @JsonProperty("module_name")
    public void setModuleName(String moduleName) {
        this.moduleName = moduleName;
    }

    public BatchInput withModuleName(String moduleName) {
        this.moduleName = moduleName;
        return this;
    }

    @JsonProperty("method_name")
    public String getMethodName() {
        return methodName;
    }

    @JsonProperty("method_name")
    public void setMethodName(String methodName) {
        this.methodName = methodName;
    }

    public BatchInput withMethodName(String methodName) {
        this.methodName = methodName;
        return this;
    }

    @JsonProperty("service_ver")
    public String getServiceVer() {
        return serviceVer;
    }

    @JsonProperty("service_ver")
    public void setServiceVer(String serviceVer) {
        this.serviceVer = serviceVer;
    }

    public BatchInput withServiceVer(String serviceVer) {
        this.serviceVer = serviceVer;
        return this;
    }

    @JsonProperty("wsid")
    public String getWsid() {
        return wsid;
    }

    @JsonProperty("wsid")
    public void setWsid(String wsid) {
        this.wsid = wsid;
    }

    public BatchInput withWsid(String wsid) {
        this.wsid = wsid;
        return this;
    }

    /**
     * <p>Original spec-file type: MetaInput</p>
     * <pre>
     * Describes the metadata for a single batch run. Passed along to the Narrative Job Service on each child
     * job started.
     * ----------
     * cell_id - the unique id for the Narrative cell that starts the batch.
     * run_id - the unique id assigned to the run from the Narrative.
     * tag - the version tag (one of "release", "beta" or "dev") for the app being run in batch.
     * </pre>
     * 
     */
    @JsonProperty("meta")
    public MetaInput getMeta() {
        return meta;
    }

    /**
     * <p>Original spec-file type: MetaInput</p>
     * <pre>
     * Describes the metadata for a single batch run. Passed along to the Narrative Job Service on each child
     * job started.
     * ----------
     * cell_id - the unique id for the Narrative cell that starts the batch.
     * run_id - the unique id assigned to the run from the Narrative.
     * tag - the version tag (one of "release", "beta" or "dev") for the app being run in batch.
     * </pre>
     * 
     */
    @JsonProperty("meta")
    public void setMeta(MetaInput meta) {
        this.meta = meta;
    }

    public BatchInput withMeta(MetaInput meta) {
        this.meta = meta;
        return this;
    }

    @JsonProperty("batch_params")
    public List<ParamsInput> getBatchParams() {
        return batchParams;
    }

    @JsonProperty("batch_params")
    public void setBatchParams(List<ParamsInput> batchParams) {
        this.batchParams = batchParams;
    }

    public BatchInput withBatchParams(List<ParamsInput> batchParams) {
        this.batchParams = batchParams;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((((((((("BatchInput"+" [moduleName=")+ moduleName)+", methodName=")+ methodName)+", serviceVer=")+ serviceVer)+", wsid=")+ wsid)+", meta=")+ meta)+", batchParams=")+ batchParams)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
