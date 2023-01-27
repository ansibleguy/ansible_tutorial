#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace
from json import dumps as json_dumps


class TemplateInventory:
    def __init__(self, args: Namespace):
        self.args = args
        self.inventory = {}

    @property
    def result(self) -> str:
        return json_dumps(self.inventory)

    def example_inventory(self):
        return {
            'python_hosts': {
                'hosts': ['10.220.21.24', '10.220.21.27'],
                'vars': {
                    'ansible_ssh_user': 'projectuser',
                }
            },
            '_meta': {
                'hostvars': {
                    '10.220.21.24': {
                        'host_specific_var': 'testhost'
                    },
                    '10.220.21.27': {
                        'host_specific_var': 'towerhost'
                    }
                }
            }
        }

    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-l', '--list', help='Generate whole inventory')
    parser.add_argument('-h', '--host', help='Generate inventory of specific host')
    print(
        TemplateInventory(
            args=parser.parse_args(),
        ).result
    )
