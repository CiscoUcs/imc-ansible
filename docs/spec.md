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

### 2.1.2 roles

### 2.1.3 NTP

### 2.1.4 authentication

### 2.1.5 SOL

### 2.1.6 KVM

### 2.1.7 CIMC properties (hostname)

### 2.1.8 SNMP (optional)

### 2.1.9 syslog (optional)



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


		imcsdk api sdk:
			imcsdk.apis.server.bios.boot_order_precision_set
			imcsdk.apis.server.bios.boot_order_precision_exists								
		
1. **`cisco_imc_boot_order_policy`**



### 2.3.2 BIOS tokens



### 2.3.3 Storage



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
