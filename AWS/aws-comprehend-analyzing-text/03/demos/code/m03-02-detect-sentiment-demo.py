#! /usr/bin/env python3

# Standard library modules
import os

# 3rd party modules
import boto3

# Global variables & constants
SAMPLE_FILE = "m02-02-war-of-the-worlds-intro-sample.txt"

"""
Sentiment Analysis
====================
1. Break up the sample text into paragraphs
2. Send the batch of paragraphs to Amazon Comprehend for sentiment analysis
3. Present the results
"""

# First create a client that can access the service
#   - this client automatically uses the current set of credentials for the AWS CLI
#   - more info on setting up those credentails is at https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html
api = boto3.client('comprehend')
print("Accessing Amazon Comprehend via {}".format(api.meta.endpoint_url))

# Break up the sample text into paragraphs
paragraphs = []
if os.path.exists(SAMPLE_FILE):
	try:
		with open(SAMPLE_FILE, 'r') as fh:
			doc = fh.read()
			paragraphs = doc.split('\n')
	except Exception as err:
		print("Could not read the sample file. Threw exception:\n\t{}".format(err))
else:
	print("Could not find the sample file [{}]".format(SAMPLE_FILE))

# Prepare the sample text for the API call
text_blocks = [p for p in paragraphs if len(p.strip()) > 0] # remove empty paragraphs

# Send the text blocks to Amazon Comprehend for sentiment analysis
response = None
if len(text_blocks) >= 1 and len(text_blocks) <= 25: # we can only send 1-25 text blocks as a batch
	response = api.batch_detect_sentiment(TextList=text_blocks, LanguageCode="en") # we know the sample is in English but could also use detect_dominant_language to get the code
else:
	print("No text blocks available to send to Amazon Comprehend")

# Present the results
if response:
	print("----------------------------------------")
	for result in response['ResultList']:
		text_block_snippet = "{}...".format(text_blocks[result['Index']][0:100]) # get up to the first 100 characters of the sample text
		index = result['Index']
		sentiment = result['Sentiment']
		score = result['SentimentScore'][result['Sentiment'].title()]
		print(f"""TEXT BLOCK {index}
{text_block_snippet}
   {sentiment}	{score}
""") # the 'f' in front of the string automatically uses variables with the placeholder names. the """ quoted string follows the formatting in the code (which explains the multiline presentation)
else:
	print("No response from Amazon Comprehend")