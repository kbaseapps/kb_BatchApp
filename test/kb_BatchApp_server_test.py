# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import shutil
import requests

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from ReadsUtils.ReadsUtilsClient import ReadsUtils
from kb_BatchApp.kb_BatchAppImpl import kb_BatchApp
from kb_BatchApp.kb_BatchAppServer import MethodContext
from kb_BatchApp.authclient import KBaseAuth as _KBaseAuth


class kb_BatchAppTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('kb_BatchApp'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'kb_BatchApp',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        cls.serviceImpl = kb_BatchApp(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_kb_BatchApp_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    def loadSingleEndReads(self):
        if hasattr(self.__class__, 'se_reads_ref'):
            return self.__class__.se_reads_ref
        # return '23735/2/1'
        fq_path = os.path.join(self.scratch, 'reads_1_se.fq')
        shutil.copy(os.path.join('data', 'reads_1.fq'), fq_path)

        ru = ReadsUtils(self.callback_url)
        se_reads_ref = ru.upload_reads({'fwd_file': fq_path,
                                        'wsname': self.getWsName(),
                                        'name': 'test_readsSE',
                                        'sequencing_tech': 'artificial reads'})['obj_ref']
        self.__class__.se_reads_ref = se_reads_ref
        print('Loaded SingleEndReads: ' + se_reads_ref)
        return se_reads_ref

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_run_batch(self):

        print("............  TESTING   ...........")

        se_reads_ref = self.loadSingleEndReads()

        #se_reads_ref = "31433/2;30155/1/1"

        batch_input = {
            'module_name': 'kb_ea_utils',
            'method_name': 'get_fastq_ea_utils_stats',
            'meta': {
                'tag': 'release'
            },
            'service_ver': '1.1.0',
            'wsid': '30155',
            'batch_params': [
                {
                    'params': [{
                        u'read_library_ref': se_reads_ref
                    }],
                },
                {
                    'params': [{
                        u'read_library_ref': se_reads_ref
                    }],
                }
            ]
        }

        retVal = self.getImpl().run_batch(self.ctx, batch_input)[0]
        print("TEST RUN RESULTS\n================")
        pprint(retVal)

        self.assertIn('batch_results', retVal)
        self.assertEqual(len(retVal['batch_results'].keys()), 2)
        for child_id, child_job in retVal['batch_results'].items():
            self.assertIn('result_package', child_job)
            self.assertEqual(child_id, child_job['result_package']['run_context']['job_id'])
