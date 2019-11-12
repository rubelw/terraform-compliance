from __future__ import absolute_import, division, print_function
import logging
import inspect
import boto3




def lineno():
    """Returns the current line number in our program."""
    return str(' - S3Rules - line number: '+str(inspect.currentframe().f_back.f_lineno))


class S3Rules:
    """
    S3 Validation Rules
    """

    def __init__(self, stfile):
        """
        Initialize Validator
        :param statefile:
        """

        self.debug = False
        self.data = stfile
        print(stfile['parameters'])
        self.debug = stfile['parameters']['debug']
        self.region = stfile['parameters']['region']
        print(self.data)



    def check_for_public_bucket(self):
        """
        Validate the state file
        :return: rendered results
        """


        if 'resources' in self.data:
            for resource in self.data['resources']:

                if 'type' in resource and resource['type'] == 'aws_s3_bucket':
                    if 'instances' in resource:
                        for instance in resource['instances']:

                            if 'attributes' in instance:
                                for attribute in instance['attributes']:
                                    print(attribute)
                                    if attribute == 'acl' and instance['attributes'][str(attribute)] == 'public-read':
                                        return False

        return True
