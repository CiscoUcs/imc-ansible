#!/usr/bin/env python

from ansible.module_utils.basic import *

DOCUMENTATION = '''
---
module: cisco_imc_inventory
short_description: Collect CIMC inventory
version_added: ""
description:
    - Puts CIMC inventory information into cimc_inventory host's variable.

requirements: ['imcsdk']
author: "Nikolay Fedotov (nfedotov@cisco.com)"
'''

EXAMPLES = '''
- name: Gather CIMC inventory
  cisco_imc_inventory:
    ip: "192.168.1.1"
    username: "admin"
    password: "password"
'''


def main():
    from ansible.module_utils.cisco_imc import ImcConnection
    from imcsdk.apis.server.inventory import inventory_get
    module = AnsibleModule(
        argument_spec=dict(
            # ImcHandle
            server=dict(required=False, type='dict'),

            # Imc server credentials
            ip=dict(required=False, type='str'),
            username=dict(required=False, default="admin", type='str'),
            password=dict(required=False, type='str', no_log=True),
            port=dict(required=False, default=None),
            secure=dict(required=False, default=None),
            proxy=dict(required=False, default=None)
        ),
        supports_check_mode=False
    )

    conn = ImcConnection(module)
    server = conn.login()
    inventory = inventory_get(server)
    conn.logout()
    module.exit_json(ansible_facts=dict(cimc_inventory=inventory[server.ip]))


if __name__ == '__main__':
    main()
