# Intro to Ansible

----

## Sources

* [Ansible Datasheet](https://www.redhat.com/en/resources/ansible-automation-platform-datasheet)
* [How Ansible works](https://www.ansible.com/overview/how-ansible-works)
* [Documentation](https://docs.ansible.com/ansible/latest/index.html)

----

## What is Ansible

Ansible is used to automate IT administration.

Its [base-product is Open-Source](https://github.com/ansible/ansible) and **free to use**.

There is also an Open-Source web-based control-environment named ['Ansible AWX'](https://github.com/ansible/awx).

For enterprise-use RedHat offers a product named ['Ansible Automation Platform'](https://www.redhat.com/en/technologies/management/ansible) that is Closed-Source and must be licensed.

### Arguments

**Practical examples** of use-cases are:
* Provisioning/managing IT-services from small- up to large-scale
  * [Webserver nodes](https://github.com/ansibleguy/infra_nginx)
  * [Database clusters](https://github.com/ansibleguy/infra_mariadb)
  * Configuration of [host-](https://github.com/ansibleguy/infra_nftables) and [network-firewalls]((https://github.com/ansibleguy/collection_opnsense))
  * Configuration of [local users](https://github.com/ansibleguy/linux_users) or identity providers
* Generating and renewing [certificates](https://github.com/ansibleguy/infra_certs) for encrypted connectivity
* Preparing for the worst-case - automate your disaster-recovery

**Why automate?**
* [Scalability](https://www.ansible.com/blog/large-scale-deployments-using-ansible) 
* Allows you to implement [Infrastructure-as-Code](https://en.wikipedia.org/wiki/Infrastructure_as_code)
  * [Benefits](https://www.redhat.com/en/topics/automation/what-is-infrastructure-as-code-iac#benefits-of-iac):
    * Cost reduction
    * Increase in speed of deployments
    * Reduce errors
    * Improve infrastructure consistency
    * Having the configuration of all your IT-systems in one place and versioning it using a [Version Control System](https://en.wikipedia.org/wiki/Version_control) like [Git](https://git-scm.com/)
* Abstract the complexity of administration to a single click or button press
* Simplifying/empowering [Continuous integration/Continuous delivery](https://www.redhat.com/en/topics/devops/what-is-ci-cd)
* Testing of your automation can also be automated - see: [Molecule](https://github.com/ansibleguy/ansible_tutorial/blob/main/99/Molecule.md)
  * Making system-upgrades easier
  * Finding and correcting bugs before they hit your actual infrastructure

It is **designed to**:
* work in an agentless manner
  * need few to none requirements on the target systems
* operations being [idempotent](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html#desired-state-and-idempotency) (_checking if operations need to be performed before executing them_)
* combine variable host- & group-configuration with templated tasks
* verify the target state is as desired

----

## Target systems

What systems can Ansible target?

* Linux/Unix-like
* [Cloud providers](https://docs.ansible.com/ansible/2.8/modules/list_of_cloud_modules.html) like Amazon AWS, Microsoft Azure, Google Cloud
* [Windows](https://docs.ansible.com/ansible/2.8/modules/list_of_windows_modules.html)
* [Network devices](https://docs.ansible.com/ansible/2.8/modules/list_of_network_modules.html) like Switches, Firewalls
* [Storage](https://docs.ansible.com/ansible/2.8/modules/list_of_storage_modules.html) like NetApp, PureStorage
* [Databases](https://docs.ansible.com/ansible/2.8/modules/list_of_database_modules.html) like MySQL/MariaDB, PostgreSQL
* Virtualization Platforms like [VMWare](https://docs.ansible.com/ansible/latest/collections/vmware/vmware_rest/index.html#plugins-in-vmware-vmware-rest), 
[Proxmox](https://docs.ansible.com/ansible/latest/collections/community/general/index.html#stq=proxmox&stp=1),
[Kubernetes](https://docs.ansible.com/ansible/latest/collections/kubernetes/),
[LibVirt](https://docs.ansible.com/ansible/latest/collections/community/libvirt/index.html)
* [Monitoring systems](https://docs.ansible.com/ansible/2.8/modules/list_of_monitoring_modules.html) like Zabbix
* [And many more](https://docs.ansible.com/ansible/2.8/modules/modules_by_category.html)

### Third party contributions

There are also third-party community modules that allow you to manage even more systems!

Per example:

* [ansibleguy.opnsense](https://github.com/ansibleguy/collection_opnsense) => allows you to manage [OPNSense firewalls](https://opnsense.org/)

----

## Connection types

For Ansible to manage its target system it needs to connect to them.

Most of the time one will use the system-specific default connection-types:

* Linux/Unix-like via [OpenSSH](https://docs.ansible.com/ansible/latest/inventory_guide/connection_details.html)
* Cloud services via APIs/SDKs
* Windows via [WinRM/Windows Remote Management](https://docs.ansible.com/ansible/latest/os_guide/windows_winrm.html)
* Network devices via OpenSSH
* Many systems via APIs (_mainly HTTPS/REST_)

<a href="https://www.ansible.com/overview/how-ansible-works">
  <img src="https://www.ansible.com/hs-fs/hubfs/graphic-crop.jpg?width=500&name=graphic-crop.jpg" alt="RedHat - Ansible" width="400"/>
</a>

### Advanced tricks

There are also some advanced tricks you can use for connecting to target systems:

* [SSH Tunneling to provision private targets through a jump-host](https://www.jeffgeerling.com/blog/2022/using-ansible-playbook-ssh-bastion-jump-host)
* [Using automation-mesh to add connection proxies](https://www.ansible.com/blog/peeling-back-the-layers-and-understanding-automation-mesh)

----

## Scripting vs Automation

If you have got some experience administrating IT-systems you might think: 

> Why use a large framework like Ansible if I can just script it?
> Ansible has much more overhead and is slower than basic bash/powershell scripts..

It's true - Ansible has more overhead and is slower than scripting.

But that has its reasons.

----

### Features

Ansible provides many features that help you prevent mistakes and/or errors:

* **Simplicity**:
  * Ansible 'scripts' are written in [YAML Syntax](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html).
This format makes it really easy to read tasks/roles/playbooks and understand what is going on.
  * Even people without a background in programming or advanced-scripting are able to understand and write most tasks.
* [**Check-Mode**](https://docs.ansible.com/ansible/2.9/user_guide/playbooks_checkmode.html):
  * Ansible Modules can be executed in check-mode to show you what WOULD BE changed without actually applying those changes. 
  * That is pretty useful if you want to test some new functionality or just want to make sure nothing will break.
* [**Diff-Mode**](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_checkmode.html#using-diff-mode):
  * Most Ansible Modules have implemented the 'difference' flag/mode - it enables you to see what exact changes are applied.
  * This feature is really useful in check-mode.
  * If the execution did unintentionally break something it helps you to analyze what went wrong.
* [**Error handling**](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_error_handling.html):
  * Ansible give you many options to configure error-handling.
  * Most Ansible Modules will return useful information whenever they fail just in case you want to soft-handle its failure.
* **Validation**
  * [Parameters passed to Ansible Modules](https://docs.ansible.com/ansible/latest/dev_guide/developing_program_flow_modules.html#argument-spec) are checked for basic validity and formatted as a given type.
That can catch user- or configuration-errors before they have any negative impact.
  * [Parameters passed to Ansible Roles](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html#role-argument-validation) can also be validated that way.
* **Secrets**
  * Ansible has a feature named [Ansible-Vault](https://docs.ansible.com/ansible/latest/vault_guide/index.html) that provides a way to encrypt and manage sensitive data such as passwords.
  * You can also use centralized 3th-party vault-solutions like [Hashicorp Vault](https://docs.ansible.com/ansible/2.9/plugins/lookup/hashi_vault.html).
  * Sensitive data can also be protected from being logged in clear-text using the ['no_log' parameter](https://docs.ansible.com/ansible/latest/reference_appendices/logging.html).
Most Modules also implement this for secrets you pass to them.
  * Secrets that are [prompted at runtime](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_prompts.html#hashing-values-supplied-by-vars-prompt) can also be encrypted.

----

### Example

In the following example I will show you the difference between [Bash-scripting](https://www.freecodecamp.org/news/shell-scripting-crash-course-how-to-write-bash-scripts-in-linux/) and Ansible.

#### Info

What will be configured in this example:

* Installing web-application dependencies
  * MariaDB database server
  * Apache2 webserver
* Configuration
  * Apache2
    * Modules
    * Virtualhost
  * MariaDB
    * Config
    * Import database schema
    * Users
  * Copy/update web application
  * [Systemd Timer](https://wiki.archlinux.org/title/systemd/Timers) to update some data on a schedule


Compare the Bash and Ansible example and think about it: which one would you rather maintain/work with?

#### Prerequisites

* The script and Ansible-playbook needs to be executed on a controller node
* The controller needs to have network-access to the target-system (_ssh port_)
* The executing user needs to be able to
  * connect to the target-system via SSH
  * run commands with root-privileges on the target-system using 'sudo'

#### Bash

If a single command will fail, the whole script will stop executing.

See: [Example Bash](https://github.com/ansibleguy/ansible_tutorial/blob/main/2/Example_Bash.md)

#### Ansible

See: [Example Ansible](https://github.com/ansibleguy/ansible_tutorial/blob/main/2/Example_Ansible.md)
