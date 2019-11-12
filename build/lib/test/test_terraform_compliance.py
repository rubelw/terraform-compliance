import os
import sys
import unittest
import json
from collections import OrderedDict
from terraform_compliance.ValidateUtility import ValidateUtility as class_to_test
from localstack.services import infra
import boto3

os.environ['SERVICES'] = SERVICES
os.environ['DEFAULT_REGION']=REGION
os.environ['LAMBDA_EXECUTOR'] = 'local'
os.environ['HOSTNAME'] = 'localhost'
os.environ['HOSTNAME_EXTERNAL']='localhost'
os.environ['USE_SSL']='false'
os.environ['LAMBDA_REMOTE_DOCKER']='false'
os.environ['DATA_DIR']=os.getcwd()

# start localstack
infra.start_infra(asynchronous=True)

def pretty(value, htchar='\t', lfchar='\n', indent=0):
    """
    Prints pretty json
    :param value:
    :param htchar:
    :param lfchar:
    :param indent:
    :return: pretty json
    """


    nlch = lfchar + htchar * (indent + 1)
    if type(value) == type(dict()) or type(value) == type(OrderedDict()):
        items = [
            nlch + repr(key) + ': ' + pretty(value[key], htchar, lfchar, indent + 1)
            for key in value
        ]
        return '{%s}' % (','.join(items) + lfchar + htchar * indent)

    elif type(value) == type(list()):
        items = [
            nlch + pretty(item, htchar, lfchar, indent + 1)
            for item in value
        ]

        if items:
            items = sorted(items)
        [str(item) for item in items]
        return '[%s]' % (','.join(items) + lfchar + htchar * indent)

    elif type(value) is tuple:
        items = [
            nlch + pretty(item, htchar, lfchar, indent + 1)
            for item in value
        ]
        return '(%s)' % (','.join(items) + lfchar + htchar * indent)

    else:
        return repr(str(value))


class TestTerraformCompliance(unittest.TestCase):

    @pytest.fixture(scope="session", autouse=True)
    def setupConfig(request):
        try:
            # print("Function setup")

            time.sleep(30)
            current_directory = os.getcwd()

            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket='test',ACL='public-read')

        except Exception as e:
            # Teardown the failed configuration and re-raise the exception
            teardownConfig()
            raise e
        yield

        validateTerraform()
        teardownConfig()

    def teardownConfig():
        print("Teardown code...")

        current_directory = os.getcwd()

        process = subprocess.Popen(['/usr/local/bin/terraform', 'destroy', '-auto-approve'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   cwd=str(current_directory) )
        process.wait()
        stdout, stderr = process.communicate()
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        stdout = ansi_escape.sub('', stdout.decode('utf-8'))
        stderr = ansi_escape.sub('', stderr.decode('utf-8'))
        print(stdout)
        print(stderr)

        infra.stop_infra()

        if os.path.exists(current_directory+'/terraform.tfstate'):
            os.remove(current_directory+'/terraform.tfstate')

         if os.path.exists(current_directory+'/terraform.tfstate.backup'):
            os.remove(current_directory+'/terraform.tfstate.backup')


    """
    Test public s3 bucket
    """
    def test_public_s3_bucket(self):

        validator = TerraformValidator(str(current_directory) + '/terraform.tfstate')
        results = validator.validate()
        print("validator: " + str(results))
        assert str(results) is True

