# Sheller

Sheller is a Windows Post Exploitation Tool to bypass all known Anti-Malware Scanner Interfaces including Defender, Bitdefender, Kaspersky, McAfee, NANO-Antivirus, Kingsoft, Avast, Avira and many more.



For use python3 and powershell (Windows) or pwsh (Linux) are required, the script supports Windows and Linux distribution.
The module sheller is to gain reverse shell to the victims device, providing several amsi bypass module such as encoding, chunking and var randomization.
There is a module to disable any windows defender antivirus feature if executed with admin privileges too.
# Getting started
To see Information:
```python 
python3 sheller.py
```
![sheller_help](https://user-images.githubusercontent.com/73026669/150557890-cdb78323-3708-4932-8355-c98f5b05a660.jpg)


# Example
``
python sheller.py -s xy.bat -lh lh -lp 4444 -b64 -ch -v: 
``

<a href="https://www.virustotal.com/gui/file/2fc4ec778c03a989fd74fa878617dc22e7efc35e8d906b51af611562d1b0b418?nocache=1">fully undetected AMSI Scan Results</a>

[![](https://user-images.githubusercontent.com/73026669/150165109-71b9f841-3b8e-42bd-a502-5d666244eaaf.png)](https://www.virustotal.com/gui/file/2fc4ec778c03a989fd74fa878617dc22e7efc35e8d906b51af611562d1b0b418?nocache=1)
