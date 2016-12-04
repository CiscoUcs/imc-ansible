```
➔ ansible-playbook -i hosts site.yml -k
SSH password:

PLAY [all]
*******************************************************************************************************

TASK [Gathering Facts]
*******************************************************************************************
ok: [localhost]

TASK [common : check if imcsdk is installed]
*********************************************************************
fatal: [localhost]: FAILED! => {"changed": false, "cmd": "python -c \"import
imcsdk\", "delta": "0:00:00.011486", "end": "2016-12-04 12:49:48.712304",
"failed": true, "rc": 1, "start": "2016-12-04 12:49:48.700818", "stderr":
"Traceback (most recent call last):\n  File \"<string>\", line 1, in
<module>\nImportError: No module named imcsdk", "stdout": ", "stdout_lines": [], "warnings": []}
...ignoring

TASK [common : install imcsdk]
***********************************************************************************
changed: [localhost]

TASK [boot : running a test task]
********************************************************************************
changed: [localhost]

PLAY RECAP
*******************************************************************************************************
localhost                  : ok=4    changed=2    unreachable=0    failed=0

```
