Terraform Compliance
====================

Features
========
Terraform compliance tool will evaluate your tf.state file against a repository of rules.

Installation
============
terraform-compliance is on PyPI so all you need is:

.. code:: console

   $ pip install terraform-compliance



Example
=======
Getting help

.. code:: console

   $ tfcomply validate --help
   Usage: tfcomply validate [OPTIONS]

   primary function for evaluating a tf.state file :return:

    Options:
      -s, --sfile TEXT  State File  [required]
      -v, --version     Print version and exit
      -r, --region      AWS region
      --debug           Turn on debugging
      --help            Show this message and exit.



.. code:: console

   tfcomply validate --sfile example.tfstate
   
   

Options

    * xxx

