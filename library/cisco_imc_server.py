#!/usr/bin/env python

from ansible.module_utils.basic import *

DOCUMENTATION = '''
---
module: cisco_imc_server
short_description: Configures sol on a Cisco IMC Server
version_added: "0.9.0.0"
description:
    - Configures the Serial Over Lan(SOL) service on a Cisco IMC Server
Input Params:
    state:
        description: speed of the connection
        required: False
        choices: ["on", "shutdown", "off", "reset", "boot"]

    indicator_led:
        description: enable or disable indicator_led
        required: False
        choices: ["on", "off"]

    timeout:
        description: number of seconds to wait for state change
        required: False

    server_id:
        description: Server Id to be specified for C3260 platforms
        required: False

    chassis_id:
        description: chassis Id to be specified for C3260 platforms, 
            if specified on LED it will light the chassis id.
        required: False

requirements: ['imcsdk']
author: "Branson Matheson (brmathes@cisco.com)"
'''

EXAMPLES = '''
- name: boot server
  cisco_imc_server:
    state: "on"
    ip: "192.168.1.1"
    username: "admin"
    password: "password"

- name: shutdown and enable indicator
  cisco_imc_server:
    state: shutdown
    indicator_led: on
    poweroff_seconds: 300
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


def setup_server_power(server, module, status, timeout, interval):
    from imcsdk.apis.server.serveractions import server_power_state_get
    from imcsdk.apis.server.serveractions import server_power_up
    from imcsdk.apis.server.serveractions import server_power_down
    from imcsdk.apis.server.serveractions import server_power_down_gracefully
    from imcsdk.apis.server.serveractions import server_power_cycle

    ansible = module.params
    timeout, interval = ansible["timeout"], ansible["interval"]
    server_id = ansible["server_id"]
    changed = False

    current = server_power_state_get(server, server_id=server_id)

    if current == "off":
        if status == "on" or status == "boot":
            changed = server_power_up(server, timeout=timeout, 
                            interval=interval, serverid_=server_id)
        
    elif current == "on":
        if status == "shutdown":
            changed = server_power_down_gracefully(server, timeout=timeout, 
                            interval=interval, serverid_=server_id)
        elif status == "off":
            changed = server_power_down(server, timeout=timeout, 
                            interval=interval, serverid_=server_id)
        elif status == "boot" or status == "reset":
             changed = server_power_cycle(server, timeout=timeout, 
                            interval=interval, serverid_=server_id)
            
    return change


def setup_server_led(server, module, locator_led):
    from imcsdk.apis.server.serveractions import locator_led_off
    from imcsdk.apis.server.serveractions import locator_led_on

    server_id, chassis_id = ansible["server_id"], ansible["chassis_id"]
    
    if locator_led == "on": 
        locator_led_on(server,
                       server_id=server_id,
                       chassis_id=chassis_id)
    elif locator_led == "off":
        locator_led_off(server, 
                        server_id=server_id, 
                        chassis_id=chassis_id)
    return True

    

def setup_server(server, module):
    ansible = module.params
    status, locator_led = ansible["status"], ansible["locator_led"]
    
    if status is not None:
        power_changed = setup_server_power(server, module, 
                               status, timeout, interval)
        
    if locator_led is not None:
        led_changed = setup_server_led(server, module, locator_led)
            
    return (power_changed or led_changed)


def setup(server, module):
    results = {}
    err = False

    try:
        results["changed"] = setup_server(server, module)

    except Exception as e:
        err = True
        results["msg"] = "setup error: %s " % str(e)
        results["changed"] = False

    return results, err


def main():
    from ansible.module_utils.cisco_imc import ImcConnection
    module = AnsibleModule(
        argument_spec=dict(
            server_id=dict(required=False, type='int', default=1),
            chassis_id=dict(required=False, type='int', default=1),
            state=dict(required=False, type='str',
                       choices=["on", "shutdown", "off", "reset", "boot"]),
            state=dict(required=False, type='str',
                       choices=["on", "off"]),

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
