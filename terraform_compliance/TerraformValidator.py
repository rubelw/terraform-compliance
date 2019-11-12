from __future__ import absolute_import, division, print_function
import logging
import inspect
import sys
import json
from terraform_compliance.rules.S3Rules import S3Rules



def lineno():
    """Returns the current line number in our program."""
    return str(' - TerraforValidator - line number: '+str(inspect.currentframe().f_back.f_lineno))


class TerraformValidator:
    """
    Validates a terraform tf.state file
    """

    def __init__(self, state_file):
        """
        Initialize Validator
        :param statefile:
        """

        print('type2: '+str(type(state_file)))

        if type(state_file) == type(dict()):
            self.data = state_file
            self.debug = state_file['parameters']['debug']
        elif type(state_file) == type(str()):

            try:
                print('trying to open: '+str(state_file))
                with open(state_file) as json_file:
                    results = json.load(json_file)
                    print('result: '+str(results))
                    self.data = results

                    self.data['parameters'] = {}
                    self.data['parameters']['debug'] = True
                    self.data['parameters']['region'] = 'us-east-1'
                    self.debug = True


            except Exception as wtf:
                print(str(wtf))
                logging.error('Exception caught in read_statefile(): {}'.format(wtf))
                sys.exit(1)
        else:
            print('do not know what type of state file this is')

            sys.exit(1)





    def validate(self):
        """
        Validate the state file
        :return: rendered results
        """

        if self.debug:
            print('TerraformValidator - validate'+lineno())

        rules = S3Rules(self.data)
        results = rules.check_for_public_bucket()

        print('rules results: '+str(results))
        return results