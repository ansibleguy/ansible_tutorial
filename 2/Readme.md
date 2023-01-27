# What is Ansible

Ansible is used to automate it administration.

What systems can Ansible target?

* Linux/Unix-like
* [Cloud providers](https://docs.ansible.com/ansible/2.8/modules/list_of_cloud_modules.html) like Amazon AWS, Microsoft Azure, Google Cloud
* [Windows](https://docs.ansible.com/ansible/2.8/modules/list_of_windows_modules.html)
* [Network devices](https://docs.ansible.com/ansible/2.8/modules/list_of_network_modules.html) like Switches, Firewalls
* [Storage](https://docs.ansible.com/ansible/2.8/modules/list_of_storage_modules.html) like NetApp, PureStorage
* [Databases](https://docs.ansible.com/ansible/2.8/modules/list_of_database_modules.html) like MySQL/MariaDB, PostgreSQL
* [Monitoring systems](https://docs.ansible.com/ansible/2.8/modules/list_of_monitoring_modules.html) like Zabbix
* [And many more](https://docs.ansible.com/ansible/2.8/modules/modules_by_category.html)

## Third party

There are also third-party community modules that allow you to manage even more systems!

Per example:

* [ansibleguy.opnsense](https://github.com/ansibleguy/collection_opnsense) => allows you to manage [OPNSense firewalls](https://opnsense.org/)

## Connection types

For Ansible to manage its target system it needs to connect to them.

Most of the time one will use the system-specific default connection-types:

* Linux/Unix-like via [OpenSSH](https://docs.ansible.com/ansible/latest/inventory_guide/connection_details.html)
* Cloud services via API
* Windows via [WinRM/Windows Remote Management](https://docs.ansible.com/ansible/latest/os_guide/windows_winrm.html)

## Sources

* [Ansible Datasheet](https://www.redhat.com/en/resources/ansible-automation-platform-datasheet)
* [How Ansible works](https://www.ansible.com/overview/how-ansible-works)
* [Documentation](https://docs.ansible.com/ansible/latest/index.html)
