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
    A KBase module: kb_BatchApp
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = ""

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
        :param params: instance of type "BatchInput" -> structure: parameter
           "app_id" of String, parameter "method" of String, parameter
           "service_ver" of String, parameter "wsid" of String, parameter
           "meta" of type "MetaInput" -> structure: parameter "cell_id" of
           String, parameter "run_id" of String, parameter "tag" of String,
           parameter "batch_params" of list of type "ParamsInput" ->
           structure: parameter "params" of list of mapping from String to
           unspecified object, parameter "source_ws_objects" of list of type
           "obj_ref"
        :returns: instance of type "BatchResult" -> structure: parameter
           "batch_result" of mapping from String to String, parameter
           "report_name" of String, parameter "report_ref" of String
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
