#!/usr/bin/env python

from ansible.module_utils.basic import *


DOCUMENTATION = '''
---
module: cisco_imc_certificate
short_description: Generates certificate request on a Cisco IMC Server
version_added: 0.9.0.0
description:
   -  Generates certificate request on a Cisco IMC Server
Input Params:
    name:
        description: certificate name
        required: True
    org:
        description: organization name
        required: True
    locality:
        description: locality
        required: True
    state:
        description: state
        required: True
    country:
        description: country code
        required: True
        choices: ['Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola',
        'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina',
        'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas',
        'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize',
        'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina',
        'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory'
        , 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi',
        'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands',
        'Central African Republic', 'Chad', 'Chile', 'China',
        'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros',
        'Congo', 'Cook Islands', 'Costa Rica', "Cote D'Ivoire (Ivory Coast)",
        'Croatia (Hrvatska)', 'Cuba', 'Cyprus', 'Czech Republic',
        'Czechoslovakia', 'Denmark', 'Djibouti', 'Dominica',
        'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt',
        'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia',
        'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland',
        'France, Metropolitan', 'France', 'French Guiana', 'French Polynesia',
        'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany',
        'Ghana', 'Gibraltar', 'Great Britain (UK)', 'Greece', 'Greenland',
        'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guinea', 'Guinea-Bissau'
        , 'Guyana', 'Haiti', 'Heard and McDonald Islands', 'Honduras',
        'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq'
        , 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan',
        'Kazakhstan', 'Kenya', 'Kiribati', 'Korea (North)', 'Korea (South)',
        'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho',
        'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg',
        'Macau', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives',
        'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania',
        'Mauritius', 'Mayotte', 'Mexico', 'Micronesia', 'Moldova', 'Monaco',
        'Mongolia', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia'
        , 'Nauru', 'Nepal', 'Netherlands Antilles', 'Netherlands',
        'Neutral Zone', 'New Caledonia', 'New Zealand (Aotearoa)',
        'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island',
        'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau',
        'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines',
        'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Reunion',
        'Romania', 'Russian Federation', 'Rwanda',
        'S. Georgia and S. Sandwich Isls.', 'Saint Kitts and Nevis',
        'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa',
        'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal',
        'Seychelles', 'Sierra Leone', 'Singapore', 'Slovak Republic',
        'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'Spain',
        'Sri Lanka', 'St. Helena', 'St. Pierre and Miquelon', 'Sudan',
        'Suriname', 'Svalbard and Jan Mayen Islands', 'Swaziland', 'Sweden',
        'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand',
        'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey',
        'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu',
        'US Minor Outlying Islands', 'USSR (former)', 'Uganda', 'Ukraine',
        'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay',
        'Uzbekistan', 'Vanuatu', 'Vatican City State (Holy See)', 'Venezuela',
        'Viet Nam', 'Virgin Islands (British)', 'Virgin Islands (U.S.)',
        'Wallis and Futuna Islands', 'Western Sahara', 'Yemen', 'Yugoslavia',
        'Zaire', 'Zambia', 'Zimbabwe']
    org_unit:
        description: organization unit name
        required: False
    email:
        description: Email
        required: False
    server:
        description: ip address of the remote server
        required: False
    username:
        description: remote server login user
        required: False
    password:
        description: remote server login password
        required: False
    file_name:
        description: file_name with full path for the certificate file
        required: False
    protocol:
        description: protocol to transfer file to remote server
        required: False
        choices: ['ftp', 'http', 'none', 'scp', 'sftp', 'tftp']
    self_signed:
        description: if self signed, (user, password, server, file, protocol) not required
        required: False
        default: False

requirements: ['imcsdk']
author: "Rahul Gupta(ragupta4@cisco.com)"
'''


EXAMPLES = '''
- name:
  cisco_imc_certificate:
    name:
    org:
    locality:
    state:
    country:
    org_unit:
    email:
    server:
    username:
    password:
    file_name:
    protocol:
    self_signed:
    state: "present"
    ip: "192.168.1.1"
    username: "admin"
    password: "password"
'''


def _argument_mo():
    return dict(
                name=dict(required=True, type='str'),
                org=dict(required=True, type='str'),
                locality=dict(required=True, type='str'),
                state=dict(required=True, type='str'),
                country=dict(required=True, type='str', choices=[
                    'Albania', 'Algeria', 'American Samoa', 'Andorra',
                    'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda',
                    'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria',
                    'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh',
                    'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin',
                    'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina',
                    'Botswana', 'Bouvet Island', 'Brazil',
                    'British Indian Ocean Territory', 'Brunei Darussalam',
                    'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia',
                    'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands',
                    'Central African Republic', 'Chad', 'Chile', 'China',
                    'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia',
                    'Comoros', 'Congo', 'Cook Islands', 'Costa Rica',
                    "Cote D'Ivoire (Ivory Coast)", 'Croatia (Hrvatska)',
                    'Cuba', 'Cyprus', 'Czech Republic', 'Czechoslovakia',
                    'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic',
                    'East Timor', 'Ecuador', 'Egypt', 'El Salvador',
                    'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia',
                    'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji',
                    'Finland', 'France, Metropolitan', 'France',
                    'French Guiana', 'French Polynesia',
                    'French Southern Territories', 'Gabon', 'Gambia',
                    'Georgia', 'Germany', 'Ghana', 'Gibraltar',
                    'Great Britain (UK)', 'Greece', 'Greenland', 'Grenada',
                    'Guadeloupe', 'Guam', 'Guatemala', 'Guinea',
                    'Guinea-Bissau', 'Guyana', 'Haiti',
                    'Heard and McDonald Islands', 'Honduras', 'Hong Kong',
                    'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq',
                    'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan',
                    'Kazakhstan', 'Kenya', 'Kiribati', 'Korea (North)',
                    'Korea (South)', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia',
                    'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein',
                    'Lithuania', 'Luxembourg', 'Macau', 'Macedonia',
                    'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali',
                    'Malta', 'Marshall Islands', 'Martinique', 'Mauritania',
                    'Mauritius', 'Mayotte', 'Mexico', 'Micronesia', 'Moldova',
                    'Monaco', 'Mongolia', 'Montserrat', 'Morocco',
                    'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal',
                    'Netherlands Antilles', 'Netherlands', 'Neutral Zone',
                    'New Caledonia', 'New Zealand (Aotearoa)', 'Nicaragua',
                    'Niger', 'Nigeria', 'Niue', 'Norfolk Island',
                    'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan',
                    'Palau', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru',
                    'Philippines', 'Pitcairn', 'Poland', 'Portugal',
                    'Puerto Rico', 'Qatar', 'Reunion', 'Romania',
                    'Russian Federation', 'Rwanda',
                    'S. Georgia and S. Sandwich Isls.',
                    'Saint Kitts and Nevis', 'Saint Lucia',
                    'Saint Vincent and the Grenadines', 'Samoa', 'San Marino',
                    'Sao Tome and Principe', 'Saudi Arabia', 'Senegal',
                    'Seychelles', 'Sierra Leone', 'Singapore',
                    'Slovak Republic', 'Slovenia', 'Solomon Islands',
                    'Somalia', 'South Africa', 'Spain', 'Sri Lanka',
                    'St. Helena', 'St. Pierre and Miquelon', 'Sudan',
                    'Suriname', 'Svalbard and Jan Mayen Islands', 'Swaziland',
                    'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan',
                    'Tanzania', 'Thailand', 'Togo', 'Tokelau', 'Tonga',
                    'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan',
                    'Turks and Caicos Islands', 'Tuvalu',
                    'US Minor Outlying Islands', 'USSR (former)', 'Uganda',
                    'Ukraine', 'United Arab Emirates', 'United Kingdom',
                    'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu',
                    'Vatican City State (Holy See)', 'Venezuela', 'Viet Nam',
                    'Virgin Islands (British)', 'Virgin Islands (U.S.)',
                    'Wallis and Futuna Islands', 'Western Sahara', 'Yemen',
                    'Yugoslavia', 'Zaire', 'Zambia', 'Zimbabwe']),
                org_unit=dict(required=False, type='str'),
                email=dict(required=False, type='str'),
                server=dict(required=False, type='str'),
                username=dict(required=False, type='str'),
                password=dict(required=False, type='str'),
                file_name=dict(required=False, type='str'),
                protocol=dict(required=False, type='str', choices=['ftp', 'http', 'none', 'scp', 'sftp', 'tftp']),
                self_signed=dict(required=False, type='bool', default=False),
    )


def _argument_imc_connection():
    return  dict(
        # ImcHandle
        imc_server=dict(required=False, type='dict'),

        # Imc server credentials
        imc_ip=dict(required=False, type='str'),
        imc_username=dict(required=False, default="admin", type='str'),
        imc_password=dict(required=False, type='str', no_log=True),
        imc_port=dict(required=False, default=None),
        imc_secure=dict(required=False, default=None),
        imc_proxy=dict(required=False, default=None)
    )


def _ansible_module_create():
    argument_spec = dict()
    argument_spec.update(_argument_mo())
    argument_spec.update(_argument_imc_connection())

    return AnsibleModule(argument_spec,
                         supports_check_mode=True)


def _get_mo_params(params):
    from ansible.module_utils.cisco_imc import ImcConnection
    args = {}
    for key in params:
        if ( ImcConnection.is_login_param(key) or
            params.get(key) is None):
            continue
        args[key] = params.get(key)
    return args


def setup_certificate(server, module):
    from imcsdk.apis.admin.certificate import certificate_signing_request_generate
    from imcsdk.apis.admin.certificate import certificate_exists

    ansible = module.params
    args_mo  =  _get_mo_params(ansible)
    exists, mo = certificate_exists(handle=server, **args_mo)

    if module.check_mode or exists:
        return not exists, False

    certificate_signing_request_generate(handle=server, **args_mo)
    return True, False


def setup(server, module):
    results = {}
    err = False

    try:
        results["changed"], err = setup_certificate(server, module)

    except Exception as e:
        err = True
        results["msg"] = "setup error: %s " % str(e)
        results["changed"] = False

    return results, err


def main():
    from ansible.module_utils.cisco_imc import ImcConnection

    module = _ansible_module_create()
    conn = ImcConnection(module)
    server = conn.login()
    results, err = setup(server, module)
    conn.logout()
    if err:
        module.fail_json(**results)
    module.exit_json(**results)


if __name__ == '__main__':
    main()

