#!/usr/bin/env python

from ansible.module_utils.basic import *

DOCUMENTATION = '''
---
module: cisco_imc_sol
short_description: Configures sol on a Cisco IMC Server
version_added: "0.9.0.0"
description:
    - Configures the Serial Over Lan(SOL) service on a Cisco IMC Server
Input Params:
    speed:
        description: speed of the connection
        required: False
        choices: ["9600", "19200", "38400", "57600", "115200"]
        default: '19200'

    comport:
        description: Comport on the server side
        required: False
        choices: ["com0", "com1"]

    server_id:
        description: Server Id to be specified for C3260 platforms
        choices: ["admin", "read-only", "user"]
        default: "read-only"
        required: False

    ssh_port: 
        description: the SSH port for access to the console
        default: 22

    state:
        description: Used to create or delete the SOL console
        choices: ["present", "absent"]
        default: "present"
        required: False

requirements: ['imcsdk']
author: "Branson Matheson (brmathes@cisco.com)"
'''

EXAMPLES = '''
- name: enable SOL over ssh
  cisco_imc_sol:
    comport: "com0"
    speed: "9600"
    ssh_port: 22
    state: "present"
    ip: "192.168.1.1"
    username: "admin"
    password: "password"
'''


def login(module):
    ansible = module.params
    server = ansible.get('server')
    if server:
        return server

    from imcsdk.imchandle import ImcHandle
    results = {}
    try:
        server = ImcHandle(ip=ansible["ip"],
                           username=ansible["username"],
                           password=ansible["password"],
                           port=ansible["port"],
                           secure=ansible["secure"],
                           proxy=ansible["proxy"])
        server.login()
    except Exception as e:
        results["msg"] = str(e)
        module.fail_json(**results)
    return server


def logout(module, imc_server):
    ansible = module.params
    server = ansible.get('server')
    if server:
        # we used a pre-existing handle from another task.
        # do not logout
        return False

    if imc_server:
        imc_server.logout()
        return True
    return False


def setup_sol(server, module):
    from imcsdk.apis.server.remotepresence import sol_setup
    from imcsdk.apis.server.remotepresence import sol_disable
    from imcsdk.apis.server.remotepresence import is_sol_enabled

    ansible = module.params
    speed, comport = ansible["speed"], ansible["com_port"]
    ssh_port, server_id = ansible['ssh_port'], ansible["server_id"]

    exists = is_sol_enabled(server, server_id=server_id)
    if ansible["state"] == "present":
        if exists:
            return False
        if not module.check_mode:
            sol_setup(server, speed, comport, ssh_port, server_id=server_id)
    else:
        if not exists:
            return False
        if not module.check_mode:
            sol_disable(server, server_id=server_id)
    return True


def setup(server, module):
    results = {}
    err = False

    try:
        results["changed"] = setup_sol(server, module)

    except Exception as e:
        err = True
        results["msg"] = "setup error: %s " % str(e)
        results["changed"] = False

    return results, err


def main():
    from ansible.module_utils.cisco_imc import ImcConnection
    module = AnsibleModule(
        argument_spec=dict(
            speed=dict(type='str', default='115200',
                       choices=["9600", "19200", "38400", "57600", "115200"]),
            server_id=dict(required=False, type='int', default=1),
            com_port=dict(type='str', default="com0",
                      choices=["com0", "com1"]),
            ssh_port=dict(type='int', default=22),
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
