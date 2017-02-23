#!/usr/bin/env python

from ansible.module_utils.basic import *

DOCUMENTATION = '''
---
module: cisco_imc_logout
short_description: Logout of a IMC server
version_added: "0.9.0.0"
description:
  - Logs out of a cisco IMC server
  - Executes the aaaLogout method provided by the IMC Server

requirements: ['imcsdk']
author: "Vikrant Balyan(vvb@cisco.com)"
'''

EXAMPLES = '''
- name: login to a IMC server
  hosts: 127.0.0.1
  connection: local
  tasks:
  - name: logout from the server
    cisco_imc_logout:
      server=frozen_server_handle
'''


def imc_logout(module):
    results = {}
    results['changed'] = False

    imc = module.params.get('server')
    if imc:
        imc.logout()
        return results, False

    results["msg"] = "server is a required parameter"
    return results, True


def main():
    module = AnsibleModule(
        argument_spec=dict(
            server=dict(required=True)
        ),
        supports_check_mode=True
    )

    results, err = imc_logout(module)
    if err:
        module.fail_json(**results)
    module.exit_json(**results)


if __name__ == '__main__':
    main()
