# imc-ansible

## introduction
`imc-ansible` is a ansible module for Cisco UCS Integrated Management Controller line of servers. This document servers as a functional specification for `imc-ansible`.

Cisco IMC server configuration is divided into 3 flows,

1. initial conf to bring CIMC connectivity up

1. admin configuration that does not require server to be up and can be done with only CIMC being up

1. configuration to bring up a server


This module only targets the later 2 parts. The first part needs to be done manually by the user.


# configuration
The sections below describe a typical configuration flow that a customer follows. 

## admin configuration
These are settings that an administrator would need to configure prior to bring a server up.

### users

### roles

### NTP

### authentication

### SNMP (optional)

### syslog (optional)

### CIMC properties (hostname)

### SOL

### KVM



## Firmware update

### HUU

1. **`cisco_imc_firmware`**


## Server Profile

### BIOS boot order

1. **`cisco_imc_boot_order_precision`**

		Configures the boot order precision on a Cisco IMC server. It allows configuration of first level and second level boot order.
		
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

			server_id
				Specifies the server_id, required for UCS 3260 platform. 
				This is not required for classic IMC platforms.
				default: 1
					
		
1. **`cisco_imc_boot_order_policy`**



### BIOS tokens



### Storage

