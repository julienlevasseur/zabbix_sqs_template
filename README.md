zabbix_sqs_template
===================

AWS SQS Template for Zabbix

# Overview

The SQS Zabbix Template monitor the following SQS metrics :

- SentMessageSize
- ApproximateNumberOfMessagesDelayed
- NumberOfMessagesSent
- NumberOfEmptyReceives
- ApproximateNumberOfMessagesVisible
- ApproximateNumberOfMessagesNotVisible
- NumberOfMessagesReceived
- ApproximateAgeOfOldestMessage
- NumberOfMessagesDeleted

Each item has is own graph but only the `ApproximateAgeOfOldestMessage` have a trigger (switching to PROBLEM if the oldest message is older than 24h).

Each queue is considered as a host.

# Installation on the Zabbix server

This template come with a playbook to install the dependencies (boto3 python module & sqs_stats.py) on the zabbix server :

```bash
ansible-playbook installation_playbook.yml --extra-vars "target=$host"

PLAY [zabbix] ******************************************************************

TASK [setup] *******************************************************************
ok: [zabbix]

TASK [Install boto3 python module] *********************************************
changed: [zabbix]

TASK [Send the sqs_stats.py file] **********************************************
changed: [zabbix]

PLAY RECAP *********************************************************************
zabbix                     : ok=3    changed=2    unreachable=0    failed=0
```

The last step to do for having the template working is to import the template himself to your zabbix server.