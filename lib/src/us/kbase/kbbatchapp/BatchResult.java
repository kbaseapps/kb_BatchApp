
package us.kbase.kbbatchapp;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import us.kbase.common.service.UObject;


/**
 * <p>Original spec-file type: BatchResult</p>
 * <pre>
 * The results of a batch run.
 * --------
 * batch_result - a mapping from a string (child job id) to the result for that child job
 * report_name - the name of the report for the entire batch run
 * report_ref - the UPA of the report for the entire batch run
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "batch_result",
    "report_name",
    "report_ref"
})
public class BatchResult {

    @JsonProperty("batch_result")
    private Map<String, UObject> batchResult;
    @JsonProperty("report_name")
    private java.lang.String reportName;
    @JsonProperty("report_ref")
    private java.lang.String reportRef;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("batch_result")
    public Map<String, UObject> getBatchResult() {
        return batchResult;
    }

    @JsonProperty("batch_result")
    public void setBatchResult(Map<String, UObject> batchResult) {
        this.batchResult = batchResult;
    }

    public BatchResult withBatchResult(Map<String, UObject> batchResult) {
        this.batchResult = batchResult;
        return this;
    }

    @JsonProperty("report_name")
    public java.lang.String getReportName() {
        return reportName;
    }

    @JsonProperty("report_name")
    public void setReportName(java.lang.String reportName) {
        this.reportName = reportName;
    }

    public BatchResult withReportName(java.lang.String reportName) {
        this.reportName = reportName;
        return this;
    }

    @JsonProperty("report_ref")
    public java.lang.String getReportRef() {
        return reportRef;
    }

    @JsonProperty("report_ref")
    public void setReportRef(java.lang.String reportRef) {
        this.reportRef = reportRef;
    }

    public BatchResult withReportRef(java.lang.String reportRef) {
        this.reportRef = reportRef;
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
        return ((((((((("BatchResult"+" [batchResult=")+ batchResult)+", reportName=")+ reportName)+", reportRef=")+ reportRef)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
