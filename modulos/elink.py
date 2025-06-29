import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from colorama import Fore, Style
import socket

def elink():
    def extract_directories(url):
        directories = set()
        try:
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()  # Levanta exceção para códigos 4xx/5xx
            
            if 'text/html' not in response.headers.get('Content-Type', ''):
                print(f"{Fore.YELLOW}Aviso: O conteúdo em {url} não é HTML{Style.RESET_ALL}")
                return directories

            soup = BeautifulSoup(response.content, 'html.parser', from_encoding=response.encoding)
            base_url = urlparse(url).scheme + "://" + urlparse(url).netloc
            domain = urlparse(url).netloc

            for link in soup.find_all('a', href=True):
                try:
                    href = link['href'].strip()
                    if not href or href.startswith('javascript:'):
                        continue

                    if href.startswith('/') or base_url in href:
                        directory_url = urljoin(base_url, href) if href.startswith('/') else href
                        
                        parsed_url = urlparse(directory_url)
                        if parsed_url.scheme in ['http', 'https'] and domain in parsed_url.netloc:
                            directories.add(directory_url)
                except (ValueError, KeyError, AttributeError) as e:
                    print(f"{Fore.YELLOW}Aviso: Erro ao processar link {href}: {e}{Style.RESET_ALL}")
                    continue

        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}Erro ao acessar {url}: {type(e).__name__} - {str(e)}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Erro inesperado ao processar {url}: {type(e).__name__} - {str(e)}{Style.RESET_ALL}")

        return directories

    def extract_all_links(url):
        links = set()
        try:
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            
            if 'text/html' not in response.headers.get('Content-Type', ''):
                print(f"{Fore.YELLOW}Aviso: O conteúdo em {url} não é HTML{Style.RESET_ALL}")
                return links

            soup = BeautifulSoup(response.content, 'html.parser', from_encoding=response.encoding)
            base_url = urlparse(url).scheme + "://" + urlparse(url).netloc
            domain = urlparse(url).netloc

            for link in soup.find_all('a', href=True):
                try:
                    href = link['href'].strip()
                    if not href or href.startswith(('mailto:', 'tel:', 'javascript:')):
                        continue

                    full_url = urljoin(base_url, href) if href.startswith('/') else href
                    
                    parsed_url = urlparse(full_url)
                    if parsed_url.scheme in ['http', 'https'] and domain in parsed_url.netloc:
                        links.add(full_url)
                except (ValueError, KeyError, AttributeError) as e:
                    print(f"{Fore.YELLOW}Aviso: Erro ao processar link {href}: {e}{Style.RESET_ALL}")
                    continue

        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}Erro ao acessar {url}: {type(e).__name__} - {str(e)}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Erro inesperado ao processar {url}: {type(e).__name__} - {str(e)}{Style.RESET_ALL}")

        return links

    def extract_parameter_links(url):
        parameter_links = set()
        try:
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            
            if 'text/html' not in response.headers.get('Content-Type', ''):
                print(f"{Fore.YELLOW}Aviso: O conteúdo em {url} não é HTML{Style.RESET_ALL}")
                return parameter_links

            soup = BeautifulSoup(response.content, 'html.parser', from_encoding=response.encoding)
            base_url = urlparse(url).scheme + "://" + urlparse(url).netloc
            domain = urlparse(url).netloc

            for link in soup.find_all('a', href=True):
                try:
                    href = link['href'].strip()
                    if not href or href.startswith(('mailto:', 'tel:', 'javascript:')):
                        continue

                    if '?' in href or ('.php' in href and '=' in href):
                        full_url = urljoin(base_url, href) if href.startswith('/') else href
                        
                        parsed_url = urlparse(full_url)
                        if parsed_url.scheme in ['http', 'https'] and domain in parsed_url.netloc:
                            parameter_links.add(full_url)
                except (ValueError, KeyError, AttributeError) as e:
                    print(f"{Fore.YELLOW}Aviso: Erro ao processar link {href}: {e}{Style.RESET_ALL}")
                    continue

        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}Erro ao acessar {url}: {type(e).__name__} - {str(e)}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Erro inesperado ao processar {url}: {type(e).__name__} - {str(e)}{Style.RESET_ALL}")

        return parameter_links

    def get_valid_url(host):
        urls_to_try = [
            f"http://{host}",
            f"http://www.{host}",
            f"https://{host}",
            f"https://www.{host}"
        ]
        
        for url in urls_to_try:
            try:
                response = requests.head(url, timeout=10, allow_redirects=True)
                if response.status_code < 400:
                    return response.url  # Retorna a URL final após redirecionamentos
            except (requests.exceptions.RequestException, socket.gaierror) as e:
                print(f"{Fore.YELLOW}Tentativa falhou para {url}: {type(e).__name__}{Style.RESET_ALL}")
                continue
        
        print(f"{Fore.RED}Não foi possível estabelecer conexão com nenhuma variação do host.{Style.RESET_ALL}")
        return None

    print("\n\n\n--------- E-Link | Extrator de Links e Diretórios\n\n\n")
    
    while True:
        try:
            host = input("\n[\033[93m#\033[0m] Host (sem http/https) >> ").strip()
            if not host:
                print(f"{Fore.RED}Host não pode estar vazio.{Style.RESET_ALL}")
                continue
                
            url = get_valid_url(host)
            if url:
                break
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}Operação cancelada pelo usuário.{Style.RESET_ALL}")
            return

    while True:
        try:
            print("\nModo de extração:")
            print(f"{Fore.YELLOW}\n1 - 'Todos os diretórios'")
            print(f"{Fore.YELLOW}2 - 'Todos os links'")
            print(f"{Fore.YELLOW}3 - 'Links com parâmetros (?ref=pf, .php?=)'")
            print(f"{Fore.RED}0 - 'Sair'{Style.RESET_ALL}")

            mode = input(f"\nEscolha o modo >> ").strip()

            if mode == '1':
                directories = extract_directories(url)
                if directories:
                    print("\n\nDiretórios encontrados:")
                    for directory in sorted(directories):
                        print(f"{Fore.GREEN}{directory}{Style.RESET_ALL}")
                    print(f"\nTotal de diretórios encontrados: {Fore.CYAN}{len(directories)}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}\nNenhum diretório encontrado.{Style.RESET_ALL}")

            elif mode == '2':
                links = extract_all_links(url)
                if links:
                    print("\n\nTodos os links encontrados:")
                    for link in sorted(links):
                        print(f"{Fore.GREEN}{link}{Style.RESET_ALL}")
                    print(f"\nTotal de links encontrados: {Fore.CYAN}{len(links)}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}\nNenhum link encontrado.{Style.RESET_ALL}")

            elif mode == '3':
                parameter_links = extract_parameter_links(url)
                if parameter_links:
                    print("\n\nLinks com parâmetros encontrados:")
                    for link in sorted(parameter_links):
                        print(f"{Fore.GREEN}{link}{Style.RESET_ALL}")
                    print(f"\nTotal de links com parâmetros encontrados: {Fore.CYAN}{len(parameter_links)}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}\nNenhum link com parâmetros encontrado.{Style.RESET_ALL}")

            elif mode == '0':
                print(f"\n{Fore.RED}Encerrando o programa.{Style.RESET_ALL}")
                break

            else:
                print(f"{Fore.RED}\nOpção inválida. Escolha novamente.{Style.RESET_ALL}")

        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Operação interrompida. Voltando ao menu principal.{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{Fore.RED}Erro inesperado: {type(e).__name__} - {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    elink()