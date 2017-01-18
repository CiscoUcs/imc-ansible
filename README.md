```
➔ ansible-playbook -i inventory site.yml

PLAY [imc] *********************************************************************

TASK [common : check if imcsdk is installed] ***********************************
ok: [batman]

TASK [common : install imcsdk] *************************************************
skipping: [batman]

TASK [admin : set password policy] *********************************************
ok: [batman]

TASK [admin : create local user] ***********************************************
changed: [batman]

TASK [admin : delete local user] ***********************************************
changed: [batman]

TASK [admin : reset password policy] *******************************************
changed: [batman]

TASK [admin : enable ntp] ******************************************************
changed: [batman]

TASK [admin : disable ntp] *****************************************************
changed: [batman]

TASK [boot : set boot order] ***************************************************
changed: [batman]

TASK [boot : set boot order alternate] *****************************************
changed: [batman]

TASK [storage : create virtual drive] ******************************************
changed: [batman]

TASK [storage : delete virtual drive] ******************************************
changed: [batman]

PLAY RECAP *********************************************************************
batman                    : ok=11   changed=9    unreachable=0    failed=0

```
