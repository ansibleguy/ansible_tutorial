# Basic Ansible Usage

In this video we will go through the basics n how to use Ansible and some Tips & Tricks.

## Documentation

* [Directory Structure](https://docs.ansible.com/ansible/2.8/user_guide/playbooks_best_practices.html#directory-layout)
  * [Roles](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html#role-directory-structure)
  * [Collections](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_structure.html)
* [Plugins](https://docs.ansible.com/ansible/latest/plugins/plugins.html)

## Structure

See: [structure](https://github.com/ansibleguy/videos/blob/main/2/structure/)

```bash
├── collections  # local collections
├── files  # files to copy
├── filter_plugins  # custom jinja2 filters written in python3
├── inventories  # config
│   ├── env1  # environmental sub-section
│   │   ├── group_vars  # variables shared by groups
│   │   └── host_vars  # host-specific variables
│   └── env2
│       ├── group_vars
│       └── host_vars
├── roles  # roles
│   └── role1
│       ├── defaults  # default values to be overwritten
│       ├── files  # files to be copied
│       ├── filter_plugins  # custom jinja2 filters
│       ├── handlers  # tasks to be run after something changed
│       ├── meta  # used to define what the role does
│       ├── molecule  # can be used to run automated tests
│       ├── tasks  # tasks to be executed
│       ├── templates  # jinja2-templated files to be copied
│       └── vars  # variables used by the role
├── tasks  # globally available tasks
└── vars  # vars to be included by playbooks
```

Some more directories are available in the playbook and role scope. Like 'library', 'module_utils' and 'lookup_plugins'.
