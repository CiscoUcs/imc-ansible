#!/usr/bin/env python

DOCUMENTATION = '''
---
module: cisco_imc_boot_order_precision
short_description: Set boot order precision for a Cisco IMC server.
version_added: "0.9.0.0"
description:
  - Set boot order precision for a Cisco IMC server
options:
  boot_devices:
    description: dictionary {"order":"", "device-type": "", "name":""}
    required: true
  configured_boot_mode:
    description: Configure boot mode
    required: false
    default: False
    choices: ["Legacy", "None", "Uefi"]
  reapply:
    description: Configure reapply
    required: false
    default: "no"
    choices: ["yes", "no"]
  reboot_on_update:
    description: Enable reboot on update
    required: false
    default: "no"
    choices: ["yes", "no"]
  server_id:
    description: Specify server id for UCS C3260 modular servers
    default: 1
    required: false

requirements: ['imcsdk']
author: "Vikrant Balyan(vvb@cisco.com)"
'''

EXAMPLES = '''
- name: Set the boot order precision
  cisco_imc_boot_order_precision:
    boot_devices:
      - {"order":"1", "device-type":"hdd", "name":"hdd"}
      - {"order":"2", "device-type":"pxe", "name":"pxe"}
      - {"order":"3", "device-type":"pxe", "name":"pxe2"}
    ip: "192.168.1.1"
    username: "admin"
    password: "password"
'''


def policy_exists(server, module):
    from imcsdk.apis.server.bios import boot_order_precision_exists as exists

    ansible = module.params
    match, err = exists(handle=server,
                        reboot_on_update=ansible["reboot_on_update"],
                        reapply=ansible["reapply"],
                        configured_boot_mode=ansible["configured_boot_mode"],
                        boot_devices=ansible["boot_devices"],
                        server_id=ansible["server_id"])

    if err:
        print(err)
    return match


def boot_order_precision(server, module):
    from imcsdk.apis.server.bios import boot_order_precision_set as \
                                        set_boot_order

    results = {}
    err = False

    try:
        ansible = module.params
        _exists = policy_exists(server, module)
        if module.check_mode or _exists:
            results["changed"] = not _exists
            return results, False

        set_boot_order(handle=server,
                       boot_devices=ansible['boot_devices'],
                       reboot_on_update=(False, True)[ansible['reboot_on_update'] == "yes"],
                       reapply=(False, True)[ansible['reapply'] == "yes"],
                       configured_boot_mode=ansible['configured_boot_mode'],
                       server_id=ansible['server_id'])

        results["changed"] = True
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
            boot_devices=dict(required=True, type='list'),
            configured_boot_mode=dict(required=False, default="Legacy",
                                      choices=["Legacy", "None", "Uefi"],
                                      type='str'),
            reapply=dict(required=False, default="no", choices=["yes", "no"],
                         type="str"),
            reboot_on_update=dict(required=False, default="no",
                                  choices=["yes", "no"], type="str"),
            server_id=dict(required=False, default=1, type='int'),

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
    results, err = boot_order_precision(server, module)
    conn.logout()
    if err:
        module.fail_json(**results)
    module.exit_json(**results)


if __name__ == '__main__':
    main()
