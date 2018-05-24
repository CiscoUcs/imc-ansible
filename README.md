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
git clone https://github.com/ciscoucs/imcsdk
cd imcsdk
sudo make install
```
- clone this repository and install the ansible modules
```
git clone https://github.com/ciscoucs/imc-ansible
cd imc-ansible
sudo python install.py
```

# uninstall
```
cd imc-ansible
sudo python uninstall.py
```

# usage
`site.yml` and the various playbooks in the `roles` folder can be used as an
example on how to use the various modules that are a part of this package.

Users can create a new playbook `flow.yml` and pick taks from the example
roles and use them. Users can also modify the existing tasks and execute the
plays as shown in the next section of the readme.

`inventory` file should be updated to mention the connection details of the
server.


# sample run
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
