from django.test import TestCase
from django.test.utils import setup_test_environment
import json
from .models import *

    
class SpaceTraceTest(TestCase):

    def test_user_experience(self):
        """
        tests user experience 
        """
        resp = self.client.post('/api/sessions')
        self.assertEqual(resp.status_code, 200)

        #   test list of sessions
        resp = self.client.get('/api/sessions')
        self.assertEqual(resp.status_code, 200)
        obj = json.loads(resp.content)
        self.assertTrue('list' in obj)
        self.assertEqual([poll['id'] for poll in obj['list']], [1])

        #   test user getting that session
        #   should just contain the step
        resp = self.client.get('/api/updates/1')
        self.assertEqual(resp.status_code, 200)
        obj = json.loads(resp.content)
        compare = {'step': 1}
        self.assertEqual(compare, obj)

        #   test user setting arguments
        #   test user uploading files
        python_dict = {
                'files_to_upload': [{'name': 'abc.txt'}],
                'arguments': {'xff': 'select1', 'rotation':'30deg'}
            }
        resp = self.client.post(
            '/api/updates/1',
            json.dumps(python_dict),
            content_type="application/json")

        self.assertEqual(resp.status_code, 200)

        #   ensure those fields were set correctly
        stp1 = step_one.objects.get(pk=1)
        self.assertTrue(stp1.completed)
        stp2 = step_two.objects.get(pk=1)
        self.assertTrue(stp2.arguments != None)
        self.assertEqual(len(stp2.arguments), 2)
        self.assertTrue(stp2.files_to_upload != None)

        #   Emulate SpaceTraceHPC trying to recieve those arguments
        resp = self.client.get('/api/sessions/1')
        self.assertEqual(resp.status_code, 200)
        obj = json.loads(resp.content)
        self.assertTrue("step" in obj)
        self.assertTrue("files_to_upload" in obj)
        self.assertTrue("arguments" in obj)
        file_names = obj['files_to_upload']
        self.assertEqual(len(file_names), 1)
        arguments = obj['arguments']
        self.assertEqual(len(arguments), 2)

        #   Next Emulate SpaceTraceHPC posting an image for the
        #   User to evaluate

        python_dict = {
                'image': "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",
                "label" : 'test label',
                "info": 'test info'
            }
        resp = self.client.post(
            '/api/sessions/1',
            json.dumps(python_dict),
            content_type="application/json")

        self.assertEqual(resp.status_code, 200)
        stp2 = step_two.objects.get(pk=1)
        self.assertTrue(stp2.completed)
        step3 = step_three.objects.get(pk=1)
        self.assertEqual(python_dict, step3.data)

        #   Next emulate the user doing a request to view that
        #   Image posted in the previous step.

        resp = self.client.get('/api/updates/1')
        self.assertEqual(resp.status_code, 200)
        obj = json.loads(resp.content)
        self.assertEqual(len(obj), 4)
        self.assertEqual(obj['step'], 3)

        #   Next emulate the user sending click info to be served
        python_dict = {
                'data':
                    {
                        'click_loc': 'x123232,y123213',
                        'click_height': "400m",
                        'is_astronomy_cool': 'maybe',
                    }
            }
        resp = self.client.post(
            '/api/updates/1',
            json.dumps(python_dict),
            content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        step3 = step_three.objects.get(pk=1)
        self.assertTrue(step3.completed)
        step4 = step_four.objects.get(pk=1)
        self.assertEqual(python_dict['data'], step4.data)

        #   Next emulate the server polling for that data just set
        resp = self.client.get('/api/sessions/1')
        self.assertEqual(resp.status_code, 200)
        obj = json.loads(resp.content)
        self.assertEqual(len(obj), 2)
        self.assertEqual(obj['step'], 4)
        self.assertEqual(obj['data'],python_dict['data'])

        #   Finally have server post that job is completed
        python_dict = {
                'finish_instructions': 'Yes'
            }
        resp = self.client.post(
            '/api/sessions/1',
            json.dumps(python_dict),
            content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        step4 = step_four.objects.get(pk=1)
        self.assertTrue(step4.completed)
        step5 = step_five.objects.get(pk=1)
        self.assertEqual(python_dict, step5.data)