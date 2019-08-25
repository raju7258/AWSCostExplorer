# AWSCostExplorer


#This is the code for getting AWS Total billing of 30 days using AWS Lambda and AWS SES. You will receive the total billing of your account to the email ID entered in the lambda function.
=======

This is the code for getting AWS Total billing of 30 days using AWS Lambda and AWS SES. You will receive the total billing of your account to the email ID entered in the lambda function.


Requirements
-----------


1. AWS IAM Role needs to be created for Lambda Function to run.

    Custom IAM Policy for the role is available as "AWS_Policy_Custom.json"

2. AWS SES email id to be verified

    You need to verify email ID in AWS SES.

3. Enable Cost Explorer

Changes in Lambda Function
------------------


1. You need to update change the email id from "rajeshnair@rajeshnair.co.in" to your AWS SES verified email ID.

