#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: imc_query

short_description: Queries Cisco IMC (Integrated Management Controller) objects by class or distinguished name

description:
  - Queries IMC objects by class or distinguished name.

options:
    class_ids:
        description:
        - One or more IMC Class IDs to query.
        - As a comma separtated list
        type: str

    distinguished_names:
        description:
        - One or more IMC Distinguished Names to query.
        - As a comma separtated list
        type: str

requirements:
    - imcsdk

author:
    - David Soper (@dsoper2)
    - John McDonough (@movinalot)
    - Ciscoimc (@Ciscoimc)
version_added: "2.10"
'''

EXAMPLES = r'''
- name: Query IMC Class ID
  imc_query:
    hostname: "{{ inventory_hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    class_ids: adaptorUnit
  delegate_to: localhost

- name: Query IMC Class IDs
  imc_query:
    hostname: "{{ inventory_hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    class_ids: computeRackUnit, adaptorUnit
  delegate_to: localhost

- name: Query IMC Distinguished Name
  imc_query:
    hostname: "{{ inventory_hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    distinguished_names: sys/rack-unit-1/adaptor-MLOM
  delegate_to: localhost

- name: Query IMC Distinguished Names
  imc_query:
    hostname: "{{ inventory_hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    distinguished_names: sys/rack-unit-1, sys/rack-unit-1/adapter-MLOM
  delegate_to: localhost
'''

RETURN = '''
objects:
    description: results JSON encodded
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.cisco_imc import ImcConnection


def retrieve_class_id(class_id, imc):
    return imc.handle.query_classid(class_id)


def retrieve_distinguished_name(distinguished_name, imc):
    return imc.handle.query_dn(distinguished_name)


def make_mo_dict(imc_mo):
    obj_dict = {}
    for mo_property in imc_mo.prop_map['classic'].values():
        obj_dict[mo_property] = getattr(imc_mo, mo_property)
    return obj_dict


def main():
    argument_spec = dict(
        ip=dict(type='str', required=True, aliases=['hostname']),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        port=dict(type='str'),
        secure=dict(type='str'),
        proxy=dict(type='str'),
        class_ids=dict(type='str'),
        distinguished_names=dict(type='str'),
    )

    module = AnsibleModule(
        argument_spec,
        supports_check_mode=True,
        mutually_exclusive=[
            ['class_ids', 'distinguished_names'],
        ],
    )

    # imcModule verifies imcmsdk is present and exits on failure.
    # Imports are below for imc object creation.
    imc = ImcConnection(module)
    imc.result = {}
    imc.login()

    query_result = {}

    try:
        if module.params['class_ids']:
            class_ids = [
                x.strip() for x in module.params['class_ids'].split(',')
            ]
            for class_id in class_ids:
                query_result[class_id] = []
                imc_mos = retrieve_class_id(class_id, imc)
                if imc_mos:
                    for imc_mo in imc_mos:
                        query_result[class_id].append(make_mo_dict(imc_mo))

            imc.result['objects'] = query_result

        elif module.params['distinguished_names']:
            distinguished_names = [
                x.strip()
                for x in module.params['distinguished_names'].split(',')
            ]
            for distinguished_name in distinguished_names:
                query_result[distinguished_name] = {}
                imc_mo = retrieve_distinguished_name(distinguished_name, imc)

                if imc_mo:
                    query_result[distinguished_name] = make_mo_dict(imc_mo)

            imc.result['objects'] = query_result

    except Exception as e:
        imc.result['msg'] = "setup error: %s " % str(e)
        module.fail_json(**imc.result)

    finally:
        imc.logout()

    module.exit_json(**imc.result)


if __name__ == '__main__':
    main()
