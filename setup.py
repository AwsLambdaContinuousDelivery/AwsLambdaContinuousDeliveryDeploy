#!/usr/bin/env python

from distutils.core import setup

<<<<<<< HEAD
setup( name='AwsLambdaContinuousDeliveryDeploy'
     , version = '0.0.1'
     , description = 'AwsLambdaContinuousDeliveryDeploy'
=======
setup( name='pyAwsLambdaContinuousDeliveryDeploy'
     , version = '0.0.1'
     , description = 'pyAwsLambdaContinuousDeliveryDeploy'
>>>>>>> 87acc6068dbe565a352525bb476bae6a84adb6a1
     , author = 'Janos Potecki'
     , url = 'https://github.com/AwsLambdaContinuousDelivery/AwsLambdaContinuousDeliveryDeploy'
     , packages = ['awslambdacontinuousdelivery.deploy']
     , license='MIT'
     , install_requires = [ 
          'troposphere'
        , 'awacs'
        ]
<<<<<<< HEAD
     )
=======
     )
>>>>>>> 87acc6068dbe565a352525bb476bae6a84adb6a1
