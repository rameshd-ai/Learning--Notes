#! /usr/bin/env python3

# Standard library modules
import os

# 3rd party modules
import boto3

# Global variables & constants
SAMPLE_FILE = "m02-03-war-of-the-worlds-intro-sentence-sample.txt"

"""
Sentiment Analysis
====================
1. Break up the sample text into sentences that can be analyzed by Amazon Comprehend
2. Send the batch of paragraphs to Amazon Comprehend for sentiment analysis
3. Present the results
"""

# First create a client that can access the service
#   - this client automatically uses the current set of credentials for the AWS CLI
#   - more info on setting up those credentails is at https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html
api = boto3.client('comprehend')
print("Accessing Amazon Comprehend via {}".format(api.meta.endpoint_url))

# Break up the sample text into sentences
sentences = []
if os.path.exists(SAMPLE_FILE):
	try:
		with open(SAMPLE_FILE, 'r') as fh:
			doc = fh.read()
			sentences = doc.split('.')
	except Exception as err:
		print("Could not read the sample file. Threw exception:\n\t{}".format(err))
else:
	print("Could not find the sample file [{}]".format(SAMPLE_FILE))

# Make sure each sentenct meets the required aspects of a text block for analysis
#   - must be at least 1 character long
#   - cannot be more than 5,000 bytes
text_blocks = []
if len(sentences) > 0:
	# Make sure that the sample paragraphs are less than the 5,000 bytes limit
	for sentence in sentences:
		sentence = sentence.strip()
		if len(sentence) <= 5000 and len(sentence) > 0:
			text_blocks.append(sentence)
		else:
			print("Skipping sentence due to length restrictions") # in a production workflow, you would break up longer text into seperate blocks
			if len(sentence) <= 0:
				print("   Sentence too small")
			else:
				print("   Sentence too large")
else:
	print("No sentence to process")

print(text_blocks)

# Send the text blocks to Amazon Comprehend for sentiment analysis
response = None
if len(text_blocks) >= 1 and len(text_blocks) <= 25: # we can only send 1-25 text blocks as a batch
	response = api.batch_detect_syntax(TextList=text_blocks, LanguageCode="en") # we know the sample is in English but could also use detect_dominant_language to get the code
else:
	print("No text blocks available to send to Amazon Comprehend")

# Present the results
if response:
	print("---------------------------------------------")
	for result in response['ResultList']:
		print("{}{}Score".format("Text".ljust(15), "Tag".ljust(10)))
		print("---------------------------------------------")
		for token in result['SyntaxTokens']:
			print("{}{}{}".format(token['Text'].ljust(15), token['PartOfSpeech']['Tag'].ljust(10), token['PartOfSpeech']['Score']))
else:
	print("No response from Amazon Comprehend")