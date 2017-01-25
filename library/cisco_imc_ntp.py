#!/usr/bin/python

DOCUMENTATION = '''
---
module: cisco_imc_ntp
short_description: Setup NTP on a Cisco IMC server.
version_added: "0.9.0.0"
description:
  - Setup NTP on a Cisco IMC server.
options:
  state:
    description: Enable/Disable NTP
    default: "present"
    choices: ["present", "absent"]
    required: true
  ntp_servers:
    description: Dictionary of NTP servers to be configured {"id":"", "ip":""}
    required: false

requirements: ['imcsdk']
author: "Swapnil Wagh(swwagh@cisco.com)"
'''

EXAMPLES = '''
- name: enable ntp
  cisco_imc_ntp
    ntp_servers:
      - {"id": "1", "ip": "192.168.1.1"}
      - {"id": "2", "ip": "192.168.1.2"}
    ip: "192.168.1.1"
    username: "admin"
    password: "password"
    state: "present"
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


def setup(server, module):
    from imcsdk.apis.admin.ntp import ntp_enable
    from imcsdk.apis.admin.ntp import ntp_disable
    from imcsdk.apis.admin.ntp import ntp_setting_exists

    results = {}
    err = False

    try:
        ansible = module.params
        if ansible['state'] == 'present':
            ntp_servers = ansible['ntp_servers']
            exists, mo = ntp_setting_exists(
                                    server,
                                    ntp_enable='yes',
                                    ntp_servers=ansible['ntp_servers'])
            if module.check_mode or exists:
                results["changed"] = not exists
                return results, False

            ntp_enable(server, ntp_servers=ntp_servers)
        elif ansible['state'] == 'absent':
            exists, mo = ntp_setting_exists(server, ntp_enable='no')
            if module.check_mode or exists:
                results["changed"] = not exists
                return results, False

            ntp_disable(server)

        results['changed'] = True

    except Exception as e:
        err = True
        results["msg"] = str(e)
        results["changed"] = False

    return results, err


def main():
    from ansible.module_utils.basic import AnsibleModule
    from ansible.module_utils.cisco_imc import ImcConnection
    module = AnsibleModule(
        argument_spec=dict(
            ntp_servers=dict(required=False, default=[], type='list'),
            state=dict(required=True,
                       choices=['present', 'absent'], type='str'),

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
