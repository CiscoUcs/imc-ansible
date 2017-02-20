#!/usr/bin/env python

from ansible.module_utils.basic import *

DOCUMENTATION = '''
---
module: cisco_imc_ipmi
short_description: Configures ipmi a Cisco IMC Server
version_added: "0.9.0.0"
description:
    - Configures the Serial Over Lan(SOL) service on a Cisco IMC Server
Input Params:
    priv:
        description: Privilege to be used
        required: False
        choices: ["admin", "user", "read-only"]
        default: 'user'

    key:
        description: Hexadecimal Key to be used for authentication
        required: False

    server_id:
        description: Server Id to be specified for C3260 platforms
        choices: ["admin", "read-only", "user"]
        default: "read-only"
        required: False

    state:
        description: Used to create or delete the SOL console
        choices: ["present", "absent"]
        default: "present"
        required: False

requirements: ['imcsdk']
author: "Branson Matheson (brmathes@cisco.com)"
'''

EXAMPLES = '''
- name: enable IPMI
  cisco_imc_ipmi:
    priv: "admin"
    state: "present"
    ip: "192.168.1.1"
    username: "admin"
    password: "password"
'''

def setup_ipmi(server, module):
    from imcsdk.apis.admin.ipmi import ipmi_disable
    from imcsdk.apis.admin.ipmi import ipmi_enable
    from imcsdk.apis.admin.ipmi import is_ipmi_enabled

    ansible = module.params
    priv, key, server_id = (ansible["priv"],
                            ansible["key"], ansible["server_id"])

    exists = is_ipmi_enabled(server, server_id=server_id)
    
    if ansible["state"] == "present":
        if exists:
            return False
        if not module.check_mode:
            ipmi_enable(server, priv=priv, key=key, server_id=server_id)
    else:
        if not exists:
            return False
        if not module.check_mode:
            ipmi_disable(server, server_id=server_id)
    return True


def setup(server, module):
    results = {}
    err = False

    try:
        results["changed"] = setup_ipmi(server, module)

    except Exception as e:
        err = True
        results["msg"] = "setup error: %s " % str(e)
        results["changed"] = False

    return results, err


def main():
    from ansible.module_utils.cisco_imc import ImcConnection
    module = AnsibleModule(
        argument_spec=dict(
            key=dict(required=False, type='str', default='0'*40),
            server_id=dict(required=False, type='int', default=1),
            priv=dict(required=False, default="read-only",
                      choices=["admin", "read-only", "user"], type='str'),
            state=dict(required=False, default="present",
                       choices=["present", "absent"], type='str'),

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
        supports_check_mode=True
    )

    conn = ImcConnection(module)
    server = conn.login()
    results, err = setup(server, module)
    conn.logout()
    if err:
        module.fail_json(**results)
    module.exit_json(**results)


if __name__ == '__main__':
    main()
