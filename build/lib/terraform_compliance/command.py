"""
The command line interface to cfn_nagger.

"""
from __future__ import absolute_import, division, print_function
import sys
import inspect
import logging
import traceback
from configparser import RawConfigParser
import boto3
import click
from terraform_compliance import TerraformValidator
import terraform_compliance
import json

def lineno():
    """Returns the current line number in our program."""
    return str(' - TerraformCompliance - line number: '+str(inspect.currentframe().f_back.f_lineno))


@click.group()
@click.version_option(version='0.0.19')
def cli():
    pass


@cli.command()
@click.option('--sfile', '-s', help='State File', required=True)
@click.option('--version', '-v', help='Print version and exit', required=False, is_flag=True)
@click.option('--region', '-r', help='AWS region', required=False, is_flag=True)
@click.option('--debug', help='Turn on debugging', required=False, is_flag=True)
def validate(
        sfile,
        version,
        region,
        debug
    ):
    '''
    primary function for validating a state file
    :return:
    '''

    sfile_data = read_statefile(sfile)

    if 'parameters' not in sfile_data:
        sfile_data['parameters'] = {}

    if debug:
        sfile_data['parameters']['debug'] = True
    else:
        sfile_data['parameters']['debug'] = False

    if region:
        sfile_data['parameters']['region'] = str(region)
    else:
        sfile_data['parameters']['region'] = 'us-east-1'


    print(sfile_data)
    if version:
        myversion()
    else:
        start_validate(
            sfile_data,
            debug
        )






@click.option('--version', '-v', help='Print version and exit', required=False, is_flag=True)
def version(version):
    """
    Get version
    :param version:
    :return:
    """
    myversion()


def myversion():
    '''
    Gets the current version
    :return: current version
    '''
    print('Version: ' + str(terraform_compliance.__version__))

def start_validate(
        sfile,
        debug
    ):
    '''
    Starts the validation
    :return:
    '''
    if debug:
        print('command - start_validate'+lineno())
        print('state file data: '+str(sfile)+lineno())


    config_dict = {}

    #if 'debug' in ini['parameters']:

    #    if ini['parameters']['debug']:
    #        config_dict['debug'] = ini['parameters']['debug']
    #    else:
    #        config_dict['debug'] = False
    #else:
    #    config_dict['debug'] = False

    #if ini['parameters']['bucket_name']:
    #    config_dict['bucket_name'] = ini['parameters']['bucket_name']
    #if ini['environment']['profile']:
    #    config_dict['aws_profile'] = ini['environment']['profile']
    #if ini['environment']['region']:
    #    config_dict['region'] = ini['environment']['region']
    #tags = []



    validator = TerraformValidator(sfile)
    if debug:
        print('print have TerraformValidation')
    #if creator.create():
    #    if debug:
    #        print('created')
    #else:
    #    if debug:
    #        print('not created')

    validator.validate()

def find_myself():
    """
    Find myself
    Args:
        None
    Returns:
       An Amazon region
    """
    my_session = boto3.session.Session()
    return my_session.region_name

def read_statefile(state_file):
    """
    Read the terraform state file
    Args:
        state_file - path to the file
    Returns:
        A dictionary
    Exits:
        1 - if problems are encountered
    """
    try:
        with open(state_file) as json_file:
            data = json.load(json_file)
            for p in data:
                print(p)
            return data
    except Exception as wtf:
        logging.error('Exception caught in read_statefile(): {}'.format(wtf))
        traceback.print_exc(file=sys.stdout)
        return sys.exit(1)



