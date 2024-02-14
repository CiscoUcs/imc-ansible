#!/usr/bin/env python

from ansible.module_utils.basic import *


DOCUMENTATION = '''
---
module: cisco_imc_bios_profile_upload
short_description: Uploads a user configured bios profile in json format.
version_added: 0.9.0.0
description:
   -  Uploads a user configured bios profile in json format.
      Cisco IMC supports uploading a maximum of 3 profiles
Input Params:
    remote_server:
        description: ip address of the remote server
        required: True
    user:
        description: remote server login user
        required: True
    pwd:
        description: remote server login password
        required: True
    remote_file:
        description: file_name with full path for the bios profile file
        required: True
    protocol:
        description: protocol to transfer file to remote server
        required: True
        choices: ['ftp', 'http', 'none', 'scp', 'sftp', 'tftp']
    server_id:
        description: d of the server to perform this operation on C3260
        platforms
        required: False
        choices:
        default: 1

requirements: ['imcsdk']
author: "Rahul Gupta(ragupta4@cisco.com)"
'''


EXAMPLES = '''
- name:
  cisco_imc_bios_profile_upload:
    remote_server:
    user:
    pwd:
    remote_file:
    protocol:
    state: "present"
    ip: "192.168.1.1"
    username: "admin"
    password: "password"
'''


def _argument_mo():
    return dict(
                remote_server=dict(required=True, type='str'),
                user=dict(required=True, type='str'),
                pwd=dict(required=True, type='str'),
                remote_file=dict(required=True, type='str'),
                protocol=dict(required=True, type='str',
                    choices=['ftp', 'http', 'none', 'scp', 'sftp', 'tftp']),
                server_id=dict(required=False, type='str', default='1')
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


def setup_bios_profile_upload(server, module):
    from imcsdk.apis.server.bios import bios_profile_upload

    ansible = module.params
    exists = False
    args_mo  =  _get_mo_params(ansible)
    if module.check_mode or exists:
        return not exists, False
    mo = bios_profile_upload(handle=server, **args_mo)
    if "failed" in mo.bios_profile_upload_status:
        return False, True

    return True, False


def setup(server, module):
    results = {}
    err = False

    try:
        results["changed"], err = setup_bios_profile_upload(server, module)
        if err:
            results["msg"] = "Bios Profile already exist. If there is any "\
            "configuration change. Please remove the bios profile and "\
            "re-upload."
            err = False

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

