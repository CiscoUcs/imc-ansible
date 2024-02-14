#!/usr/bin/env python

from ansible.module_utils.basic import *


DOCUMENTATION = '''
---
module: cisco_imc_boot_order_legacy
short_description: Set boot order precision for a Cisco IMC server.
version_added: 0.9.0.0
description:
   -  Set boot order precision for a Cisco IMC server.
Input Params:
    reboot_on_update:
        description: reboots cimc if true and boot order changes
        required: False
    secure_boot:
        description: secure_boot
        required: False
    boot_devices:
        description: dictionary {"order":"", "device-type": ""}
        required: True
    server_id:
        description: Server Id to be specified for C3260 platforms
        required: False
        default: "1"

requirements: ['imcsdk']
author: "Rahul Gupta(ragupta4@cisco.com)"
'''


EXAMPLES = '''
- name:
  cisco_imc_boot_order_legacy:
    reboot_on_update:
    secure_boot:
    boot_devices:
    server_id:
    ip: "192.168.1.1"
    username: "admin"
    password: "password"
'''


def _argument_mo():
    return dict(
                reboot_on_update=dict(required=False, type='bool', default=False),
                secure_boot=dict(required=False, type='bool', default=False),
                boot_devices=dict(required=True, type='list'),
                server_id=dict(required=False, type='str', default="1"),
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
    argument_spec.update(_argument_imc_connection())

    return AnsibleModule(argument_spec,
                         supports_check_mode=True)


def _get_mo_params(params):
    from ansible.module_utils.cisco_imc import ImcConnection
    args = {}
    for key in params:
        if ( ImcConnection.is_login_param(key) or
            params.get(key) is None):
            continue
        args[key] = params.get(key)
    return args


def setup_boot_order_legacy(server, module):
    from imcsdk.apis.server.bios import boot_order_policy_set
    from imcsdk.apis.server.bios import boot_order_policy_exists

    ansible = module.params
    args_mo  =  _get_mo_params(ansible)
    exists, mo = boot_order_policy_exists(handle=server, **args_mo)

    if module.check_mode or exists:
        return not exists, False

    boot_order_policy_set(handle=server, **args_mo)
    return True, False


def setup(server, module):
    results = {}
    err = False

    try:
        results["changed"], err = setup_boot_order_legacy(server, module)

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

