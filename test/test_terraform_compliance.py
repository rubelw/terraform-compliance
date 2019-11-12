import os
import sys
import unittest
import json
from collections import OrderedDict
from terraform_compliance.TerraformValidator import TerraformValidator as class_to_test





class TestTerraformValidator(unittest.TestCase):



    """
    Test public s3 bucket
    """
    def test_public_s3_bucket(self):
        current_directory = os.getcwd()
        validator = class_to_test(str(current_directory) + '/test/example.tfstate')
        results = validator.validate()
        print("validator: " + str(results))
        assert str(results) is True

