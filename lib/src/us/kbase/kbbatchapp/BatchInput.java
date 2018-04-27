
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
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "app_id",
    "method",
    "service_ver",
    "wsid",
    "meta",
    "batch_params"
})
public class BatchInput {

    @JsonProperty("app_id")
    private String appId;
    @JsonProperty("method")
    private String method;
    @JsonProperty("service_ver")
    private String serviceVer;
    @JsonProperty("wsid")
    private String wsid;
    /**
     * <p>Original spec-file type: MetaInput</p>
     * 
     * 
     */
    @JsonProperty("meta")
    private MetaInput meta;
    @JsonProperty("batch_params")
    private List<ParamsInput> batchParams;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("app_id")
    public String getAppId() {
        return appId;
    }

    @JsonProperty("app_id")
    public void setAppId(String appId) {
        this.appId = appId;
    }

    public BatchInput withAppId(String appId) {
        this.appId = appId;
        return this;
    }

    @JsonProperty("method")
    public String getMethod() {
        return method;
    }

    @JsonProperty("method")
    public void setMethod(String method) {
        this.method = method;
    }

    public BatchInput withMethod(String method) {
        this.method = method;
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
     * 
     * 
     */
    @JsonProperty("meta")
    public MetaInput getMeta() {
        return meta;
    }

    /**
     * <p>Original spec-file type: MetaInput</p>
     * 
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
        return ((((((((((((((("BatchInput"+" [appId=")+ appId)+", method=")+ method)+", serviceVer=")+ serviceVer)+", wsid=")+ wsid)+", meta=")+ meta)+", batchParams=")+ batchParams)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
