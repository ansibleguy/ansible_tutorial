# Installing Ansible

This is a brief overview on how to set-up an Ansible environment.

## Controller vs AWX/Tower

This tutorial shows you how to set-up a simple Ansible controller.

We will not go into the possibility of installing an [Ansible AWX](https://www.ansible.com/community/awx-project) (_Open Source_) or [Ansible Tower](https://access.redhat.com/products/ansible-tower-red-hat) instance (_Closed Source_) that both enable you to use Ansible via a web-interface!

----

## Prerequisites

Ansible needs to run on a linux/unix system! (_[Source](https://docs.ansible.com/ansible/latest/installation_guide/installation_distros.html)_)

### Windows

Microsoft WSL is [not supported](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#control-node-requirements). (_according to my experience it might work somehow, but it's not reliable_)

If you are running on a Windows client-OS you will need to install a Linux virtual machine locally or in your existing virtualization environment.

If you are using an IDE like [PyCharm](https://www.jetbrains.com/pycharm/) to manage your Ansible projects - you might want to map/redirect your local project directories into your VM. (_Ansible will execute them in read-only mode_)

You might not need a GUI installation of linux. Commandline-only will do. Per example: [Debian minimal](https://www.debian.org/CD/netinst/) or [Ubuntu server](https://ubuntu.com/download/server)

### Linux packages

You need Python3 and PIP to run Ansible:

```bash
sudo apt install python3 python3-pip
```

----

## Virtual Environment

You should consider using [python virtual-environments](https://realpython.com/python-virtual-environments-a-primer/) to run Ansible.

```bash
python3 -m pip install virtualenv
python3 -m virtualenv ~/venv_ansible
```

Whenever you want to use ansible or install other dependencies - you will need to activate the environment:

```bash
source ~/venv_ansible/bin/activate

# you can verify it is active by checking which python3 binary is currently used
which python3
> ~/venv_ansible/bin/python3
```

----

## Ansible

```bash
python3 -m pip install ansible
```

### Collections / Roles

```bash
# roles
ansible-galaxy install ansibleguy.infra_wireguard

## from github
ansible-galaxy install git+https://github.com/ansibleguy/sw_zabbix

## install to a specific path
ansible-galaxy install --roles-path ./roles ansibleguy.infra_wireguard

# collections
ansible-galaxy collection install ansibleguy.opnsense

## from github
ansible-galaxy collection install git+https://github.com/ansibleguy/collection_opnsense

## install to a specific path
ansible-galaxy collection install ansibleguy.opnsense -p ./collections
```

You can also save your requirements to a file:

```yaml
---

collections:
  - name: 'community.crypto'

  - name: 'https://github.com/ansibleguy/collection_opnsense.git'
    type: 'git'
    version: '1.1.0'  # branch, tag/release, commit

roles:
  - src: 'ansibleguy.infra_certs'

  - name: 'ansibleguy.infra_nftables'
    src: 'https://github.com/ansibleguy/infra_nftables'
```

See also: [Roles](https://galaxy.ansible.com/docs/using/installing.html#installing-multiple-roles-from-a-file) | [Collections](https://docs.ansible.com/ansible/devel/collections_guide/collections_installing.html#installing-collections-with-ansible-galaxy)

And install them:

```bash
# roles
ansible-galaxy install -r requirements.yml

# collections
ansible-galaxy collection install -r requirements.yml
```

----

## Linting

Using linting-checks helps you to ensure your code/scripts comply with existing best-practices.

### Install

```bash
python3 -m pip install ansible-lint yamllint pylint
```

### Configure

You might have the need to disable or modify some tests.

#### Ansible-Lint

See: [Documentation](https://ansible-lint.readthedocs.io/configuring/)

#### Yamllint

See: [Documentation](https://yamllint.readthedocs.io/en/stable/configuration.html)

#### PyLint

Generate the default config for your current version of pylint:

```bash
pylint --generate-rcfile > .pylintrc
```

See: [Documentation](https://yamllint.readthedocs.io/en/stable/configuration.html)

### Run

You should create a script that runs those commands in the base-directory of your project:

```bash
#!/bin/bash
set -e
ansible-lint -c .ansible-lint.yml
yamllint .
pylint --recursive=y
```

An extended sample-script can be found [here](https://github.com/ansibleguy/videos/blob/main/2/structure/extended/script/lint.sh).
