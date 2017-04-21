#!/usr/bin/env python

from ansible.module_utils.basic import *


DOCUMENTATION = '''
---
module: cisco_imc_redfish
short_description: Configures redfish on a Cisco IMC Server
version_added: 0.9.0.0
description:
   -  Configures redfish on a Cisco IMC Server
Input Params:

requirements: ['imcsdk']
author: "Rahul Gupta(ragupta4@cisco.com)"
'''


EXAMPLES = '''
- name:
  cisco_imc_redfish:
    state: "present"
    ip: "192.168.1.1"
    username: "admin"
    password: "password"
'''


def _argument_state():
    return dict(
        state=dict(required=False,
                   default="present",
                   choices=['present', 'absent'],
                   type='str'),
    )


def _argument_imc_connection():
    return  dict(
        # ImcHandle
        imc_server=dict(required=False, type='dict'),

        # Imc server credentials
        imc_ip=dict(required=False, type='str'),
        imc_username=dict(required=False, default="admin", type='str'),
        imc_password=dict(required=False, type='str', no_log=True),
        imc_port=dict(required=False, default=None),
        imc_secure=dict(required=False, default=None),
        imc_proxy=dict(required=False, default=None)
    )


def _ansible_module_create():
    argument_spec = dict()
    argument_spec.update(_argument_state())
    argument_spec.update(_argument_imc_connection())

    return AnsibleModule(argument_spec,
                         supports_check_mode=True)


def setup_redfish(server, module):
    from imcsdk.apis.admin.redfish import redfish_enable
    from imcsdk.apis.admin.redfish import redfish_disable
    from imcsdk.apis.admin.redfish import is_redfish_enabled

    ansible = module.params
    exists = is_redfish_enabled(handle=server)

    if ansible["state"] == "present":
        if module.check_mode or exists:
            return not exists, False
        redfish_enable(handle=server)
    else:
        if module.check_mode or not exists:
            return exists, False
        redfish_disable(server)

    return True, False


def setup(server, module):
    results = {}
    err = False

    try:
        results["changed"], err = setup_redfish(server, module)

    except Exception as e:
        err = True
        results["msg"] = "setup error: %s " % str(e)
        results["changed"] = False

    return results, err


def main():
    from ansible.module_utils.cisco_imc import ImcConnection

    module = _ansible_module_create()
    conn = ImcConnection(module)
    server = conn.login()
    results, err = setup(server, module)
    conn.logout()
    if err:
        module.fail_json(**results)
    module.exit_json(**results)


if __name__ == '__main__':
    main()

