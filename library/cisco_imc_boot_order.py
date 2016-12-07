#!/usr/bin/python

DOCUMENTATION = '''
---
module: cisco_imc_boot_order
short_description: Set boot order for a Cisco IMC server.
version_added: "0.9.0.0"
description:
  - Set boot order for a Cisco IMC server
options:
  boot_devices:
    description: a list of tuples, [(<order>, <device-type>, <device-name>)]
        boot-order(string): Order
        boot-device-type(string): "efi", "lan", "storage", "vmedia"
        boot-device-name(string): Unique label for the boot device
    required: true
  secure_boot:
    description: Enable secure-boot
    required: false
    default: False
    choices: [True, False]
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
- name: Create a boot order policy for Cisco IMC
  hosts: 127.0.0.1
  connection: local
  tasks:
  - name: Set the boot order
    cisco_imc_boot_order:
      boot_devices= [("1", "storage", "ext-hdd1"), ("2", "lan", "office-lan")]

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


def policy_exists(server, module):
    from imcsdk.apis.server.bios import boot_order_precision_exists

    ansible = module.params
    match, msg = boot_order_precision_exists(handle=server,
                                          reboot_on_update=ansible["reboot_on_update"],
                                          configured_boot_mode=ansible["configured_boot_mode"],
                                          boot_devices=ansible["boot_devices"],
                                          server_id=ansible["server_id"])
    #print(msg)
    return match


def boot_order_policy(module):
    from imcsdk.apis.server.bios import set_boot_order_precision

    results = {}
    err = False

    try:
        server = login(module)

        ansible = module.params
        _exists = policy_exists(server, module)
        if module.check_mode or _exists:
            module.exit_json(changed=not _exists)

        set_boot_order_precision(handle=server,
                                    boot_devices=ansible['boot_devices'],
                                    reboot_on_update=ansible['reboot_on_update'],
                                    configured_boot_mode=ansible['configured_boot_mode'],
                                    server_id=ansible['server_id'])

        results["changed"] = True
        logout(module, server)
    except Exception as e:
        err = True
        results["exception"] = str(e)
        results["msg"] = str(e)
        results["changed"] = False
        logout(module, server)

    return results, err


def main():
    from ansible.module_utils.basic import AnsibleModule
    module = AnsibleModule(
        argument_spec=dict(
            boot_devices=dict(required=True, type='list'),
            configured_boot_mode=dict(required=False, default="Legacy", type='str'),
            reboot_on_update=dict(required=False, default="no", choices=["yes", "no"]),
            server_id=dict(required=False, default=1, type='int'),

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

    results, err = boot_order_policy(module)
    if err:
        module.fail_json(**results)
    module.exit_json(**results)


if __name__ == '__main__':
    main()
