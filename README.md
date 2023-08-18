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

This template comes with a playbook to install the dependencies (boto3 python module & sqs_stats.py) on the zabbix server :

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

The last step to do for having the template working is to import the template itself to your zabbix server.
This can be done with [util_zabbix chef cookbook](https://github.com/julienlevasseur/util_zabbix) :

```ruby
# This cookbook file is the template in its XML format

cookbook_file '/tmp/sqs_zabbix_template.xml' do
  source 'sqs_zabbix_template.xml'
  owner 'zabbix'
  group 'zabbix'
  mode '0644'
  action :create
end

rules = {
  templates: {
    createMissing: true,
    updateExisting: true
  },
  items: {
    createMissing: true,
    updateExisting: true
  }
}

# Creation

util_zabbix_configuration 'config_test' do
  rules rules
  source lazy { ::File.open('/tmp/sqs_zabbix_template.xml', 'rb').read }
  not_if {template_exists?('Template AWS SQS')}
end
```

