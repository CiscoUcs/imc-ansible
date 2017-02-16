#!/usr/bin/env python

from ansible.module_utils.basic import *


DOCUMENTATION = '''
---
module: cisco_imc_user_password_policy
short_description:
Configures the password policy and password expiration policy for local users on a Cisco IMC server.
version_added: "0.9.0.0"
description:
    - Configures the password policy and password expiration policy for local users on a Cisco IMC server.
options:
    strong_password:
        description: This enables the strong password policy.
        choices: ["enabled", "disabled"]
        default: "disabled"
        required: False

    password_expiry_duration:
        description: Specifies in days when the password will expire when password expiry is enabled.
        choices: [0-3650]
        default: 0
        required: False

    password_history:
        description: Tracks password change history. Specifies in number of instances, the new password entered should not have been used in the past.
        choices: [0-5]
        default: 0
        required: False

    password_notification_period:
        description: Specifies the number of days the user will be notified before password expiry.
        choices: [0-15]
        default: 0
        required: False

    password_grace_period:
        description: Specifies the number of days the old password will still be valid after the password expiry.
        choices: [0-5]
        default: 0
        required: False

requirements: ['imcsdk']
author: "Swapnil Wagh(swwagh@cisco.com)"
'''

EXAMPLES = '''
- name: set password policy
  cisco_imc_user_password_policy:
    strong_password: "enabled"
    password_expiry_duration: 365
    password_history: 1
    password_notification_period: 15
    password_grace_period: 15
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


def password_policy_setup(server, module):
    from imcsdk.apis.admin.user import strong_password_set
    from imcsdk.apis.admin.user import is_strong_password_set

    ansible = module.params
    strong_password = ansible["strong_password"]
    to_enable = (False, True)[strong_password == "enabled"]
    is_enabled = is_strong_password_set(server)
    if to_enable == is_enabled:
        return False

    if not module.check_mode:
        strong_password_set(server, enable=to_enable)
    return True


def password_expiry_setup(server, module):
    from imcsdk.apis.admin.user import password_expiration_set
    from imcsdk.apis.admin.user import password_expiration_exists

    return False

    ansible = module.params

    password_expiry_duration = ansible["password_expiry_duration"]
    password_history = ansible["password_history"]
    password_notification_period = ansible["password_notification_period"]
    password_grace_period = ansible["password_grace_period"]

    exists, mo = password_expiration_exists(
        server,
        password_expiry_duration=password_expiry_duration,
        password_history=password_history,
        password_notification_period=password_notification_period,
        password_grace_period=password_grace_period)

    if exists:
        return False

    if module.check_mode:
        return True

    password_expiration_set(
        server,
        password_expiry_duration=password_expiry_duration,
        password_history=password_history,
        password_notification_period=password_notification_period,
        password_grace_period=password_grace_period)
    return True


def setup(server, module):
    results = {}
    err = False

    try:
        pp_changed = password_policy_setup(server, module)
        pe_changed = password_expiry_setup(server, module)
        results["changed"] = pp_changed or pe_changed

    except Exception as e:
        err = True
        results["msg"] = str(e)
        results["changed"] = False

    return results, err


def main():
    from ansible.module_utils.cisco_imc import ImcConnection
    module = AnsibleModule(
        argument_spec=dict(
            strong_password=dict(required=False, default="disabled",
                                 choices=["enabled", "disabled"], type='str'),
            password_expiry_duration=dict(required=False, default=0,
                                          type='int'),
            password_history=dict(required=False, default=0,
                                  choices=[0, 1, 2, 3, 4, 5], type='int'),
            password_notification_period=dict(required=False, default=0,
                                              type='int'),
            password_grace_period=dict(required=False, default=0,
                                       type='int'),

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

    conn = ImcConnection(module)
    server = conn.login()
    results, err = setup(server, module)
    conn.logout()
    if err:
        module.fail_json(**results)
    module.exit_json(**results)


if __name__ == '__main__':
    main()
