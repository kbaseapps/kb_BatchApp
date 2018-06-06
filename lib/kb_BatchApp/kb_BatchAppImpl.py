# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
from pprint import pprint
from util.BatchRunner import BatchRunner
#END_HEADER


class kb_BatchApp:
    '''
    Module Name:
    kb_BatchApp

    Module Description:
    kb_BatchApp
-----------
This contains tools for running batch jobs.
In this first pass, a "batch" is defined as multiple parallel runs of a single job. Each job's inputs and outputs should
be treated as independent of each other. An example might be a parameter sweep for a single app, or importing a list of
files using the same parameters, just being run multiple times.
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/briehl/kb_BatchApp"
    GIT_COMMIT_HASH = "b1790d5363e9dc72db1ee8cdfff04ca65968511c"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.scratch_dir = os.path.abspath(config['scratch'])
        self.workspace_url = config['workspace-url']
        self.srv_wiz_url = config['srv-wiz-url']
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        #END_CONSTRUCTOR
        pass


    def run_batch(self, ctx, params):
        """
        Runs a batch of the same app with a number of different input parameters.
        :param params: instance of type "BatchInput" (The inputs for a batch
           run on a single app. ---------- module_name - the name of the
           module to run. In an app like "MEGAHIT.run_megahit", this would be
           "MEGAHIT" method_name - the name of the method to run in the
           module. In the above, this would be "run_megahit" service_ver -
           the version of the app to run (or a github hash) wsid - the id of
           the workspace to associate with the job for sharing purposes meta
           - the job metadata batch_params - the list of input parameters for
           the app.) -> structure: parameter "module_name" of String,
           parameter "method_name" of String, parameter "service_ver" of
           String, parameter "wsid" of String, parameter "meta" of type
           "MetaInput" (Describes the metadata for a single batch run. Passed
           along to the Narrative Job Service on each child job started.
           ---------- cell_id - the unique id for the Narrative cell that
           starts the batch. run_id - the unique id assigned to the run from
           the Narrative. tag - the version tag (one of "release", "beta" or
           "dev") for the app being run in batch.) -> structure: parameter
           "cell_id" of String, parameter "run_id" of String, parameter "tag"
           of String, parameter "batch_params" of list of type "ParamsInput"
           (Describes the parameters for a single run in a batch. This
           contains both the set of parameters for a given run, along with
           the list of object UPAs to be used in setting provenance.
           ---------- params - an arbitrary list of inputs for the job run.
           source_ws_objects - the list of UPAs used as inputs to this job.
           These should be reflected somewhere in params.) -> structure:
           parameter "params" of list of unspecified object, parameter
           "source_ws_objects" of list of type "obj_ref" (An UPA for a single
           object.)
        :returns: instance of type "BatchResult" (The results of a batch run.
           -------- batch_result - a mapping from a string (child job id) to
           the result for that child job report_name - the name of the report
           for the entire batch run report_ref - the UPA of the report for
           the entire batch run) -> structure: parameter "batch_result" of
           mapping from String to unspecified object, parameter "report_name"
           of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN run_batch
        print("=============  RUN_BATCH_PARAMS  ==================")
        pprint(params)
        print("===================================================")
        batchRunner = BatchRunner(self.scratch_dir, self.workspace_url,
                                  self.callback_url, self.srv_wiz_url,
                                                  ctx.provenance())
        result = batchRunner.run(params)
        returnVal = {'result': result}
        #END run_batch

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method run_batch return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
