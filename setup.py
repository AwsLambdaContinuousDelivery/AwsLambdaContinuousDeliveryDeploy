#!/usr/bin/env python

from distutils.core import setup

setup( name='pyAwsLambdaContinuousDeliveryDeploy'
     , version = '0.0.1'
     , description = 'pyAwsLambdaContinuousDeliveryDeploy'
     , author = 'Janos Potecki'
     , url = 'https://github.com/AwsLambdaContinuousDelivery/AwsLambdaContinuousDeliveryDeploy'
     , packages = ['awslambdacontinuousdelivery.deploy']
     , license='MIT'
     , install_requires = [ 
          'troposphere'
        , 'awacs'
        ]
     )