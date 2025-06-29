import os
import requests
from http.client import HTTPConnection, HTTPSConnection
from colorama import Fore, init
from urllib.parse import urlparse
import socket
import ssl
init(autoreset=True)

def siteping():
    # Dicionário de status HTTP
    http_statuses = {
        100: "Continue", 101: "Switching Protocols", 200: "OK", 201: "Created", 202: "Accepted",
        203: "Non-Authoritative Information", 204: "No Content", 205: "Reset Content",
        206: "Partial Content", 300: "Multiple Choices", 301: "Moved Permanently", 302: "Found",
        303: "See Other", 304: "Not Modified", 305: "Use Proxy", 307: "Temporary Redirect",
        308: "Permanent Redirect", 400: "Bad Request", 401: "Unauthorized", 402: "Payment Required",
        403: "Forbidden", 404: "Not Found", 405: "Method Not Allowed", 406: "Not Acceptable",
        407: "Proxy Authentication Required", 408: "Request Timeout", 409: "Conflict",
        410: "Gone", 411: "Length Required", 412: "Precondition Failed", 413: "Payload Too Large",
        414: "URI Too Long", 415: "Unsupported Media Type", 416: "Range Not Satisfiable",
        417: "Expectation Failed", 500: "Internal Server Error", 501: "Not Implemented",
        502: "Bad Gateway", 503: "Service Unavailable", 504: "Gateway Timeout",
        505: "HTTP Version Not Supported"
    }

    def check_site(url):
        def get_response(url, use_https=True):
            try:
                parsed_url = urlparse(url if '://' in url else f'{"https" if use_https else "http"}://{url}')
                hostname = parsed_url.hostname
                if not hostname:
                    return None
                
                conn = HTTPSConnection(hostname, timeout=5) if use_https else HTTPConnection(hostname, timeout=5)
                path = parsed_url.path if parsed_url.path else '/'
                conn.request("HEAD", path)
                return conn.getresponse()
            except socket.gaierror:
                return None  # DNS lookup failed
            except ssl.SSLError:
                if use_https:
                    return get_response(url, use_https=False)
                return None
            except ConnectionRefusedError:
                return None
            except socket.timeout:
                return None
            except Exception as e:
                print(Fore.YELLOW + f"Erro ao verificar {url}: {str(e)}")
                return None

        response = get_response(url)
        if not response:
            response = get_response(url, use_https=False)
        
        if response:
            return response.status, http_statuses.get(response.status, "Unknown Status")
        else:
            return None, "Falha na conexão"

    online_sites = []

    print("   _____   _   _            _____    _                 ")
    print("  / ____| (_) | |          |  __ \  (_)                ")
    print(" | (___    _  | |_    ___  | |__) |  _   _ __     __ _ ")
    print("  \___ \  | | | __|  / _ \ |  ___/  | | | '_ \   / _` |")
    print("  ____) | | | | |_  |  __/ | |      | | | | | | | (_| |")
    print(" |_____/  |_|  \__|  \___| |_|      |_| |_| |_|  \__, |")
    print("                                                  __/ |")
    print("                                                 |___/ \n")

    # Solicitar link do Pastebin
    pastebin_url = input("Cole o link do Pastebin com a lista de sites: ").strip()
    
    # Converter para raw link se for um link normal do Pastebin
    if "pastebin.com" in pastebin_url and "/raw/" not in pastebin_url:
        pastebin_url = pastebin_url.replace("pastebin.com/", "pastebin.com/raw/")

    try:
        # Baixar conteúdo do Pastebin
        response = requests.get(pastebin_url, timeout=10)
        response.raise_for_status()
        
        if not response.text.strip():
            print(Fore.RED + "O Pastebin está vazio.")
            return
            
        sites = [site.strip() for site in response.text.splitlines() if site.strip()]
        
        if not sites:
            print(Fore.RED + "Nenhum site válido encontrado no Pastebin.")
            return
            
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Erro ao acessar o Pastebin: {str(e)}")
        return
    except Exception as e:
        print(Fore.RED + f"Erro inesperado ao processar o Pastebin: {str(e)}")
        return

    # Verificar cada site
    for site in sites:
        try:
            status, status_message = check_site(site)
            if status == 200:
                print(Fore.GREEN + f"{site} está online ({status} {status_message})")
                online_sites.append(f"{site} ({status} {status_message})")
            elif status:
                if status in (301, 302, 500):
                    print(Fore.YELLOW + f"{site} ({status} {status_message})")
                else:
                    print(Fore.RED + f"{site} ({status} {status_message})")
            else:
                print(Fore.LIGHTBLACK_EX + f"{site} não está online ({status_message})")
        except Exception as e:
            print(Fore.YELLOW + f"Erro ao processar o site {site}: {str(e)}")

    print(Fore.BLUE + "\nSites online (200 OK):")
    for site in online_sites:
        print(site)

    print(Fore.BLUE + f"\nTotal de sites online (200 OK): {len(online_sites)}")

if __name__ == "__main__":
    try:
        siteping()
    except KeyboardInterrupt:
        print(Fore.RED + "\nOperação interrompida pelo usuário.")
    except Exception as e:
        print(Fore.RED + f"Erro inesperado: {str(e)}")