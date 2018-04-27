
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
import us.kbase.common.service.UObject;


/**
 * <p>Original spec-file type: ParamsInput</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "params",
    "source_ws_objects"
})
public class ParamsInput {

    @JsonProperty("params")
    private List<Map<String, UObject>> params;
    @JsonProperty("source_ws_objects")
    private List<String> sourceWsObjects;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("params")
    public List<Map<String, UObject>> getParams() {
        return params;
    }

    @JsonProperty("params")
    public void setParams(List<Map<String, UObject>> params) {
        this.params = params;
    }

    public ParamsInput withParams(List<Map<String, UObject>> params) {
        this.params = params;
        return this;
    }

    @JsonProperty("source_ws_objects")
    public List<String> getSourceWsObjects() {
        return sourceWsObjects;
    }

    @JsonProperty("source_ws_objects")
    public void setSourceWsObjects(List<String> sourceWsObjects) {
        this.sourceWsObjects = sourceWsObjects;
    }

    public ParamsInput withSourceWsObjects(List<String> sourceWsObjects) {
        this.sourceWsObjects = sourceWsObjects;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((("ParamsInput"+" [params=")+ params)+", sourceWsObjects=")+ sourceWsObjects)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
