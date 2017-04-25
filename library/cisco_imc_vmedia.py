#!/usr/bin/env python

from ansible.module_utils.basic import *


DOCUMENTATION = '''
---
module: cisco_imc_vmedia
short_description: Configures vmedia on a Cisco IMC Server
version_added: 0.9.0.0
description:
   -  Configures the vmedia on a Cisco IMC Server
Input Params:
    encryption_state:
        description: Encrypt virtual media communications
        required: False
        choices: ['disabled', 'enabled']
        default: "disabled"
    low_power_usb:
        description: Enable low power usb
        required: False
        choices: ['disabled', 'enabled']
        default: "disabled"
    server_id:
        description: Server Id to be specified for C3260 platforms
        required: False
        default: "1"

requirements: ['imcsdk']
author: "Rahul Gupta(ragupta4@cisco.com)"
'''


EXAMPLES = '''
- name:
  cisco_imc_vmedia:
    encryption_state:
    low_power_usb:
    server_id:
    state: "present"
    ip: "192.168.1.1"
    username: "admin"
    password: "password"
'''


def _argument_mo():
    return dict(
                encryption_state=dict(required=False, type='str', choices=['disabled', 'enabled'], default="disabled"),
                low_power_usb=dict(required=False, type='str', choices=['disabled', 'enabled'], default="disabled"),
                server_id=dict(required=False, type='str', default="1"),
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


def setup_vmedia(server, module):
    from imcsdk.apis.server.remotepresence import vmedia_setup
    from imcsdk.apis.server.remotepresence import vmedia_disable
    from imcsdk.apis.server.remotepresence import is_vmedia_enabled

    ansible = module.params
    args_mo  =  _get_mo_params(ansible)
    exists, mo = is_vmedia_enabled(handle=server, **args_mo)

    if ansible["state"] == "present":
        if module.check_mode or exists:
            return not exists, False
        vmedia_setup(handle=server, **args_mo)
    else:
        if module.check_mode or not exists:
            return exists, False
        vmedia_disable(server)

    return True, False


def setup(server, module):
    results = {}
    err = False

    try:
        results["changed"], err = setup_vmedia(server, module)

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

