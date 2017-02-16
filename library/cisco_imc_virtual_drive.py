#!/usr/bin/env python

DOCUMENTATION = '''
---
module: cisco_imc_virtual_drive
short_description: Create and Delete virtual drives
version_added: "0.9.0.0"
description:
  - Create and Delete virtual drives on a Cisco IMC server
options:
  boot_drive:
    description: Set as boot drive
                example - True
    required: false

  drive_group:
    description: A list of drive groups. It needs to be a list of list.
                example - [[1]]
                        - [[1, 2]]
                        - [[1, 2],[3, 4]]
    required: true

  controller_type:
    description: Name of the controller
                example - 'SAS'
    required: false

  controller_slot:
    description: Name of the SAS controller slot
                example - "MEZZ", "0", .. , "9"
    required: true

  raid_level:
    description: Select the RAID level for the new virtual drives.
                 This can be one of the following,
                 Raid 0 Simple striping.
                 Raid 1 Simple mirroring.
                 Raid 5 Striping with parity.
                 Raid 6 Striping with two parity drives.
                 Raid 10 Spanned mirroring.
                 Raid 50 Spanned striping with parity.
                 Raid 60 Spanned striping with two parity drives.
    choices: ["0", "1", "10", "5", "50", "6", "60"]
    default: "0"
    required: false

  virtual_drive_name:
    description: name of the virtual drive
    required: false

  access_policy:
    description: Defines the host access level to the virtual drive.
                 This can be one of the following,
                  "read-write" Enables host to perform read-write on the VD.
                  "read-only" Host can only read from the VD.
                  "blocked" Host can neither read nor write to the VD.
    choices: ["blocked", "read-only", "read-write"]
    default: "read-write"
    required: false

  read_policy:
    description: The read-ahead cache mode.
    choices: ["always-read-ahead", "no-read-ahead"]
    default: "no-read-ahead"
    required: false

  cache_policy:
    description: The cache policy used for buffering reads.
    choices: ["cached-io", "direct-io"]
    default: "direct-io"
    required: false

  disk_cache_policy:
    description: The cache policy used for buffering reads.
                 This can be one of the following,
                  "unchanged" The disk cache policy is unchanged.
                  "enabled" Allows IO caching on the disk.
                  "disabled" Disallows disk caching.
    choices: ["disabled", "enabled", "unchanged"]
    default: "unchanged"
    required: false

  write_policy:
    description: This can be one of the following,
                  "Write Through" Data is written through the cache and to the physical drives. Performance is improved, because subsequent reads of that data can be satisfied from the cache.
                  "Write Back" Data is stored in the cache, and is only written to the physical drives when space in the cache is needed. Virtual drives requesting this policy fall back to Write Through caching when the BBU cannot guarantee the safety of the cache in the event of a power failure.
                  "Write Back Bad BBU" With this policy, write caching remains Write Back even if the battery backup unit is defective or discharged.
    choices: ["Always Write Back", "Write Back Good BBU", "Write Through", "always-write-back", "write-back-good-bbu", "write-through"]
    default: "Write Through"
    required: false

  strip_size:
    description: The size of each strip
    choices: ["1024k", "128k", "16k", "256k", "32k", "512k", "64k", "8k"]
    default: "64k"
    required: false

  size:
    description: The size of the virtual drive you want to create. Enter a value and select one of the following units - MB, GB, TB
    required: false

  admin_action:
    description: Enables drive security on classic platforms
    choices: ["enable-self-encrypt"]
    required: false

  server_id:
    description: Specify server id for UCS C3260 modular servers
    default: 1
    required: false

requirements: ['imcsdk']
author: "Vikrant Balyan(vvb@cisco.com)"
'''

EXAMPLES = '''
- name: Create virtual drive
  cisco_imc_virtual_drive:
    drive_group: [[1,2]]
    raid_level: 0
    controller_slot: "MEZZ"
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


def exists(server, module):
    from imcsdk.apis.server.storage import virtual_drive_exists as vd_exists
    from imcsdk.apis.server.storage import vd_name_derive

    ansible = module.params
    # VD name may have been derived while creation
    vd_name = ansible["virtual_drive_name"]
    if vd_name is None:
        vd_name = vd_name_derive(ansible["raid_level"],
                                 ansible["drive_group"])
    exists, err = vd_exists(handle=server,
                            controller_type=ansible['controller_type'],
                            controller_slot=ansible["controller_slot"],
                            virtual_drive_name=vd_name,
                            server_id=ansible['server_id'])
    if err:
        print(err)
    return exists


def virtual_drive(server, module):
    from imcsdk.apis.server.storage import virtual_drive_create as vd_create
    from imcsdk.apis.server.storage import vd_query_by_name
    from imcsdk.apis.server.storage import virtual_drive_delete as vd_delete
    from imcsdk.apis.server.storage import vd_name_derive

    results = {}
    err = False

    try:
        ansible = module.params
        _exists = exists(server, module)
        if ansible["state"] == "present":
            if module.check_mode or _exists:
                results["changed"] = not _exists
                return results, False

            print "size is %s" % ansible["size"]
            vd_create(handle=server,
                      drive_group=ansible["drive_group"],
                      controller_type=ansible['controller_type'],
                      controller_slot=ansible["controller_slot"],
                      raid_level=ansible["raid_level"],
                      virtual_drive_name=ansible["virtual_drive_name"],
                      access_policy=ansible["access_policy"],
                      read_policy=ansible["read_policy"],
                      cache_policy=ansible["cache_policy"],
                      disk_cache_policy=ansible["disk_cache_policy"],
                      write_policy=ansible["write_policy"],
                      strip_size=ansible["strip_size"],
                      size=ansible["size"],
                      server_id=ansible['server_id'])
            if ansible['boot_drive']:
                # VD name may have been derived while creation
                vd_name = ansible["virtual_drive_name"]
                if vd_name is None:
                    vd_name = vd_name_derive(ansible["raid_level"],
                                             ansible["drive_group"])
	        vd = vd_query_by_name(handle=server,
                                      controller_type=ansible['controller_type'],
 			              controller_slot=ansible['controller_slot'],
 			              name=vd_name,
 			              server_id=ansible['server_id'])
                vd.admin_action = 'set-boot-drive'
                server.set_mo(vd)
        else:
            if module.check_mode:
                results["changed"] = _exists
                return results, False

            if not _exists:
                results["changed"] = False
                return results, False

            # VD name may have been derived while creation
            vd_name = ansible["virtual_drive_name"]
            if vd_name is None:
                vd_name = vd_name_derive(ansible["raid_level"],
                                         ansible["drive_group"])

            vd_delete(handle=server,
                      controller_type=ansible['controller_type'],
                      controller_slot=ansible["controller_slot"],
                      name=vd_name,
                      server_id=ansible['server_id'])

        results["changed"] = True
    except Exception as e:
        err = True
        results["msg"] = str(e)
        results["changed"] = False
        if ansible["print_exception"]:
            raise

    return results, err


def main():
    from ansible.module_utils.basic import AnsibleModule
    from ansible.module_utils.cisco_imc import ImcConnection
    module = AnsibleModule(
        argument_spec=dict(
            boot_drive=dict(required=False, default=False, type='bool'),
            drive_group=dict(required=True, type='list'),
            controller_type=dict(required=False, default='SAS', type='str'),
            controller_slot=dict(required=True, type='str'),
            raid_level=dict(required=False,
                            default=0,
                            choices=[0, 1, 5, 6, 10, 50, 60],
                            type='int'),
            virtual_drive_name=dict(required=False, type='str'),
            access_policy=dict(required=False,
                               default="read-write",
                               choices=["blocked", "read-only", "read-write"],
                               type='str'),
            read_policy=dict(required=False,
                             default="no-read-ahead",
                             choices=["always-read-ahead", "no-read-ahead"],
                             type='str'),
            cache_policy=dict(required=False,
                              default="direct-io",
                              choices=["cached-io", "direct-io"],
                              type='str'),
            disk_cache_policy=dict(required=False,
                                   default="unchanged",
                                   choices=["disabled", "enabled", "unchanged"],
                                   type='str'),
            write_policy=dict(required=False,
                              default="Write Through",
                              choices=["Always Write Back", "Write Back Good BBU", "Write Through", "always-write-back", "write-back-good-bbu", "write-through"],
                              type='str'),
            strip_size=dict(required=False,
                            default="64k",
                            choices=["1024k", "128k", "16k", "256k", "32k", "512k", "64k", "8k"],
                            type='str'),
            size=dict(required=False, type='str'),
            admin_action=dict(required=False,
                              choices=["enable-self-encrypt"],
                              type='str'),
            state=dict(required=False,
                       default="present",
                       choices=["present", "absent"],
                       type='str'),
            server_id=dict(required=False, default=1, type='int'),

            # ImcHandle
            server=dict(required=False, type='dict'),

            # Imc server credentials
            ip=dict(required=False, type='str'),
            username=dict(required=False, default="admin", type='str'),
            password=dict(required=False, type='str'),
            port=dict(required=False, default=None),
            secure=dict(required=False, default=None),
            proxy=dict(required=False, default=None),

            # For debugging purposes
            print_exception=dict(required=False, default=False, type='bool')
        ),
        supports_check_mode=True
    )

    conn = ImcConnection(module)
    server = conn.login()
    results, err = virtual_drive(server, module)
    conn.logout()
    if err:
        module.fail_json(**results)
    module.exit_json(**results)


if __name__ == '__main__':
    main()
