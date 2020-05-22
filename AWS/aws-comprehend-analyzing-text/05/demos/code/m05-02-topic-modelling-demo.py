#! /usr/bin/env python3

# Standard library modules
import os
import time

# 3rd party modules
import boto3

# Global variables & constants
DATA_ACCESS_ARN = "arn:aws:iam::168495412682:role/AmazonComprehendDataAccessRole"

"""
Topic Modelling
=================
1. Configure the job paramters
2. Submit the job
3. Poll the service until the job completes or stops for another reason
"""

# First create a client that can access the service
#   - this client automatically uses the current set of credentials for the AWS CLI
#   - more info on setting up those credentails is at https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html
api = boto3.client('comprehend')
print("Accessing Amazon Comprehend via {}".format(api.meta.endpoint_url))

# Create the job input data configuration
input_data_config = {
	"S3Uri": "s3://atoawac-input/war-and-peace.txt", # s3://bucket/path_to_key
	"InputFormat": "ONE_DOC_PER_LINE",
}

# Create the job output data configuration
output_data_config = {
	"S3Uri": "s3://atoawac-output/", # s3://bucket/path_to_key << then the service will add more to the path
}

# Create the job on the service
response = api.start_topics_detection_job(
	InputDataConfig=input_data_config,
	OutputDataConfig=output_data_config,
	DataAccessRoleArn=DATA_ACCESS_ARN,
	JobName="M05-02 Topic Modelling Demo",
	)

# Get the JobId from the service
job_id = None
if response:
	job_id = response['JobId']

# Poll the service for any result besides "SUBMITTED" and "IN_PROGRESS"
polling = True
while polling:
	response = api.describe_topics_detection_job(JobId=job_id)
	print("Current status of job: {}".format(response['TopicsDetectionJobProperties']['JobStatus']))
	if response['TopicsDetectionJobProperties']['JobStatus'] in [ 'SUBMITTED', 'IN_PROGRESS']:
		# Work in progress, wait and keep polling
		print("Job in progress, waiting 30 seconds...")
		time.sleep(30) # wait 30 seconds and try again
	else:
		polling = False
		if response['TopicsDetectionJobProperties']['JobStatus'] == 'FAILED':
			print("Job failed due to:\n\t{}".format(response['TopicsDetectionJobProperties']['Message']))
		elif response['TopicsDetectionJobProperties']['JobStatus'] in [ 'STOP_REQUESTED', 'STOPPED' ]:
			print("Job has been manually stopped")
		else:
			print("Job completed! Results are available at:\n{}\n".format(response['TopicsDetectionJobProperties']['OutputDataConfig']['S3Uri']))