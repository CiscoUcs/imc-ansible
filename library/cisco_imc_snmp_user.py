#!/usr/bin/env python

from ansible.module_utils.basic import *


DOCUMENTATION = '''
---
module: cisco_imc_snmp_user
short_description: Configures SNMP user on a Cisco IMC Server
version_added: 0.9.0.0
description:
   -  Configures the SNMP user on a Cisco IMC Server
Input Params:
    name:
        description: snmp username
        required: True
    security_level:
        description: security level
        required: False
        choices: ['authpriv', 'authnopriv', 'noauthnopriv']
        default: "authpriv"
    auth_pwd:
        description: password
        required: False
    auth:
        description: auth type
        required: False
        choices: ['MD5', 'SHA']
        default: "MD5"
    privacy_pwd:
        description: privacy password
        required: False
    privacy:
        description: privacy type
        required: False
        choices: ['AES', 'DES']
        default: "AES"

requirements: ['imcsdk']
author: "Rahul Gupta(ragupta4@cisco.com)"
'''


EXAMPLES = '''
- name:
  cisco_imc_snmp_user:
    name:
    security_level:
    auth_pwd:
    auth:
    privacy_pwd:
    privacy:
    state: "present"
    ip: "192.168.1.1"
    username: "admin"
    password: "password"
'''


def _argument_mo():
    return dict(
                name=dict(required=True, type='str'),
                security_level=dict(required=False, type='str', choices=['authpriv', 'authnopriv', 'noauthnopriv'], default="authpriv"),
                auth_pwd=dict(required=False, type='str'),
                auth=dict(required=False, type='str', choices=['MD5', 'SHA'], default="MD5"),
                privacy_pwd=dict(required=False, type='str'),
                privacy=dict(required=False, type='str', choices=['AES', 'DES'], default="AES"),
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


def setup_snmp_user(server, module):
    from imcsdk.apis.admin.snmp import snmp_user_add
    from imcsdk.apis.admin.snmp import snmp_user_remove
    from imcsdk.apis.admin.snmp import snmp_user_exists

    ansible = module.params
    args_mo  =  _get_mo_params(ansible)
    exists, mo = snmp_user_exists(handle=server, **args_mo)

    if ansible["state"] == "present":
        if module.check_mode or exists:
            return not exists, False
        snmp_user_add(handle=server, **args_mo)
    else:
        if module.check_mode or not exists:
            return exists, False
        snmp_user_remove(server, mo.name)

    return True, False


def setup(server, module):
    results = {}
    err = False

    try:
        results["changed"], err = setup_snmp_user(server, module)

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

