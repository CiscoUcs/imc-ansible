```
➔ ansible-playbook -i inventory site.yml

PLAY [127.0.0.1] ****************************************************************************

TASK [Gathering Facts] **********************************************************************
ok: [localhost]

TASK [common : check if imcsdk is installed] ************************************************
ok: [localhost]

TASK [common : install imcsdk] **************************************************************
skipping: [localhost]

TASK [boot : set boot order] ****************************************************************
changed: [localhost]

TASK [boot : set boot order alternate] ******************************************************
changed: [localhost]

PLAY RECAP **********************************************************************************
localhost                  : ok=4    changed=2    unreachable=0    failed=0

```
