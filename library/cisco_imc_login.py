#!/usr/bin/env python

from ansible.module_utils.basic import *

DOCUMENTATION = '''
---
module: cisco_imc_login
short_description: Login to a IMC server
version_added: "0.9.0.0"
description:
  - Logs in to a cisco IMC server
  - Executes the aaaLogin method provided by the IMC Server

requirements: ['imcsdk']
author: "Vikrant Balyan(vvb@cisco.com)"
'''

EXAMPLES = '''
- name: login to a IMC server
  hosts: 127.0.0.1
  connection: local
  tasks:
  - name: login to the server
    cisco_imc_login:
      ip=192.168.1.1
      username=admin
      password=password
'''


def imc_login(module):
    '''
    Fetches/Creates a server handle.

    Arguments:
        module: AnsibleModule

    Returns:
        (server(ImcHandle), results(dict), error(bool))

    '''
    ansible = module.params
    results = {}

    server, results, err = _login(ip=ansible["ip"],
                                  username=ansible["username"],
                                  password=ansible["password"],
                                  port=ansible["port"],
                                  secure=ansible["secure"],
                                  proxy=ansible["proxy"])
    return server, results, err


def _login(ip, username, password, port=None, secure=None, proxy=None):
    from imcsdk.imchandle import ImcHandle
    results = {}
    try:
        server = ImcHandle(ip, username, password, port, secure, proxy)
        server.login()
    except Exception as e:
        results["msg"] = str(e)
        return server, results, True

    results["msg"] = "login succeded"
    results["changed"] = False
    results["server"] = server
    return server, results, False


def main():
    module = AnsibleModule(
        argument_spec=dict(
            ip=dict(required=True, type='str'),
            username=dict(required=False, default="admin", type='str'),
            password=dict(required=True, type='str'),
            port=dict(required=False, default=None),
            secure=dict(required=False, default=None),
            proxy=dict(required=False, default=None)
        ),
        supports_check_mode=True
    )

    server, results, err = imc_login(module)
    if err:
        module.fail_json(**results)
    module.exit_json(**results)


if __name__ == '__main__':
    main()
