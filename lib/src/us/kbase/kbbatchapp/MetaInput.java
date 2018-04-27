
package us.kbase.kbbatchapp;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: MetaInput</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "cell_id",
    "run_id",
    "tag"
})
public class MetaInput {

    @JsonProperty("cell_id")
    private String cellId;
    @JsonProperty("run_id")
    private String runId;
    @JsonProperty("tag")
    private String tag;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("cell_id")
    public String getCellId() {
        return cellId;
    }

    @JsonProperty("cell_id")
    public void setCellId(String cellId) {
        this.cellId = cellId;
    }

    public MetaInput withCellId(String cellId) {
        this.cellId = cellId;
        return this;
    }

    @JsonProperty("run_id")
    public String getRunId() {
        return runId;
    }

    @JsonProperty("run_id")
    public void setRunId(String runId) {
        this.runId = runId;
    }

    public MetaInput withRunId(String runId) {
        this.runId = runId;
        return this;
    }

    @JsonProperty("tag")
    public String getTag() {
        return tag;
    }

    @JsonProperty("tag")
    public void setTag(String tag) {
        this.tag = tag;
    }

    public MetaInput withTag(String tag) {
        this.tag = tag;
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
        return ((((((((("MetaInput"+" [cellId=")+ cellId)+", runId=")+ runId)+", tag=")+ tag)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
