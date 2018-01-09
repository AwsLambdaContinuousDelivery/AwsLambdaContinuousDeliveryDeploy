#!/usr/bin/env python

from distutils.core import setup

setup( name='AwsLambdaContinuousDeliveryDeploy'
     , version = '0.0.1'
     , description = 'AwsLambdaContinuousDeliveryDeploy'
     , author = 'Janos Potecki'
     , url = 'https://github.com/AwsLambdaContinuousDelivery/AwsLambdaContinuousDeliveryDeploy'
     , packages = ['awslambdacontinuousdelivery.deploy']
     , license='MIT'
     , install_requires = [ 
          'troposphere'
        , 'awacs'
        ]
     )
