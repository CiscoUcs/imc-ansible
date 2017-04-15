#!/usr/bin/env python

from ansible.module_utils.basic import *


DOCUMENTATION = '''
---
module: cisco_imc_snmp
short_description: Configures SNMP on a Cisco IMC Server
version_added: 0.9.0.0
description:
   -  Configures the SNMP on a Cisco IMC Server
Input Params:
    community:
        description: community name
        required: False
    privilege:
        description: SNMP community access
        required: False
        choices: ['disabled', 'limited', 'full']
        default: "disabled"
    trap_community:
        description: community to be used when generating traps
        required: False
    sys_contact:
        description: system contact
        required: False
    sys_location:
        description: system location
        required: False
    port:
        description: SNMP port
        required: False
        default: "161"

requirements: ['imcsdk']
author: "Rahul Gupta(ragupta4@cisco.com)"
'''


EXAMPLES = '''
- name:
  cisco_imc_snmp:
    community:
    privilege:
    trap_community:
    sys_contact:
    sys_location:
    port:
    state: "present"
    ip: "192.168.1.1"
    username: "admin"
    password: "password"
'''


def _argument_mo():
    return dict(
                community=dict(required=False, type='str'),
                com2_sec=dict(required=False, type='str', choices=['disabled', 'limited', 'full'], default="disabled"),
                trap_community=dict(required=False, type='str'),
                sys_contact=dict(required=False, type='str'),
                sys_location=dict(required=False, type='str'),
                port=dict(required=False, type='str', default="161"),
    )


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
    argument_spec.update(_argument_mo())
    argument_spec.update(_argument_state())
    argument_spec.update(_argument_imc_connection())

    return AnsibleModule(argument_spec,
                         supports_check_mode=True)


def _get_mo_params(params):
    from ansible.module_utils.cisco_imc import ImcConnection
    args = {}
    for key in params:
        if (key == 'state' or
            ImcConnection.is_login_param(key) or
            params.get(key) is None):
            continue
        args[key] = params.get(key)
    return args


def setup_snmp(server, module):
    from imcsdk.apis.admin.snmp import snmp_enable
    from imcsdk.apis.admin.snmp import snmp_disable
    from imcsdk.apis.admin.snmp import is_snmp_enabled

    ansible = module.params
    args_mo  =  _get_mo_params(ansible)
    exists, mo = is_snmp_enabled(handle=server, **args_mo)

    if ansible["state"] == "present":
        if module.check_mode or exists:
            return not exists, False
        snmp_enable(handle=server, **args_mo)
    else:
        if module.check_mode or not exists:
            return exists, False
        snmp_disable(server)

    return True, False


def setup(server, module):
    results = {}
    err = False

    try:
        results["changed"], err = setup_snmp(server, module)

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

