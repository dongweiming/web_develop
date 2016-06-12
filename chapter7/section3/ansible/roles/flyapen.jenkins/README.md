# Readme

## Description

*ansible-jenkins* is an [Ansible](http://ansible.cc) role.
Use this role to install Jenkins and install/update plugins.

## Provides

1. Latest Jenkins server
2. Jenkins plugins support

## Requires

1. Ansible 1.4 or higher
2. Debian 7.3 (other deb-based distros should work too)
3. Vagrant (optional)

## Usage

### Get the code

```bash
$ git clone https://github.com/ICTO/ansible-jenkins.git roles
```

The code should reside in the roles directory of ansible ( See [ansible documentation](http://www.ansibleworks.com/docs/playbooks.html#roles) for more information on roles ), in a folder jenkins.

### Create a host file

Following example make ansible aware of the Vagrant box reachable on localhost port 2222.

```bash
$ vi ansible.host
```

with

```ini
[jenkins]
127.0.0.1 ansible_ssh_port=2222 ansible_ssh_user=vagrant ansible_ssh_private_key_file=~/.vagrant.d/insecure_private_key 
```

### Create host specific variables

Make the host_vars directory where *ansible.host* file is located.

```bash
$ mkdir host_vars
```

Create a file in the newly created directory matching your host.

```bash
$ cd host_vars
$ vi 127.0.0.1
```

with

```yaml
---
plugins:
  - 'ldap'
  - 'github'
  - 'translation'
  - 'preSCMbuildstep'
port: 8081
prefix: '/build'
email:
  smtp_host: 'mail.example.com'
  smtp_ssl: 'true'
  default_email_suffix: '@example.com'
```

### Run the playbook


First create a playbook including the jenkins role, naming it jenkins.yml.

```yml
- name: Jenkins
  hosts: jenkins
  sudo: yes
  roles:
    - ansible-jenkins
```

Use *ansible.host* as inventory. Run the playbook only for the remote host *jenkins*. Use *vagrant* as the SSH user to connect to the remote host. *-k* enables the SSH password prompt.

```bash
$ ansible-playbook -i ansible.host jenkins.yml
```

### Example output

```
SSH password:

PLAY [Jenkins] ****************************************************************

GATHERING FACTS ***************************************************************
ok: [127.0.0.1]

TASK: [ansible-jenkins | Install python-software-properties] ******************
ok: [127.0.0.1]

TASK: [ansible-jenkins | Add jenkins apt-key] *********************************
ok: [127.0.0.1]

TASK: [ansible-jenkins | Add Jenkins repository] ******************************
ok: [127.0.0.1]

TASK: [ansible-jenkins | Install dependencies] ********************************
ok: [127.0.0.1] => (item=openjdk-6-jre)
ok: [127.0.0.1] => (item=openjdk-6-jdk)
ok: [127.0.0.1] => (item=git)
ok: [127.0.0.1] => (item=curl)

TASK: [ansible-jenkins | Install Jenkins] *************************************
ok: [127.0.0.1]

TASK: [ansible-jenkins | 10s delay while starting Jenkins] ********************
skipping: [127.0.0.1]

TASK: [ansible-jenkins | Create Jenkins CLI destination directory: /opt/jenkins] ***
ok: [127.0.0.1]

TASK: [ansible-jenkins | Get Jenkins CLI] *************************************
ok: [127.0.0.1]

TASK: [ansible-jenkins | Get Jenkins updates] *********************************
ok: [127.0.0.1]

TASK: [ansible-jenkins | Update-center Jenkins] *******************************
skipping: [127.0.0.1]

TASK: [ansible-jenkins | List plugins] ****************************************
skipping: [127.0.0.1]

TASK: [ansible-jenkins | Install/update plugins] ******************************
skipping: [127.0.0.1] => (item=plugins)

TASK: [ansible-jenkins | List plugins to be updated] **************************
changed: [127.0.0.1]

TASK: [ansible-jenkins | Update plugins] **************************************
skipping: [127.0.0.1]

PLAY RECAP ********************************************************************
127.0.0.1                  : ok=11   changed=1    unreachable=0    failed=0  
```
