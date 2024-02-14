[![](https://ucspython.herokuapp.com/badge.svg)](https://ucspython.herokuapp.com)

# imc-ansible

* Apache License, Version 2.0 (the "License")

# install
- ansible must be installed
```
sudo pip install ansible
```
- you will need the latest imcsdk.
```
sudo pip install imcsdk
```
- install this repository as an ansible galaxy collection OR by cloning this repository
    ```bash
    # Install as an Ansible Galaxy collection
    ansible-galaxy collection install git+https://github.com/CiscoUcs/imc-ansible.git --upgrade
    ```
    ```bash
    # OR Install by cloning tis repository
    git clone https://github.com/ciscoucs/imc-ansible
    cd imc-ansible
    ```

If you install via cloning this repository:
- You will need to run playbooks from the imc-ansible module directory so that local modules are available from the library subdirectory.
- See https://docs.ansible.com/ansible/latest/dev_guide/developing_locally.html for more information on Ansible's use of local modules.

# imc_managed_objects module usage and examples
The imc_managed_objects module provides access to the full IMC API through the imcsdk.  imc_managed_objects requires the imcsdk
module, class, and any needed properties for configuration.  Visore (available on the IMC browser at 'https://<imc ip>/visore.html') can
be used to help find Class names and required proerties on objects.

Examples using imc_managed_objects are provided in the playbooks directory, and here is example usage:
```
ansible-playbook -i example_inventory vnic_config.yml

PLAY [cimc] ***************************************************************************************************************************************************************************

TASK [Gather IMC inventory] ***
```

# roles usage
`site.yml` and the various playbooks in the `roles` folder can be used as an
example on how to use the various modules that are a part of this package.

Users can create a new playbook `flow.yml` and pick taks from the example
roles and use them. Users can also modify the existing tasks and execute the
plays as shown in the next section of the readme.

`inventory` file should be updated to mention the connection details of the
server.


# sample run using site.yml and roles
```
➔ ansible-playbook -i inventory site.yml

PLAY [imc]
*********************************************************************

TASK [common : check if imcsdk is installed]
***********************************
ok: [fpmr1_192.168.1.1]

TASK [common : install imcsdk]
*************************************************
skipping: [fpmr1_192.168.1.1]

TASK [admin : set password policy]
*********************************************
changed: [fpmr1_192.168.1.1]

TASK [admin : create local user]
***********************************************
changed: [fpmr1_192.168.1.1]

TASK [admin : delete local user]
***********************************************
changed: [fpmr1_192.168.1.1]

TASK [admin : reset password policy]
*******************************************
changed: [fpmr1_192.168.1.1]

TASK [admin : enable ntp]
******************************************************
changed: [fpmr1_192.168.1.1]

TASK [admin : disable ntp]
*****************************************************
changed: [fpmr1_192.168.1.1]

TASK [admin : enable LDAP]
*****************************************************
changed: [fpmr1_192.168.1.1]

TASK [admin : disable LDAP]
****************************************************
changed: [fpmr1_192.168.1.1]

TASK [boot : set boot order]
***************************************************
changed: [fpmr1_192.168.1.1]

TASK [boot : set boot order alternate]
*****************************************
changed: [fpmr1_192.168.1.1]

TASK [storage : create virtual drive]
******************************************
changed: [fpmr1_192.168.1.1]

TASK [storage : delete virtual drive]
******************************************
changed: [fpmr1_192.168.1.1]

PLAY RECAP
*********************************************************************
fpmr1_192.168.1.1       : ok=13   changed=12   unreachable=0    failed=0
```

# Community:

* We are on Slack - slack requires registration, but the ucspython team is open invitation to
  anyone to register [here](https://ucspython.herokuapp.com) 
