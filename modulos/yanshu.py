from bs4 import BeautifulSoup
import re
import requests
import concurrent.futures
from colorama import init, Fore
import time

def yanshu():
    # Função principal que contém todas as outras
    YELLOW = '\033[93m'
    RESET = '\033[0m'

    def show_banner():
        print(YELLOW + "\n        .--.       .--.")
        print("    _  `    \     /    `  _")
        print("     `\.===. \.^./ .===./`")
        print("         ,  | 2.0 |  ,")

    def parse_search_results(response_text, domain):
        subdomains = set()
        matches = re.findall(r'(?:https?:\/\/)?([a-zA-Z0-9\-\.]+\.' + re.escape(domain) + r')', response_text)
        for match in matches:
            subdomains.add(match)
        return subdomains

    def search_dns_dumpster(domain, subdomains_found):
        try:
            time.sleep(0.5)
            print(f"{Fore.GREEN}[-] Procurando no DNS Dumpster por {domain}...")
            subdomains_found.add("[!] DNS Dumpster não suportado diretamente.")
        except Exception as e:
            subdomains_found.add(f"[!] Erro: Falha na busca no DNS Dumpster: {e}")

    def search_virustotal(domain, subdomains_found):
        try:
            time.sleep(0.5)
            print(f"{Fore.GREEN}[-] Procurando no Virustotal por {domain}...")
            response = requests.get(f"https://www.virustotal.com/ui/domains/{domain}/subdomains")
            response.raise_for_status()
            subdomains = parse_search_results(response.text, domain)
            subdomains_found.update(subdomains)
        except requests.exceptions.RequestException as e:
            subdomains_found.add(f"[!] Erro: Falha na busca no Virustotal: {e}")

    def search_threatcrowd(domain, subdomains_found):
        try:
            time.sleep(0.5)
            print(f"{Fore.GREEN}[-] Procurando no ThreatCrowd por {domain}...")
            response = requests.get(f"https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={domain}")
            response.raise_for_status()
            data = response.json()
            if 'subdomains' in data:
                subdomains = set(data['subdomains'])
                subdomains_found.update(subdomains)
        except requests.exceptions.RequestException as e:
            subdomains_found.add(f"[!] Erro: Falha na busca no ThreatCrowd: {e}")
        except KeyError:
            subdomains_found.add("[!] Erro: Formato de resposta do ThreatCrowd inválido")

    def search_ssl_certificates(domain, subdomains_found):
        try:
            time.sleep(0.5)
            print(f"{Fore.GREEN}[-] Procurando em Certificados SSL por {domain}...")
            response = requests.get(f"https://crt.sh/?q=%.{domain}")
            response.raise_for_status()
            subdomains = parse_search_results(response.text, domain)
            subdomains_found.update(subdomains)
        except requests.exceptions.RequestException as e:
            subdomains_found.add(f"[!] Erro: Falha na busca em Certificados SSL: {e}")

    def search_passive_dns(domain, subdomains_found):
        try:
            time.sleep(0.5)
            print(f"{Fore.GREEN}[-] Procurando no PassiveDNS por {domain}...")
            response = requests.get(f"https://www.passivedns.cn/search/?q={domain}")
            response.raise_for_status()
            subdomains = parse_search_results(response.text, domain)
            subdomains_found.update(subdomains)
        except requests.exceptions.RequestException as e:
            subdomains_found.add(f"[!] Erro: Falha na busca no PassiveDNS: {e}")

    def search_source(source_name, url, domain, subdomains_found, total_unique_subdomains):
        try:
            time.sleep(0.5)
            print(f"{Fore.GREEN}[-] Procurando em {source_name}...")
            if url:
                response = requests.get(url)
                response.raise_for_status()
                subdomains = parse_search_results(response.text, domain)
                subdomains_found.update(subdomains)
                total_unique_subdomains[0] += len(subdomains)
        except requests.exceptions.RequestException as e:
            subdomains_found.add(f"[!] Erro: Falha na busca em {source_name}: {e}")

    def find_subdomains():
        domain = input("\n\nDigite o domínio para buscar subdomínios (exemplo: google.com): ").strip()
        subdomains_found = set()
        total_unique_subdomains = [0]
        init()

        sources = [
            ("Baidu", f"https://www.baidu.com/s?wd=site:{domain}"),
            ("Yahoo", f"https://search.yahoo.com/search?p=site:{domain}"),
            ("Google", f"https://www.google.com/search?q=site:{domain}"),
            ("Bing", f"https://www.bing.com/search?q=site:{domain}"),
            ("Ask", f"https://www.ask.com/web?q=site:{domain}"),
            ("Netcraft", f"https://www.netcraft.com/search/?host={domain}"),
            ("Virustotal", f"https://www.virustotal.com/ui/domains/{domain}/subdomains"),
            ("ThreatCrowd", f"https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={domain}"),
            ("SSL Certificates", f"https://crt.sh/?q=%.{domain}"),
            ("PassiveDNS", f"https://www.passivedns.cn/search/?q={domain}"),
            ("Censys", f"https://censys.io/domain/{domain}/table"),
            ("Shodan", f"https://www.shodan.io/search?query=hostname:{domain}"),
            ("SecurityTrails", f"https://securitytrails.com/list/apex_domain/{domain}")
        ]

        print(f"{Fore.GREEN}[-] Enumerando subdomínios agora para {domain}")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for source_name, url in sources:
                if source_name == "DNSdumpster":
                    futures.append(executor.submit(search_dns_dumpster, domain, subdomains_found))
                elif source_name == "Virustotal":
                    futures.append(executor.submit(search_virustotal, domain, subdomains_found))
                elif source_name == "ThreatCrowd":
                    futures.append(executor.submit(search_threatcrowd, domain, subdomains_found))
                elif source_name == "SSL Certificates":
                    futures.append(executor.submit(search_ssl_certificates, domain, subdomains_found))
                elif source_name == "PassiveDNS":
                    futures.append(executor.submit(search_passive_dns, domain, subdomains_found))
                else:
                    futures.append(executor.submit(search_source, source_name, url, domain, subdomains_found, total_unique_subdomains))
            
            for future in concurrent.futures.as_completed(futures):
                pass

        valid_subdomains = {subdomain for subdomain in subdomains_found if not subdomain.startswith("[!")}
        for subdomain in sorted(valid_subdomains):
            print(subdomain)

        print(f"{Fore.GREEN}\n[-] Total de Subdomínios Únicos Encontrados: {len(valid_subdomains)}")

    # Mostra o banner e executa a busca
    show_banner()
    find_subdomains()

