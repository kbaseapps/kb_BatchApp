/*
kb_BatchApp
-----------
This contains tools for running batch jobs.
In this first pass, a "batch" is defined as multiple parallel runs of a single job. Each job's inputs and outputs should
be treated as independent of each other. An example might be a parameter sweep for a single app, or importing a list of
files using the same parameters, just being run multiple times.
*/

module kb_BatchApp {
    /* An UPA for a single object. */
    typedef string obj_ref;

    /*
        Describes the metadata for a single batch run. Passed along to the Narrative Job Service on each child
        job started.
        ----------
        cell_id - the unique id for the Narrative cell that starts the batch.
        run_id - the unique id assigned to the run from the Narrative.
        tag - the version tag (one of "release", "beta" or "dev") for the app being run in batch.
    */
    typedef structure {
        string cell_id;
        string run_id;
        string tag;
    } MetaInput;

    /*
        Describes the parameters for a single run in a batch. This contains both the set of parameters
        for a given run, along with the list of object UPAs to be used in setting provenance.
        ----------
        params - an arbitrary list of inputs for the job run.
        source_ws_objects - the list of UPAs used as inputs to this job. These should be reflected somewhere in params.
    */
    typedef structure {
        list<UnspecifiedObject> params;
        list<obj_ref> source_ws_objects;
    } ParamsInput;

    /*
        The inputs for a batch run on a single app.
        ----------
        module_name - the name of the module to run. In an app like "MEGAHIT.run_megahit", this would be "MEGAHIT"
        method_name - the name of the method to run in the module. In the above, this would be "run_megahit"
        service_ver - the version of the app to run (or a github hash)
        wsid - the id of the workspace to associate with the job for sharing purposes
        meta - the job metadata
        batch_params - the list of input parameters for the app.
    */
    typedef structure {
        string module_name;
        string method_name;
        string service_ver;
        string wsid;
        MetaInput meta;
        list<ParamsInput> batch_params;
    } BatchInput;

    /*
        The results of a batch run.
        --------
        batch_result - a mapping from a string (child job id) to the result for that child job
        report_name - the name of the report for the entire batch run
        report_ref - the UPA of the report for the entire batch run
    */
    typedef structure {
        mapping<string, UnspecifiedObject> batch_result;
        string report_name;
        string report_ref;
    } BatchResult;

    /*
        Runs a batch of the same app with a number of different input parameters.
    */
    funcdef run_batch(BatchInput params) returns (BatchResult returnVal) authentication required;
};