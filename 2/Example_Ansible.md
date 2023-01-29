# Example - Ansible

The Ansible collection 'community.mysql' and 'community.general' will need to be installed on the controller node!

*NOTE: I did not test this playbook completely*

## Inventory

### Hosts

File: inventory/hosts.yml

```yaml
all:
  hosts:
    srv1:
  children:
    web_app1:
      hosts:
        srv1:
```

### Host-specific variables

File: inventory/host_vars/srv1.yml

```yaml
ansible_port: 22  # ssh port
ansible_user: 'user'  # ssh user
ansible_host: '192.168.0.1'  # target server ip

app1_cnf:
  path: '/var/www/app1'
  update_svc: 'app1-update'
  db:
    name: 'app1'
    users:
      user1:
        pwd: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          31363066336534336363653462386335623031303833333061646364326638653262356563363138
          3463393330356162316437343533303463613235353834610a383766366133626332653332363437
          34376431323634636564353430393365346165386332383061313033666466303436386362663933
          6433613638626337300a646432353063313264313835353362336637353263663936303833376439
          39303230316366333631316239313662633565376331326335323365316161313936613036653938
          6664653433343232333832636338656263366562353837633637
        privs: 'ALL'
      user2:
        pwd: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          66343461613165626562323935356166636462343761313538373537653933386663633137383433
          6530383933633437366264363130306663626561313335350a363930633737633431333666653837
          34653462663839623636313332343566363435636566633664653939373564363234646633656663
          3935626339373935650a353134323734396261396338396663663933653232336563626338386163
          37383930303362633264643339636162613932383133303933623261353935313262
        privs: 'SELECT'
```

## Playbook

```yaml
- name: Installation
  hosts: web_app1  # only execute tasks on servers in group 'web_app1'
  become: true  # run all commands with root privileges
  tasks:
    - name: Installing packages
      ansible.builtin.apt:
        name: ['mariadb-client', 'mariadb-server', 'apache2', 'wget']

    - name: Starting and enabling services
      ansible.builtin.systemd:
        name: "{{ item }}"
        enabled: true
        state: started
      loop:
        - 'apache2.service'
        - 'mariadb.service'

- name: Database
  hosts: web_app1
  become: true
  tasks:
    - name: Configuring MariaDB
      ansible.builtin.template:
        src: 'templates/mariadb.cnf.j2'
        dest: '/etc/mariadb/mariadb.cnf'
        owner: 'root'
        group: 'mysql'
        mode: 0640
      register: mdb_cnf

    - name: Reloading MariaDB if config changed
      ansible.builtin.systemd:
        name: 'mariadb.service'
        state: reloaded
      when: mdb_cnf.changed

    - name: Checking if database is empty
      community.mysql.mysql_query:
        login_db: "{{ app1_cnf.db.name }}"
        query: "SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA = '{{ app1_cnf.db.name }}')"
      register: mdb_empty

    - name: Copying database schema if needed
      ansible.builtin.template:
        src: 'files/db.sql'
        dest: '/tmp/db.sql'
        owner: 'root'
        group: 'root'
        mode: 0640
      when: mdb_empty['query_result'][0][0]['count(*)'] | int == 0

    - name: Importing database schema if db is empty
      community.mysql.mysql_db:
        name: "{{ app1_cnf.db.name }}"
        state: import
        force: true
        single_transaction: true
        use_shell: true
        target: '/tmp/db.sql'
      when: mdb_empty['query_result'][0][0]['count(*)'] | int == 0

    - name: Creating MariaDB users
      community.mysql.mysql_user:
        name: "{{ item.key }}"
        host: 'localhost'
        password: "{{ item.value.pwd }}"
        update_password: 'on_create'
        priv: "{{ item.value.priv }}"
        state: 'present'
      with_dict: "{{ app1_cnf.db.users }}"

- name: Apache2
  hosts: web_app1
  become: true
  tasks:
    - name: Removing default sites
      ansible.builtin.file:
        state: absent
        path: "{{ item }}"
      loop:
        - '/etc/apache2/sites-enabled/000-default.conf'
        - '/etc/apache2/sites-enabled/default-ssl.conf'

    - name: Copying web application data
      ansible.builtin.copy:
        src: 'files/app1/'
        dest: "{{ app1_cnf.path }}/"
        mode: 0644
        directory_mode: 0755
        owner: 'root'
        group: 'www-data'

    - name: Configuring Apache2 site
      ansible.builtin.template:
        src: 'templates/apache_site.conf.j2'
        dest: '/etc/apache2/sites-enabled/site.conf'
        owner: 'root'
        group: 'www-data'
        mode: 0640
      register: a2_cnf

    - name: Enabling Apache2 modules
      community.general.apache2_module:
        state: present
        name: "{{ item }}"
      loop:
        - 'a2enmod'
        - 'ssl'
        - 'headers'
        - 'rewrite'
        - 'http2'
      register: a2_mods

    - name: Reloading Apache2 if config/mods changed
      ansible.builtin.systemd:
        name: 'apache2.service'
        state: reloaded
      when: a2_cnf.changed or a2_mods.changed

- name: Update service
  hosts: web_app1
  become: true
  tasks:
    - name: Adding Systemd Timer and Service
      ansible.builtin.template:
        src: "templates/systemd.{{ item }}.j2"
        dest: "/etc/systemd/system/{{ app1_cnf.update_svc }}.{{ item }}"
        owner: 'root'
        group: 'root'
        mode: 0644
      loop:
        - 'service'
        - 'timer'

    - name: Starting and enabling update timer
      ansible.builtin.systemd:
        name: "{{ app1_cnf.update_svc }}.timer"
        enabled: true
        state: started
```

## Execution

```bash
ansible-playbook -D -K -k -i inventory/hosts.yml --ask-vault-pass playbook.yml --limit srv1
# D = diff-mode
# K = ask become password
# k = ask connect password
# i = inventory file
# ask-vault-pass = ask for password that can be used to decrypt ansible-vault encrypted variables at runtime
# playbook.yml = the actual playbook to execute
# limit = only execute playbook targeting host 'srv1'
```
