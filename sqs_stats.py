#!/usr/bin/env python

import os
import sys
import boto3
import datetime
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-q', '--queuename', dest='queue_name', help='QueueName')
parser.add_option('-a', '--access-key-id', dest='acess_key_id',
	help='AWS Access Key Id')
parser.add_option('-s', '--secret_access_key', dest='secret_access_key',
	help='AWS Secret Access Key')
parser.add_option('-m', '--metric', dest='metric',
	help='SQS Cloudwatch Metric')
parser.add_option("-r", "--region", dest="region",
	help="SQS region")

(options, args) = parser.parse_args()

if (options.queue_name == None):
	parser.error("-q QueueName is required")
if (options.acess_key_id == None):
	parser.error("-a AWS Access Key is required")
if (options.secret_access_key == None):
	parser.error("-s AWS Secret Key is required")
if (options.metric == None):
	parser.error("-m SQS Cloudwatch Metric is required")

metrics = {
	"SentMessageSize":{"type":"float", "value":None},
	"ApproximateNumberOfMessagesDelayed":{"type":"float", "value":None},
	"NumberOfMessagesSent":{"type":"float", "value":None},
	"NumberOfEmptyReceives":{"type":"float", "value":None},
	"ApproximateNumberOfMessagesVisible":{"type":"float", "value":None},
	"ApproximateNumberOfMessagesNotVisible":{"type":"float", "value":None},
	"NumberOfMessagesReceived":{"type":"float", "value":None},
	"ApproximateAgeOfOldestMessage":{"type":"float", "value":None},
	"NumberOfMessagesDeleted":{"type":"float", "value":None}
}
end = datetime.datetime.utcnow()
start = end - datetime.timedelta(minutes=5)

# If region is not provided, set it to a default value
if (options.region == None):
	region = 'us-east-1'
else:
	region = options.region
os.environ['AWS_DEFAULT_REGION'] = region

cloudwatch = boto3.client(
	'cloudwatch',
	aws_access_key_id=options.acess_key_id,
	aws_secret_access_key=options.secret_access_key
)

for k,v in metrics.items():
	if (k == options.metric):
		try:
			res = cloudwatch.get_metric_statistics(
				Namespace='AWS/SQS',
				MetricName=k,
				Dimensions=[
					{
						'Name': 'QueueName',
						'Value': options.queue_name
					},
				],
				StartTime=start,
				EndTime=end,
				Period=300,
				Statistics=[
					'Average',
				],
			)
		except Exception, e:
			print "[ERROR] %s" % e
			sys.exit(1)
		average = res['Datapoints'][-1]["Average"]

		print "%s" % (average)
		break
