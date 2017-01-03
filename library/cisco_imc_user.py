#!/usr/bin/python

DOCUMENTATION = '''
---
module: cisco_imc_user
short_description: Configures a local user on a Cisco IMC Server
version_added: "0.9.0.0"
description:
    - Configures a local user on a Cisco IMC Server
Input Params:
    name:
        description: Username for the local user
        required: True

    pwd:
        description: Password for the local user
        required: True

    priv:
        description: Privilege level of the local user
        choices: ["admin", "read-only", "user"]
        default: "read-only"
        required: False

    state:
        description: Used to create or delete the local user
        choices: ["present", "absent"]
        default: "present"
        required: False

requirements: ['imcsdk']
author: "Swapnil Wagh(swwagh@cisco.com)"
'''

EXAMPLES = '''
- name: create local user
  cisco_imc_user:
    name: "jdoe"
    pwd: "password"
    priv: "admin"
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


def local_user_setup(server, module):
    from imcsdk.apis.admin.user import local_user_create
    from imcsdk.apis.admin.user import local_user_delete
    from imcsdk.apis.admin.user import local_user_exists

    ansible = module.params
    name, pwd, priv = ansible["name"], ansible["pwd"], ansible["priv"]

    exists, user = local_user_exists(server, name=name, priv=priv)
    if ansible["state"] == "present":
        if exists:
            return False
        if not module.check_mode:
            local_user_create(server, name=name, pwd=pwd, priv=priv)
    else:
        if not exists:
            return False
        if not module.check_mode:
            local_user_delete(server, name=name)
    return True


def setup(server, module):
    results = {}
    err = False

    try:
        results["changed"] = local_user_setup(server, module)

    except Exception as e:
        err = True
        results["msg"] = str(e)
        results["changed"] = False

    return results, err


def main():
    from ansible.module_utils.basic import AnsibleModule
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(required=True, type='str'),
            pwd=dict(required=False, default=None, type='str'),
            priv=dict(required=False, default="read-only",
                      choices=["admin", "read-only", "user"], type='str'),
            state=dict(required=False, default="present",
                       choices=["present", "absent"], type='str'),

            # ImcHandle
            server=dict(required=False, type='dict'),

            # Imc server credentials
            ip=dict(required=False, type='str'),
            username=dict(required=False, default="admin", type='str'),
            password=dict(required=False, type='str'),
            port=dict(required=False, default=None),
            secure=dict(required=False, default=None),
            proxy=dict(required=False, default=None)
        ),
        supports_check_mode=True
    )

    server = login(module)
    results, err = setup(server, module)
    logout(module, server)
    if err:
        module.fail_json(**results)
    module.exit_json(**results)


if __name__ == '__main__':
    main()
