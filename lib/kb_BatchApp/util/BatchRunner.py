from pprint import pprint

import copy

from Workspace.WorkspaceClient import Workspace
from KBParallel.KBParallelClient import KBParallel

class BatchRunner(object):

    def __init__(self, scratch_dir, workspace_url, callback_url, srv_wiz_url, provenance):
        self.scratch_dir = scratch_dir
        self.workspace_url = workspace_url
        self.callback_url = callback_url
        self.srv_wiz_url = srv_wiz_url
        self.provenance = provenance

        # from the provenance, extract out the version to run by exact hash if possible
        self.my_version = 'release'
        if len(provenance) > 0:
            if 'subactions' in provenance[0]:
                self.my_version = self.get_version_from_subactions('kb_BatchApp', provenance[0]['subactions'])
        print('Running kb_BatchApp version = ' + self.my_version)

        self.ws = Workspace(self.workspace_url)
        self.parallel_runner = KBParallel(self.callback_url)

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
        #
        # validated_params = self.validate_params(params)
        validated_params = params
        num_params = len(validated_params.get('batch_params'))

        app_info = {'module_name': validated_params.get('app_id'),
                    'function_name': validated_params.get('method'),
                    'version': validated_params.get('service_ver')}

        if num_params >= 1:
            params_list = validated_params.get('batch_params')
            print('Running on set of parameters =')
            pprint(params_list)

            tasks = []
            for input_params in params_list:
                tasks.append(self.build_single_execution_task(app_info, input_params))

            batch_run_params = {'tasks': tasks,
                                'runner': 'parallel',
                                'max_retries': 2}

            # TODO check if this should be given in input
            batch_run_params['concurrent_local_tasks'] = 1
            batch_run_params['concurrent_njsw_tasks'] = 0

            print("========================  BATCH_RUN_PARAMS  ====================")
            pprint(batch_run_params)
            print("================================================================")

            results = self.parallel_runner.run_batch(batch_run_params)
            print('Batch run results=')
            pprint(results)

            return results

        raise ('Improper number of method parameters')


    def build_single_execution_task(self, app_info, params):
        task_params = copy.deepcopy(params.get('params')[0])

        retVal = {'parameters': task_params}
        retVal.update(app_info)
        return retVal

    def clean(self, run_output_info):
        ''' Not really necessary on a single run, but if we are running multiple local subjobs, we
        should clean up files that have already been saved back up to kbase '''
        pass

    def validate_params(self, params):
        # TODO Add validation if needed
        return params

