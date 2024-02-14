#!/usr/bin/env python

from ansible.module_utils.basic import *


DOCUMENTATION = '''
---
module: cisco_imc_syslog_remote
short_description: Enables remote system logs on a Cisco IMC Server
version_added: 0.9.0.0
description:
   -  Enables system log for remote client on a Cisco IMC Server
Input Params:
    hostname:
        description: ip address of the remote host
        required: True
    name:
        description: remote host type
        required: False
        choices: ['primary', 'secondary', 'tertiary']
        default: "primary"
    port:
        description: remote host port
        required: False
        default: "514"

requirements: ['imcsdk']
author: "Rahul Gupta(ragupta4@cisco.com)"
'''


EXAMPLES = '''
- name:
  cisco_imc_syslog_remote:
    hostname:
    name:
    port:
    state: "present"
    ip: "192.168.1.1"
    username: "admin"
    password: "password"
'''


def _argument_mo():
    return dict(
                hostname=dict(required=True, type='str'),
                name=dict(required=False, type='str', choices=['primary', 'secondary', 'tertiary'], default="primary"),
                port=dict(required=False, type='str', default="514"),
    )


def _argument_state():
    return dict(
        state=dict(required=False,
                   default="present",
                   choices=['present', 'absent', 'clear'],
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


def setup_syslog_remote(server, module):
    from imcsdk.apis.admin.syslog import syslog_remote_enable
    from imcsdk.apis.admin.syslog import syslog_remote_disable
    from imcsdk.apis.admin.syslog import is_syslog_remote_enabled
    from imcsdk.apis.admin.syslog import syslog_remote_clear
    from imcsdk.apis.admin.syslog import is_syslog_remote_clear

    ansible = module.params
    args_mo  =  _get_mo_params(ansible)

    if ansible["state"] == "clear":
        exists, mo = is_syslog_remote_clear(handle=server,
                                            name=args_mo['name'])
        if module.check_mode or exists:
            return not exists, False
        syslog_remote_clear(handle=server, name=args_mo['name'])
        return True, False

    exists, mo = is_syslog_remote_enabled(handle=server, **args_mo)

    if ansible["state"] == "present":
        if module.check_mode or exists:
            return not exists, False
        syslog_remote_enable(handle=server, **args_mo)
    else:
        if module.check_mode or not exists:
            return exists, False
        if ansible["state"] == "absent":
            syslog_remote_disable(server, mo.name)
        elif ansible["state"] == "clear":
            syslog_remote_clear(server, mo.name)
    return True, False


def setup(server, module):
    results = {}
    err = False

    try:
        results["changed"], err = setup_syslog_remote(server, module)

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

