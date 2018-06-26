from pprint import pprint

import copy
import re

from Workspace.WorkspaceClient import Workspace
from KBParallel.KBParallelClient import KBParallel


class BatchRunner(object):
    def __init__(self, scratch_dir, workspace_url, callback_url, srv_wiz_url, context):
        self.scratch_dir = scratch_dir
        self.workspace_url = workspace_url
        self.callback_url = callback_url
        self.srv_wiz_url = srv_wiz_url
        self.provenance = context.provenance()
        self.job_id = None
        current_call_ctx = context.get('rpc_context', {}).get('call_stack')
        if len(current_call_ctx):
            self.job_id = current_call_ctx[0].get('job_id')

        # from the provenance, extract out the version to run by exact hash if possible
        self.my_version = 'release'
        if len(self.provenance) > 0:
            if 'subactions' in self.provenance[0]:
                self.my_version = self.get_version_from_subactions('kb_BatchApp', self.provenance[0]['subactions'])
        print('Running kb_BatchApp version = ' + self.my_version)

        self.ws = Workspace(self.workspace_url)
        self.parallel_runner = KBParallel(self.callback_url, service_ver='dev')

    def get_version_from_subactions(self, module_name, subactions):
        # go through each sub action looking for
        if not subactions:
            return 'release'  # default to release if we can't find anything
        for sa in subactions:
            if 'name' in sa:
                if sa['name'] == module_name:
                    # local-docker-image implies that we are running in kb-test, so return 'dev'
                    if sa['commit'] == 'local-docker-image':
                        return 'dev'
                    # to check that it is a valid hash, make sure it is the right
                    # length and made up of valid hash characters
                    if re.match('[a-fA-F0-9]{40}$', sa['commit']):
                        return sa['commit']
        # again, default to setting this to release
        return 'release'

    def run(self, params):
        self.validate_params(params)  # raises an exception if there's a failure. see that function for details.

        app_info = {
            'module_name': params['module_name'],
            'function_name': params['method_name'],
            'version': params['service_ver']
        }

        params_list = params.get('batch_params')
        print('Running on set of parameters =')
        pprint(params_list)

        tasks = []
        for input_params in params_list:
            tasks.append(self.build_single_execution_task(app_info, input_params))

        batch_run_params = {
            'tasks': tasks,
            'runner': 'parallel',
            'max_retries': 2,
            'parent_job_id': self.job_id
        }

        # TODO check if this should be given in input
        batch_run_params['concurrent_local_tasks'] = 0
        batch_run_params['concurrent_njsw_tasks'] = 5

        print("========================  BATCH_RUN_PARAMS  ====================")
        pprint(batch_run_params)
        print("================================================================")

        batch_results = self.parallel_runner.run_batch(batch_run_params)
        print('Batch run results=')
        pprint(batch_results)

        results = {
            'batch_results': dict()
        }
        for result in batch_results['results']:
            results['batch_results'][result['result_package']['run_context']['job_id']] = result

        return results

    def build_single_execution_task(self, app_info, params):
        task_params = copy.deepcopy(params.get('params')[0])

        retVal = {'parameters': task_params}
        retVal.update(app_info)
        return retVal

    def clean(self, run_output_info):
        """
        Not really necessary on a single run, but if we are running multiple local subjobs, we
        should clean up files that have already been saved back up to KBase.
        """
        pass

    def validate_params(self, params):
        """
        Things to validate.
        params.module_name and params.method_name are real (maybe just let that go and assume they're ok)
        params.wsid is a real workspace id and the current user has write-access.
        params.batch_params is a list with len > 0
        """
        if params.get("batch_params", None) is None or (isinstance(params["batch_params"], list) and len(params["batch_params"]) == 0):
            raise ValueError("batch_params must be a list with a length >= 1")
        if params.get("module_name") is None:
            raise ValueError("module_name must be an existing KBase app module!")
        elif "." in params["module_name"] or "/" in params["module_name"]:
            raise ValueError("module_name should just be the name of the module, NOT the full module.method")
        if params.get("method_name") is None:
            raise ValueError("method_name must be an existing KBase app method!")
        elif "." in params["method_name"] or "/" in params["method_name"]:
            raise ValueError("method_name should just be the name of the method, NOT the full module.method")
        if params.get("service_ver") is None or not isinstance(params["service_ver"], basestring):
            raise ValueError("service_ver must be a valid string!")
        if params.get("wsid") is None:
            raise ValueError("A workspace id must be provided to associate each subjob!")
        return params
