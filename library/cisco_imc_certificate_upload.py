#!/usr/bin/env python

from ansible.module_utils.basic import *


DOCUMENTATION = '''
---
module: cisco_imc_certificate_upload
short_description: Uploads certificate on a Cisco IMC Server
version_added: 0.9.0.0
description:
   -  Uploads certificate on a Cisco IMC Server
Input Params:
    server:
        description: ip address of the remote server
        required: True
    username:
        description: remote server login user
        required: True
    password:
        description: remote server login password
        required: True
    file_name:
        description: file_name with full path for the certificate file
        required: True
    protocol:
        description: protocol to transfer file to remote server
        required: True
        choices: ['ftp', 'http', 'none', 'scp', 'sftp', 'tftp']

requirements: ['imcsdk']
author: "Rahul Gupta(ragupta4@cisco.com)"
'''


EXAMPLES = '''
- name:
  cisco_imc_certificate_upload:
    server:
    username:
    password:
    file_name:
    protocol:
    state: "present"
    ip: "192.168.1.1"
    username: "admin"
    password: "password"
'''


def _argument_mo():
    return dict(
                server=dict(required=True, type='str'),
                username=dict(required=True, type='str'),
                password=dict(required=True, type='str'),
                file_name=dict(required=True, type='str'),
                protocol=dict(required=True, type='str',
                    choices=['ftp', 'http', 'none', 'scp', 'sftp', 'tftp'])
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


def setup_certificate_upload(server, module):
    from imcsdk.apis.admin.certificate import certificate_upload

    ansible = module.params
    exists = False
    args_mo  =  _get_mo_params(ansible)
    if module.check_mode or exists:
        return not exists, False
    certificate_upload(handle=server, **args_mo)

    return True, False


def setup(server, module):
    results = {}
    err = False

    try:
        results["changed"], err = setup_certificate_upload(server, module)

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

