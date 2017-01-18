# imc-ansible

## 1. Introduction
`imc-ansible` is a ansible module for Cisco UCS Integrated Management Controller line of servers. This document servers as a functional specification for `imc-ansible`.

Cisco IMC server configuration is divided into 3 flows,

1. initial conf to bring CIMC connectivity up

1. admin configuration that does not require server to be up and can be done with only CIMC being up

1. configuration to bring up a server


This module only targets the later 2 parts. The first part needs to be done manually by the user.


## 2. Configuration
The sections below describe a typical configuration flow that a customer follows. Every section also has the ansible modules that are implemented for it.

## 2.1 admin configuration
These are settings that an administrator would need to configure prior to bring a server up.

### 2.1.1 users

1. **`cisco_imc_user_password_policy`**

		Configures the password policy and password expiration policy for local users on a Cisco IMC server.
		
		Input Params:
			strong_password:
				description:
				This will enable the strong password policy.
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
		
		imcsdk apis:
			imcsdk.apis.admin.user.strong_password_set
			imcsdk.apis.admin.user.is_strong_password_set
			imcsdk.apis.admin.user.password_expiration_set
			imcsdk.apis.admin.user.password_expiration_exists		

2. **`cisco_imc_user`**

		Configures a local user on a Cisco IMC Server.
		
		Input Params:
			name: 
				description: Username for the local user
				required: True
			
			pwd:
				description: Password for the local user
				required: False
			
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
				
		imcsdk apis:
			imcsdk.apis.admin.user.local_user_create
			imcsdk.apis.admin.user.local_user_delete
			imcsdk.apis.admin.user.local_user_exists
			
		

### 2.1.2 roles

### 2.1.3 NTP

1. **`cisco_imc_ntp`**

		Configures NTP on a Cisco IMC server.
		
		Input Params:
			state: 
				description: Enables/Disables NTP
				choices: ["present", "absent"]
				default: "present"
				required: True
				
			ntp_servers:
				description: Dictionaries of NTP servers to be configured
								Format:  {"id": <id>, "ip": "<ip-address>"}
								Upto 4 ntp servers can be specified
				required: False
				
		imcsdk apis:
		    from imcsdk.apis.admin.ntp import ntp_enable
		    from imcsdk.apis.admin.ntp import ntp_disable
		    from imcsdk.apis.admin.ntp import ntp_setting_exists
		

### 2.1.4 authentication

### 2.1.5 SOL

### 2.1.6 KVM

### 2.1.7 Vmedia

### 2.1.8 CIMC properties (hostname)

### 2.1.9 SNMP (optional)

### 2.1.10 syslog (optional)



## 2.2 Firmware update

### 2.2.1 HUU

1. **`cisco_imc_firmware`**


## 2.3 Server Profile

### 2.3.1 BIOS boot order

1. **`cisco_imc_boot_order_precision`**

		Configures the boot order precision on a Cisco IMC server.
		It allows configuration of first level and second level boot order.

		Input Params:
			boot_devices:
				Takes input dictionaries that specify the boot order.
				First level boot order is restricted to the type of the device.
				order, device-type, name together form the first level boot order specification.
				Second level boot order delves deeper into a given device type.
				Parameters for second level boot order specification are category specifc.
				for example, pxe type can take slot, port as second level parameters.
				example input:
					- {"order": '1', "device-type": "hdd", "name": "hdd"},
    				- {"order": '2', "device-type": "pxe", "name": "pxe", "slot": "10", "port": "100"},
    				- {"order": '3', "device-type": "pxe", "name": "pxe1"},
    				- {"order": '4', "device-type": "usb", "name": "usb0", "subtype": "usb-cd"}

			configured_boot_mode:
				Configures the bios boot mode
				choices: ["Legacy", "None", "Uefi"]
				default: "Legacy"

			reboot_on_update:
				Specifies if the server should reboot after applying the changes
				choices: ["yes", "no"]
				default: "no"

			reapply
				# todo: vvb
				# what does this variable mean?? is it required to be exposed via ansible?

			server_id
				Specifies the server_id, required for UCS 3260 platform.
				This is not required for classic IMC platforms.
				default: 1


		imcsdk apis:
			imcsdk.apis.server.bios.boot_order_precision_set
			imcsdk.apis.server.bios.boot_order_precision_exists

1. **`cisco_imc_boot_order_policy`**


### 2.3.2 BIOS tokens


### 2.3.3 Storage

1. **`cisco_imc_virtual_drive`**

		**CHECK**
			- Does size needs to be specified always. or would it get auto-filled by the back-end based on number and size of drives
			- Any better way to specify drive_group?
			- Verify that drive_group needs to be the only mandatory parameter on the SDK API for VD creation


		Input Params:
			raid_level:
				description: Select the RAID level for the new virtual drives.
								This can be one of the following,
									Raid 0 — Simple striping.
									Raid 1 — Simple mirroring.
									Raid 5 — Striping with parity.
									Raid 6 — Striping with two parity drives.
									Raid 10 — Spanned mirroring.
									Raid 50 — Spanned striping with parity.
									Raid 60 — Spanned striping with two parity drives.
				choices: ["0", "1", "10", "5", "50", "6", "60"]
				default: "0"
				required: False

			drive_group:
				description: A list of drive groups
				required: True

			virtual_drive_name:
				description: name of the virtual drive
				required: False

			access_policy:
				description: Defines the host access level to the virtual drive.
							   This can be one of the following,
									"read-write" — Enables host to perform read-write on the VD.
									"read-only" — Host can only read from the VD.
									"blocked" — Host can neither read nor write to the VD.
				choices: ["blocked", "read-only", "read-write"]
				default: "read-write"
				required: False

			read_policy:
				description: The read-ahead cache mode.
				choices: ["always-read-ahead", "no-read-ahead"]
				default: "no-read-ahead"
				required: False

			cache_policy:
				description: The cache policy used for buffering reads.
				choices: ["cached-io", "direct-io"]
				default: "direct-io"
				required: False

			disk_cache_policy:
				description: The cache policy used for buffering reads.
								This can be one of the following,
									"unchanged" — The disk cache policy is unchanged.
									"enabled" — Allows IO caching on the disk.
									"disabled" — Disallows disk caching.
				choices: ["disabled", "enabled", "unchanged"]
				default: "unchanged"
				required: False

			write_policy:
				description: This can be one of the following,
								Write Through — Data is written through the cache and to the physical drives. Performance is improved, because subsequent reads of that data can be satisfied from the cache.
								Write Back — Data is stored in the cache, and is only written to the physical drives when space in the cache is needed. Virtual drives requesting this policy fall back to Write Through caching when the BBU cannot guarantee the safety of the cache in the event of a power failure.
								Write Back Bad BBU — With this policy, write caching remains Write Back even if the battery backup unit is defective or discharged.
				choices: ["Always Write Back", "Write Back Good BBU", "Write Through", "always-write-back", "write-back-good-bbu", "write-through"]
				default: "write-through"
				required: False

			strip_size:
				description: The size of each strip
				choices: ["1024k", "128k", "16k", "256k", "32k", "512k", "64k", "8k"]
				default: "64k"
				required: False

			size:
				description: The size of the virtual drive you want to create. Enter a value and select one of the following units - MB, GB, TB
				required: False

			admin_action:
				description: todo - classic only property - enables SED! ???
				choices: ["enable-self-encrypt"]
				required: False

			state:
				description: Defines if the VD should be created or deleted
				choices: ["present", "absent"]
				default: "present"
				required: True

		imcsdk apis:
			imcsdk.apis.server.storage.vd_create
			imcsdk.apis.server.storage.vd_delete
			imcsdk.apis.server.storage.vd_exists
			imcsdk.apis.server.storage.vd_init
			imcsdk.apis.server.storage.vd_boot_drive_set
			imcsdk.apis.server.storage.vd_transport_ready_set

### 2.3.4 Network

1. **`cisco_imc_vic_adapter`**

1. **`cisco_imc_vnic`**

1. **`cisco_imc_vhba`**


## 3. Roles
Ansible roles are a method of structuring complex monolithic playbooks into different roles that may be included by other playbooks.

The roles exposed by `imc-ansible` modules are,

### 3.1 `common`

### 3.2 `boot`

### 3.3 `storage`

### 3.4 `vnic`

### 3.5 `vhba`




## 4. Requirements

### 4.1 standalone execution
A user should be able to execute a single module individually. This requires every module to also have login and logout capabilities. To accomodate this, every module except `cisco_imc_login` and `cisco_imc_logout` will accept the following inputs,

```
server:
	server connection handle from a `cisco_imc_login` task
```


```
ip:
	hostname/ip of the server
username:
	username to be used for login
password:
	password for user specified above
port:
	port to be used to login
secure:
	use https connection
proxy
	specifies a proxy server url, if the connection needs a proxy
```

#### 4.1.1 single login/logout with multiple tasks
When using a playbook with multiple tasks, a user can start with `cisco_imc_login` and save(`register`) the ouput to `server_out` variable. The `server_out.handle` variable can then be passed to the consecutive tasks as input parameter.

The playbook can finish with `cisco_imc_logout` which takes `server_out.handle` as input.

If a login was done via `cisco_imc_login` then a `cisco_imc_logout` must be present in the playbook.

```
- name: login to server
  cisco_imc_login:
    - ip: "192.168.1.1"
    - username: "admin"
    - password: "password"
  register: server_out

- name: configure boot order precision
  cisco_imc_boot_order_precision:
    - boot_devices:
        - {"order": "1", "device-type": "pxe", "name": "pxe"}
        - {"order": "2", "device-type": "lan", "name": "lan"}
    - boot_mode: "Legacy"
    - server: {{ server_out.handle }}

# many other tasks..
# ...
# ...


- name: logout from server
  cisco_imc_logout:
    - server: {{ server_out.handle }}
  register: server

```


#### 4.1.2 login/logout per task
To be able to support running a module individually, we also accept the credentials directly in a task. we use these to create a session if the `server` parameter is not defined.

```
- name: configure boot order precision
  cisco_imc_boot_order_precision:
    - boot_devices:
        - {"order": "1", "device-type": "pxe", "name": "pxe"}
        - {"order": "2", "device-type": "lan", "name": "lan"}
    - boot_mode: "Legacy"
    - ip: "192.168.1.1"
    - username: "admin"
    - password: "password"
```
