<a href="https://github.com/ansible-community/molecule">
  <img src="https://repository-images.githubusercontent.com/46383942/687a7000-5c7e-11e9-8235-51e9db9bfd68" alt="RedHat - Ansible" width="400"/>
</a>

# Molecule

[Molecule](https://molecule.readthedocs.io/en/latest/) is a framework to run automated tests for Ansible playbooks/roles.

Here I will go into how to set it up and use it. (_basically_)

----

## Install

Install testing tools:

```bash
pip3 install molecule molecule-docker
```

----

## Running

```bash
cd PATH/TO/ROLE  # p.e. "cd /home/guy/ansible/roles/infra_wireguard"

# to run build the test instances, run the tests and clean up afterwards
molecule test
# for troubleshooting
molecule create
# now we can run the actual playbook as many times as we need/want
molecule converge
# test it
molecule verify
# clean it up when we finished troubleshooting
molecule destroy
```

### AnsibleGuy Roles

AnsibleGuy Roles use Docker as testing-platform.

These steps have to be performed before running the tests:

1. Add the 'molecule-docker.local' DNS-Record to your '/etc/hosts' file and point it to your docker-server to use.
2. You will have to add the 'DOCKER_HOST' environmental variable:
```bash
export DOCKER_HOST="tcp://molecule-docker.local:2375"
```

----

## Platform

Molecule dynamically creates VMs or Containers that are used as target for you Ansible playbook to test.

There are some options to choose from:

* Official community drivers

  * [LibVirt](https://github.com/ansible-community/molecule-libvirt) (_KVM virtualization_)
  * [Docker](https://github.com/ansible-community/molecule-docker)
  * [VMWare](https://github.com/ansible-community/molecule-vmware)
  * [Vagrant](https://github.com/ansible-community/molecule-vagrant)
  * [Podman](https://github.com/ansible-community/molecule-podman)
  * [OpenStack](https://github.com/ansible-community/molecule-openstack)
  * [Google Cloud Engine](https://github.com/ansible-community/molecule-gce)
  * [AWS EC2](https://github.com/ansible-community/molecule-ec2)

* Additional drives
  * [Proxmox](https://github.com/meffie/molecule-proxmox)


There are some usage differences between those platforms.

I'll only go into the details of platforms I've experience with.

### Docker

You need a docker server/instance to deploy the test-servers to.

### Install
Install docker as described [here](https://docs.docker.com/engine/install/ubuntu/)

```bash
sudo apt-get update
sudo apt-get -y install ca-certificates curl gnupg lsb-release
```
Add the repository
```bash
# ubuntu
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
# debian
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

### Configure

Either way - the docker server must have the following setting configured in '/etc/docker/daemon.json':

```bash
{"cgroup-parent": "docker.slice"}
```

Restart docker after adding that setting. This allows systemd to work inside the container without mapping cgroup manually.

For further information see: [serverfault.com](https://serverfault.com/questions/1053187/systemd-fails-to-run-in-a-docker-container-when-using-cgroupv2-cgroupns-priva)

#### Locally

This is only recommended if you have powerful hardware and/or very simple role-tests.

Some of my roles use 10+ containers and therefor use a good amount of RAM/CPU at peak times.

You will have to set-up docker as described [here](https://docs.docker.com/engine/security/rootless/).

Switch the docker_host to your local one. (_${role}/molecule/default/molecule.yml_)
```yaml
docker_host: 'unix://var/run/docker.sock'  # localhost
```

#### Remote

Installation
```bash
sudo apt-get -y install docker-ce-cli
```

As mentioned before/above - we recommend running the testing on a server.

You might want to consider using the [docker role](https://github.com/ansibleguy/infra_docker_minimal) to provision a docker server as a vm.

You will have to configure the ip-address to your docker-server. (_${role}/molecule/default/molecule.yml_)
```yaml
docker_host: 'tcp://IP:PORT'  # p.e. tcp://172.17.0.50:2375
```

But it seems like the docker module does not get the molecule config. (_Still connecting to localhost_)

Therefore, you will have to set this environmental variable in addition:

```bash
export DOCKER_HOST='tcp://IP:PORT'
```
