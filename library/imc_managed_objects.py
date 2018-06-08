#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metatdata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: imc_managed_objects
short_description: Configures Managed Objects on Cisco Integrated Management Controller (IMC)
description:
- Configures Managed Objects on Cisco Integrated Management Controller (IMC).
- The Python SDK module, Python class within the module (UCSM Class), and all properties must be directly specified.
- More information on the UCSM Python SDK and how to directly configure Managed Objects is available at
  U(http://imcsdk.readthedocs.io/).
options:
  objects:
    description:
    - 'List of managed objects to configure.  Each managed object must have the following:'
    - '- module: Name of the Python SDK module implementing the required class.'
    - '- class: Name of the Python class that will be used to configure the Managed Object.'
    - '- properties: Properties to configure on the Managed Object.  See the UCSM Python SDK for information on properties for each class.'
    - 'Objects can optionally contain a list of "children", and each child object is required to have the above options.'
    - Note that the parent_mo_or_dn property for child objects is automatically set as the list of children is configured.
    - Either objects or json_config_file must be specified.
  json_config_file:
    description:
    - 'Filename (absolute path) of a JSON configuration file.  The JSON file should have the same fields described in the objects option.'
    - Either objects or json_config_file must be specified.
requirements:
- imcsdk
author:
- David Soper (@dsoper2)
- CiscoUcs (@CiscoUcs)
version_added: '2.6'
'''

EXAMPLES = r'''
- name: NTP config
  imc_managed_objects:
    <<: *login_info
    objects:
    - {
      "module": "imcsdk.mometa.comm.CommNtpProvider",
      "class": "CommNtpProvider",
      "properties": {
          "parent_mo_or_dn": "sys/svc-ext",
          "ntp_enable": "yes",
          "ntp_server1": "ntp.esl.cisco.com"
      }
    }

- name: Remove NTP config
  imc_managed_objects:
    <<: *login_info
    objects:
    - {
      "module": "imcsdk.mometa.comm.CommNtpProvider",
      "class": "CommNtpProvider",
      "properties": {
          "parent_mo_or_dn": "sys/svc-ext",
          "ntp_enable": "yes",
          "ntp_server1": "ntp.esl.cisco.com"
      }
    }
    state: absent
'''

RETURN = r'''
#
'''

from importlib import import_module
from copy import deepcopy
import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.cisco_imc import ImcConnection


def traverse_objects(module, imc, managed_object, mo=''):
    props_match = False

    mo_module = import_module(managed_object['module'])
    mo_class = getattr(mo_module, managed_object['class'])

    if not managed_object['properties'].get('parent_mo_or_dn'):
        managed_object['properties']['parent_mo_or_dn'] = mo

    mo = mo_class(**managed_object['properties'])

    existing_mo = imc.handle.query_dn(mo.dn)

    if module.params['state'] == 'absent':
        # mo must exist, but all properties do not have to match
        if existing_mo:
            if not module.check_mode:
                imc.handle.remove_mo(existing_mo)
            imc.result['changed'] = True
    else:
        if existing_mo:
            # check mo props
            kwargs = dict(managed_object['properties'])
            kwargs.pop('parent_mo_or_dn', None)
            if existing_mo.check_prop_match(**kwargs):
                props_match = True

        if not props_match:
            if not module.check_mode:
                imc.handle.add_mo(mo)
            imc.result['changed'] = True

    if managed_object.get('children'):
        for child in managed_object['children']:
            # explicit deep copy of child object since traverse_objects may modify parent mo information
            copy_of_child = deepcopy(child)
            traverse_objects(module, imc, copy_of_child, mo)


def main():
    argument_spec = dict(
        ip=dict(type='str', required=True, aliases=['hostname']),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        port=dict(type='str'),
        secure=dict(type='str'),
        proxy=dict(type='str'),
        objects=dict(type='list'),
        json_config_file=dict(type='str'),
        state=dict(type='str', choices=['present', 'absent'], default='present'),
    )

    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
        required_one_of=[
            ['objects', 'json_config_file'],
        ],
        mutually_exclusive=[
            ['objects', 'json_config_file'],
        ],
    )
    imc = ImcConnection(module)
    imc.result = {}
    imc.login()

    err = False
    # note that all objects specified in the object list report a single result (including a single changed).
    imc.result['changed'] = False
    try:
        if module.params.get('objects'):
            objects = module.params['objects']
        else:
            # either objects or json_config_file will be specified, so if there is no objects option use a config file
            with open(module.params['json_config_file']) as f:
                objects = json.load(f)['objects']

        for managed_object in objects:
            traverse_objects(module, imc, managed_object)

    except Exception as e:
        err = True
        imc.result['msg'] = "setup error: %s " % str(e)

    finally:
        imc.logout()

    if err:
        module.fail_json(**imc.result)
    module.exit_json(**imc.result)


if __name__ == '__main__':
    main()
