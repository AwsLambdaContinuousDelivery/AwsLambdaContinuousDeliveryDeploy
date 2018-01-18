# By Janos Potecki
# University College London
# January 2018

from awacs.aws import Allow
from awacs.iam import *
from awacs.awslambda import *

import awacs.aws
import awacs.ec2
import awacs.s3

from awslambdacontinuousdelivery.tools import alphanum
from awslambdacontinuousdelivery.tools.iam import defaultAssumeRolePolicyDocument
from awslambdacontinuousdelivery.python.test import getTest

from troposphere import Template, GetAtt, Ref, Sub
from troposphere.codepipeline import ( ActionTypeID
  , Actions, Stages, OutputArtifacts, InputArtifacts )
from troposphere.iam import Role, Policy

from typing import Tuple, List
import re
import json


def getDeployResources(t: Template) -> Tuple[ActionTypeID, Role]:
  statements = [
      awacs.aws.Statement(
          Action = [ awacs.ec2.Action("*")
                   , awacs.awslambda.GetFunction
                   , awacs.awslambda.CreateFunction
                   , awacs.awslambda.GetFunctionConfiguration
                   , awacs.awslambda.DeleteFunction
                   , awacs.awslambda.UpdateFunctionCode
                   , awacs.awslambda.UpdateFunctionConfiguration
                   , awacs.awslambda.CreateAlias
                   , awacs.awslambda.DeleteAlias
                   , awacs.s3.GetObject
                   ]
        , Resource = [ "*" ]
        , Effect = awacs.aws.Allow
        )
    , awacs.aws.Statement(
          Action = [ awacs.iam.DeleteRole
                   , awacs.iam.DeleteRolePolicy
                   , awacs.iam.GetRole
                   , awacs.iam.PutRolePolicy
                   , awacs.iam.CreateRole
                   , awacs.iam.PassRole
                   ]
        , Resource = [ "*" ]
        , Effect = awacs.aws.Allow
        )
    ]
  policy_doc = awacs.aws.Policy( Statement = statements )
  policy = Policy( PolicyDocument = policy_doc
                 , PolicyName = "CloudFormationDeployPolicy"
                 )
  assume = defaultAssumeRolePolicyDocument("cloudformation.amazonaws.com")
  role = Role( "CFDeployRole"
             , RoleName = Sub("${AWS::StackName}-CFDeployRole")
             , AssumeRolePolicyDocument = assume
             , Policies = [policy]
             )

  if role.title not in t.resources:
    role = t.add_resource(role)
  actionId = ActionTypeID( Category = "Deploy"
                         , Owner = "AWS"
                         , Version = "1"
                         , Provider = "CloudFormation"
                         )

  return (actionId, role)


def getDeploy( t: Template
             , inName: str
             , stage: str
             , interimArt: str #artifact containing func code incl. libs
             , sourceartifact: str = None
             , add_tests  = False
             ) -> Stages:
  [actionId, role] = getDeployResources(t)
  params = { "S3Key" : { "Fn::GetArtifactAtt" : [ interimArt, "ObjectKey" ] }
           , "S3Storage" : { "Fn::GetArtifactAtt" : [ interimArt, "BucketName" ] }
           }
  params = json.dumps(params)
  params = params.replace('"', '\"').replace('\n', '\\n')

  config = { "ActionMode" : "CREATE_UPDATE"
           , "RoleArn" : GetAtt(role, "Arn")
           , "StackName" : Sub("".join(["${AWS::StackName}Functions", stage]))
           , "Capabilities": "CAPABILITY_NAMED_IAM"
           , "TemplatePath" : inName + "::stack" + stage + ".json"
           , "ParameterOverrides" : params
           }
  arts = map(lambda x: InputArtifacts(Name = x), [inName, interimArt])
  actions = [ Actions( Name = "Deploy" + stage
                     , ActionTypeId = actionId
                     , InputArtifacts = list(arts)
                     , RunOrder = "1"
                     , Configuration = config
                     )
            ]
  if sourceartifact is not None and add_tests: 
    actions.append(getTest(t, sourceartifact, stage))
  return Stages( stage + "Deploy"
               , Name = stage
               , Actions = actions
               )
