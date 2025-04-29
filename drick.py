



############################################
# Drick Project ############################
############################################
# Desenvolvido pela SecBras Research #######
############################################


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\  \

import os
import random
import socket
import requests
import pycountry
import threading
import time
import platform
import psutil # type: ignore

from http.client import HTTPConnection, HTTPSConnection
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from colorama import Fore, Style, init
from datetime import datetime
from colorama import init
init()




################################################## Funções ##################################################



######################################## Testar host ON/OFF ########################################


def ping():
    try:
        print("Você pode testar os seguintes modelos:\n")
        print("1 - \033[33m\"www.google.com\"\033[0m")
        print("2 - \033[33m\"google.com\"\033[0m")
        print("3 - \033[33m\"8.8.8.8 (Google DNS)\"\033[0m")

        host = input("\n[\033[93m#\033[0m] Host >> ")
        print("\n")
        try:
            socket.inet_aton(host)  # Verifica se o host é um IP válido
        except socket.error:
            pass  # Se não for um IP, continua com o hostname

        host_online = False  # Variável para verificar se o host está online

        # Função para verificar a conectividade em uma porta específica
        def check_port(host, port, service):
            nonlocal host_online  # Acessa a variável host_online da função pai

            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)  # Define um timeout de 5 segundos

                try:
                    result = sock.connect_ex((host, port))

                    if result == 0:
                        print(f"\033[32m ✔️ \033[0m {host}:{port} ({service}) está online.")
                        host_online = True  # Marca o host como online se pelo menos uma porta estiver online
                    else:
                        print(f"\033[31m ❌ \033[0m {host}:{port} ({service}) está offline ou inacessível.")
                except socket.error as e:
                    print(f"\033[31mErro ao conectar com {host}:{port} ({service}): {e}\033[0m")
                finally:
                    sock.close()

            except Exception as e:
                print(f"\033[31mErro ao verificar a conectividade com {host}:{port} ({service}): {e}\033[0m")

        # Verificações de portas
        check_port(host, 80, "HTTP")
        check_port(host, 443, "HTTPS")
        check_port(host, 21, "FTP")
        check_port(host, 22, "SSH")
        check_port(host, 25, "SMTP")
        check_port(host, 110, "POP3")
        check_port(host, 143, "IMAP")
        check_port(host, 3306, "MySQL")
        check_port(host, 5432, "PostgreSQL")
        check_port(host, 27017, "MongoDB")

        # Imprime mensagem final se o host estiver online ou offline
        if host_online:
            print(f"\nHost {host} está \033[32monline\033[0m.")
        else:
            print(f"\nHost {host} está \033[31moffline para essas portas\033[0m.")

    except Exception as e:
        print(f"\033[31mErro ao verificar a conectividade com {host}: {e}\033[0m")
	
	
########################################   Capturar IP   ###########################################

def capip():
	try:
		ent = input("\n[\033[93m#\033[0m] Host >> ")
		ip = socket.gethostbyname(ent)
		ip = "\033[32m" + ip + "\033[0;0m"
		capt = ("\nIP: ")
		print (capt, ip)
	except:
		print("\nComando inválido.")
	

########################################     CBANNER     ###########################################


def cbanner():
    host = input("\n[\033[93m#\033[0m] Host >> ")
    porta = int(input("\n[\033[93m#\033[0m] Porta >> "))

    if porta == 21:
        s = socket.socket()
        s.settimeout(3)
        s.connect((host, porta))
        rf = s.recv(1030)
        print("\033[32m" + "\nBanner capturado" + "\033[0m", rf.decode(), "\n")

    if porta == 22:
        s = socket.socket()
        s.settimeout(3)
        s.connect((host, porta))
        rf = s.recv(1030)
        print("\033[32m" + "\nBanner capturado" + "\033[0m", rf.decode(), "\n")

    if porta == 25:
        s = socket.socket()
        s.settimeout(3)
        s.connect((host, porta))
        rf = s.recv(1030)
        print("\033[32m" + "\nBanner capturado" + "\033[0m", rf.decode(), "\n")

    if porta == 80 or porta == 443:
        try:
            s = socket.socket()
            s.connect((host, porta))
            s.send(b'GET / HTTP/1.1\r\nHost: ' + host.encode() + b'\r\n\r\n')
            rf = s.recv(10000)
            print("\033[32m" + "\nBanner capturado" + "\033[0m", rf.decode(), "\n")
        except Exception as e:
            print(f"Falha ao capturar banner na porta {porta}: {str(e)}")

    else:
        print("Porta não suportada.")


######################################## Testar porta especifica ###################################

def tporta():
	try:
		host = input("\n[\033[93m#\033[0m] Host >> ")
		porta = int(input("\n[\033[93m#\033[0m] Porta >> "))
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(4)
		result = sock.connect_ex((host, porta))
		if result == 0:
			str = "\033[32mestá aberta. \033[0;0m"
			print ("\nPorta", porta, str)
		else:
			str = "\033[31mestá fechada. \033[0;0m"
			print ("\nPorta", porta, str)
	except:
		print("\nComando inválido.")
    	 	

########################################   Localizador de IP   #####################################


def geoip():
    try:
        host = input("\n[\033[93m#\033[0m] Host >> ")
        
        # Verifica se o input é um URL completo e extrai o hostname
        parsed_url = urlparse(host)
        if parsed_url.scheme and parsed_url.netloc:
            host = parsed_url.netloc
        
        ip_address = socket.gethostbyname(host)

        endpoints = {
            "País": f"https://ipapi.co/{ip_address}/country_name/",
            "Estado": f"https://ipapi.co/{ip_address}/region/",
            "Cidade": f"https://ipapi.co/{ip_address}/city/",
            "Organização": f"https://ipapi.co/{ip_address}/org/",
            "ASN": f"https://ipapi.co/{ip_address}/asn/",
            "Coordenadas": f"https://ipapi.co/{ip_address}/latlong/"
        }

        info_list = []

        def fetch_geo_data(url):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    return response.text.strip()
                else:
                    return None
            except requests.RequestException as e:
                print(f"Erro ao fazer requisição HTTP: {e}")
                return None

        info_list.append(f"IP: \033[32m{ip_address}\033[0;0m")
        for key in ["País", "Estado", "Cidade", "Organização", "ASN", "Coordenadas"]:
            url = endpoints[key]
            data = fetch_geo_data(url)
            if data:
                if key == "Coordenadas":
                    info_list.append(f"{key}: \033[32m{data}\033[0;0m")
                else:
                    info_list.append(f"{key}: \033[32m{data}\033[0;0m")

        print("\n")
        for info in info_list:
            print(info)
        print("\n")

        # Gerando o link do Google Maps com as coordenadas
        latitude = info_list[-1].split(':')[1].strip().split(',')[0]
        longitude = info_list[-1].split(':')[1].strip().split(',')[1]
        maps_link = f"\033[32mhttps://www.google.com/maps/search/?api=1&query={latitude},{longitude}\033[0;0m"
        print(f"Link para o Google Maps com as coordenadas: {maps_link}")

    except socket.gaierror:
        print("Erro ao obter o endereço IP. Verifique o host inserido.")
    except Exception as e:
        print(f"Erro desconhecido: {e}")


########################################    PORT SCAN        #######################################


def pscan():
    # Definindo a classe de cores para os prints
    class bcolors:
        GREEN = '\033[92m'
        RED = '\033[91m'
        END = '\033[0m'

    ip = input("\n[\033[93m#\033[0m] Host >> ")
    scan_mode = input("Escolha o modo de escaneamento (1 - Portas Comuns / 2 - Todas as Portas): ")

    open_ports = []  # Lista para armazenar as portas abertas
    
    print("\n")
    
    if scan_mode == '1':
        # Portas mais comuns sem duplicatas
        ports = [
            21,    # FTP
            22,    # SSH
            23,    # Telnet
            25,    # SMTP
            53,    # DNS
            80,    # HTTP
            110,   # POP3
            115,   # SFTP
            135,   # RPC
            139,   # NetBIOS
            143,   # IMAP
            161,   # SNMP
            194,   # IRC
            443,   # HTTPS
            445,   # SMB
            993,   # IMAPS
            995,   # POP3S
            1723,  # PPTP
            3306,  # MySQL
            3389,  # RDP
            5900,  # VNC
            8080,  # HTTP Alternate
            8443,  # HTTPS Alternate
            6667,  # IRC Alternative
            5432,  # PostgreSQL
            5800,  # VNC HTTP
            5901,  # VNC HTTP Alternate
            5902,  # VNC HTTP Alternate 2
            2222,  # SSH Alternative
            2000   # Call of Duty
        ]
    elif scan_mode == '2':
        ports = range(1, 65536)  # Todas as portas de 1 a 65535
    else:
        print("Modo de escaneamento inválido. Escolha 1 para Portas Comuns ou 2 para Todas as Portas.")
        return

    # Percorre as portas de acordo com o modo escolhido
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # Tempo limite de 1 segundo para conexão
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)  # Adiciona a porta à lista de portas abertas
                print(f"Porta {port} {bcolors.GREEN}está aberta{bcolors.END}")
            else:
                print(f"Porta {port} {bcolors.RED}não está respondendo{bcolors.END}")
            sock.close()
        except socket.error:
            print(f"Erro ao conectar-se à porta {port}.")
            pass

    # Imprime as portas abertas encontradas
    if open_ports:
        print("\nPortas abertas encontradas:")
        print(open_ports)
    else:
        print("\nNenhuma porta aberta encontrada.")


########################################        Elink          #####################################


def elink():
    def extract_directories(url):
        directories = set()
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extrair a URL base para lidar com links relativos corretamente
            base_url = urlparse(url).scheme + "://" + urlparse(url).netloc
            domain = urlparse(url).netloc

            for link in soup.find_all('a', href=True):
                href = link['href'].strip()

                # Verificar se o link começa com '/' ou é uma URL relativa
                if href.startswith('/') or base_url in href:
                    # Construir a URL completa se for relativa
                    if href.startswith('/'):
                        directory_url = urljoin(base_url, href)
                    else:
                        directory_url = href

                    # Adicionar somente se for uma URL válida e dentro do domínio
                    if urlparse(directory_url).scheme in ['http', 'https'] and domain in urlparse(directory_url).netloc:
                        directories.add(directory_url)

        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}Erro ao acessar {url}: {e}{Style.RESET_ALL}")

        return directories

    def extract_all_links(url):
        links = set()
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extrair a URL base para lidar com links relativos corretamente
            base_url = urlparse(url).scheme + "://" + urlparse(url).netloc
            domain = urlparse(url).netloc

            for link in soup.find_all('a', href=True):
                href = link['href'].strip()

                # Construir a URL completa se for relativa
                if href.startswith('/'):
                    full_url = urljoin(base_url, href)
                else:
                    full_url = href

                # Adicionar somente se for uma URL válida e dentro do domínio
                if urlparse(full_url).scheme in ['http', 'https'] and domain in urlparse(full_url).netloc:
                    links.add(full_url)

        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}Erro ao acessar {url}: {e}{Style.RESET_ALL}")

        return links

    def extract_parameter_links(url):
        parameter_links = set()
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extrair a URL base para lidar com links relativos corretamente
            base_url = urlparse(url).scheme + "://" + urlparse(url).netloc
            domain = urlparse(url).netloc

            for link in soup.find_all('a', href=True):
                href = link['href'].strip()

                # Verificar se o link contém parâmetros
                if '?' in href or '.php' in href:
                    full_url = urljoin(base_url, href)

                    # Adicionar somente se for uma URL válida e dentro do domínio
                    if urlparse(full_url).scheme in ['http', 'https'] and domain in urlparse(full_url).netloc:
                        parameter_links.add(full_url)

        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}Erro ao acessar {url}: {e}{Style.RESET_ALL}")

        return parameter_links

    def get_valid_url(host):
        urls = [f"http://{host}", f"http://www.{host}"]
        for url in urls:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    return url
            except requests.exceptions.RequestException:
                continue
        return None

    print("\n\n\n--------- E-Link | Extrator de Links e Diretórios\n\n\n")
    host = input("\n[\033[93m#\033[0m] Host >> ")
    url = get_valid_url(host)

    if not url:
        print(f"{Fore.RED}Não foi possível acessar o site com ou sem 'www'.{Style.RESET_ALL}")
        return

    while True:
        print("\nModo de extração:")
        print(f"{Fore.YELLOW}\n1 - 'Todos os diretórios'")
        print(f"{Fore.YELLOW}2 - 'Todos os links'")
        print(f"{Fore.YELLOW}3 - 'Links com parâmetros (?ref=pf, .php?=)'")
        print(f"{Fore.RED}0 - 'Sair'{Style.RESET_ALL}")

        mode = input(f"\nEscolha o modo >> ")

        if mode == '1':
            directories = extract_directories(url)
            if directories:
                print("\n\nDiretórios encontrados:")
                for directory in directories:
                    print(f"{Fore.GREEN}{directory}{Style.RESET_ALL}")
                print("\nTotal de diretórios encontrados:", len(directories))
            else:
                print(f"{Fore.RED}\nNenhum diretório encontrado ou problema ao acessar o site.{Style.RESET_ALL}")

        elif mode == '2':
            links = extract_all_links(url)
            if links:
                print("\n\nTodos os links encontrados:")
                for link in links:
                    print(f"{Fore.GREEN}{link}{Style.RESET_ALL}")
                print("\nTotal de links encontrados:", len(links))
            else:
                print(f"{Fore.RED}\nNenhum link encontrado ou problema ao acessar o site.{Style.RESET_ALL}")

        elif mode == '3':
            parameter_links = extract_parameter_links(url)
            if parameter_links:
                print("\n\nLinks com parâmetros encontrados:")
                for link in parameter_links:
                    print(f"{Fore.GREEN}{link}{Style.RESET_ALL}")
                print("\nTotal de links com parâmetros encontrados:", len(parameter_links))
            else:
                print(f"{Fore.RED}\nNenhum link com parâmetros encontrado ou problema ao acessar o site.{Style.RESET_ALL}")

        elif mode == '0':
            print(f"\n{Fore.RED}Encerrando o programa.{Style.RESET_ALL}")
            break

        else:
            print(f"{Fore.RED}\nOpção inválida. Escolha novamente.{Style.RESET_ALL}")


########################################       SITEPING        #####################################


def siteping():
    # Inicializa o colorama
    init(autoreset=True)

    # Caminho absoluto do arquivo de entrada
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(current_dir, 'sites.txt')

    # Dicionário de status HTTP
    http_statuses = {
        100: "Continue",
        101: "Switching Protocols",
        200: "OK",
        201: "Created",
        202: "Accepted",
        203: "Non-Authoritative Information",
        204: "No Content",
        205: "Reset Content",
        206: "Partial Content",
        300: "Multiple Choices",
        301: "Moved Permanently",
        302: "Found",
        303: "See Other",
        304: "Not Modified",
        305: "Use Proxy",
        307: "Temporary Redirect",
        308: "Permanent Redirect",
        400: "Bad Request",
        401: "Unauthorized",
        402: "Payment Required",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        406: "Not Acceptable",
        407: "Proxy Authentication Required",
        408: "Request Timeout",
        409: "Conflict",
        410: "Gone",
        411: "Length Required",
        412: "Precondition Failed",
        413: "Payload Too Large",
        414: "URI Too Long",
        415: "Unsupported Media Type",
        416: "Range Not Satisfiable",
        417: "Expectation Failed",
        500: "Internal Server Error",
        501: "Not Implemented",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout",
        505: "HTTP Version Not Supported"
    }

    # Função para verificar se o site está online usando http.client
    def check_site(url):
        def get_response(url, use_https=True):
            try:
                conn = HTTPSConnection(url, timeout=5) if use_https else HTTPConnection(url, timeout=5)
                conn.request("HEAD", "/")
                return conn.getresponse()
            except Exception:
                return None

        response = get_response(url)
        if not response:
            response = get_response(url, use_https=False)
        
        if response:
            if response.status == 200:
                return response.status, http_statuses.get(response.status, "Unknown Status")
            elif 300 <= response.status < 400:
                return response.status, http_statuses.get(response.status, "Unknown Status")  # Handle other redirects as well
            else:
                return response.status, http_statuses.get(response.status, "Unknown Status")
        else:
            return None, "Sem resposta"

    # Lista para armazenar os sites online
    online_sites = []

    print("   _____   _   _            _____    _                 ")
    print("  / ____| (_) | |          |  __ \  (_)                ")
    print(" | (___    _  | |_    ___  | |__) |  _   _ __     __ _ ")
    print("  \___ \  | | | __|  / _ \ |  ___/  | | | '_ \   / _` |")
    print("  ____) | | | | |_  |  __/ | |      | | | | | | | (_| |")
    print(" |_____/  |_|  \__|  \___| |_|      |_| |_| |_|  \__, |")
    print("                                                  __/ |")
    print("    Desenvolvido Por @WandrewTischler   v1.0     |___/ \n")

    # Ler o arquivo de entrada
    try:
        with open(input_file, 'r') as file:
            sites = file.readlines()
    except FileNotFoundError:
        print(Fore.RED + "Arquivo 'sites.txt' não encontrado.")
        return

    # Verificar cada site
    for site in sites:
        site = site.strip()
        status, status_message = check_site(site)
        if status == 200:
            print(Fore.GREEN + f"{site} está online ({status} {status_message})")
            online_sites.append(f"{site} ({status} {status_message})")
        elif status:
            if status == 301:
                print(Fore.YELLOW + f"{site} ({status} {status_message})")  # Colorir em amarelo para 301 Moved Permanently
            elif status == 302:
                print(Fore.YELLOW + f"{site} ({status} {status_message})")  # Manter amarelo para 302 Found
            elif status == 500:
                print(Fore.YELLOW + f"{site} ({status} {status_message})")
            else:
                print(Fore.RED + f"{site} ({status} {status_message})")
        else:
            print(Fore.LIGHTBLACK_EX + f"{site} não está online ({status_message})")  # Colorir em cinza para Sem resposta

    # Imprimir sites com status 200 OK no final
    print(Fore.BLUE + "\nSites online (200 OK):")
    for site in online_sites:
        print(site)

    # Imprimir contagem total de sites online
    print(Fore.BLUE + f"\nTotal de sites online (200 OK): {len(online_sites)}")


########################################        LuckFaha        ####################################

def luckfaha():
    print(f"\n\n{Fore.YELLOW}                                           _L/L")
    print(f"                                         _LT/l_L_")
    print(f"                          {Fore.GREEN}LuckFaha{Style.RESET_ALL}{Fore.YELLOW}     _LLl/L_T_lL_")
    print(f"                   _T/L   {Fore.GREEN}Suite 1.0{Style.RESET_ALL}{Fore.YELLOW}  _LT|L/_|__L_|_L_")
    print(f"                 _Ll/l_L_          _TL|_T/_L_|__T__|_l_")
    print(f"               _TLl/T_l|_L_      _LL|_Tl/_|__l___L__L_|L_")
    print(f"             _LT_L/L_|_L_l_L_  _'|_|_|T/_L_l__T _ l__|__|L_")
    print(f"           _Tl_L|/_|__|_|__T _LlT_|_Ll/_l_ _|__[ ]__|__|_l_L_")
    print(f"    ______LT_l_l/|__|__l_T _T_L|_|_|l/___|__ | _l__|_ |__|_T_L_____{Style.RESET_ALL}")

    # Inicializa o colorama
    init()

    # Cria um lock para sincronizar as impressões
    print_lock = threading.Lock()

    # Faixas de IPs públicos conhecidos
    faixas_ip_publicos = [
        (1, 126, 0, 0, 0, 255),   # Classe A: 1.0.0.0 - 126.255.255.255
        (128, 191, 0, 0, 0, 255), # Classe B: 128.0.0.0 - 191.255.255.255
        (192, 223, 0, 0, 0, 255), # Classe C: 192.0.0.0 - 223.255.255.255
    ]

    def gerar_ip_aleatorio():
        """Gera um endereço IP aleatório dentro de faixas de IPs públicos conhecidos."""
        faixa = random.choice(faixas_ip_publicos)
        return f"{random.randint(faixa[0], faixa[1])}.{random.randint(faixa[2], faixa[3])}.{random.randint(faixa[4], faixa[5])}.{random.randint(0, 255)}"

    def testar_porta(ip, porta):
        """Testa se a porta está aberta no IP fornecido."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                s.connect((ip, porta))
                return True
        except (socket.timeout, socket.error):
            return False

    def obter_banner(ip, porta):
        """Obtém o banner de um serviço na porta fornecida."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                s.connect((ip, porta))
                s.send(b'HEAD / HTTP/1.0\r\n\r\n')  # Envia uma requisição HTTP simples
                banner = s.recv(4096).decode()  # Recebe e decodifica o banner
                return banner
        except (socket.timeout, socket.error):
            return None

    def verificar_servico(ip, porta, servico, versao=None):
        """Verifica se um serviço específico está rodando na porta fornecida, com ou sem versão."""
        banner = obter_banner(ip, porta)
        if banner:
            banner_upper = banner.upper()
            servico_upper = servico.upper()

            # Verifica se o serviço está presente no banner com uma correspondência parcial
            if servico_upper in banner_upper:
                if versao:
                    versao_upper = versao.upper()
                    # Verifica se a versão fornecida está presente no banner
                    if versao_upper in banner_upper:
                        return True, banner
                else:
                    return True, banner
        return False, banner

    def obter_localizacao(ip):
        """Obtém a localização (código ISO do país) do IP fornecido usando a API ipinfo.io."""
        url = f"http://ipinfo.io/{ip}/json"
        try:
            response = requests.get(url)
            data = response.json()
            if 'country' in data:
                return data['country']
            else:
                return "Desconhecido"
        except requests.RequestException:
            return "Desconhecido"

    def codigo_para_nome_pais(codigo_iso):
        """Converte o código ISO do país para o nome completo do país."""
        try:
            pais = pycountry.countries.get(alpha_2=codigo_iso)
            return pais.name if pais else "Desconhecido"
        except LookupError:
            return "Desconhecido"

    def tarefa_por_porta(ip, porta, resultados):
        """Executa a tarefa de testar portas e coleta informações do banner."""
        if testar_porta(ip, porta):
            with print_lock:
                print(f"{Fore.GREEN}Porta {porta} está aberta em {ip}{Style.RESET_ALL}")
                resultados.append(ip)  # Apenas o IP é adicionado à lista de resultados
        else:
            with print_lock:
                print(f"{Fore.RED}Porta {porta} NÃO está aberta em {ip}{Style.RESET_ALL}")

    def tarefa_por_servico(ip, porta, servico, versao, resultados):
        """Executa a tarefa de testar serviços e coleta informações do banner."""
        if testar_porta(ip, porta):
            banner = obter_banner(ip, porta)
            encontrado, banner = verificar_servico(ip, porta, servico, versao)

            with print_lock:
                if encontrado:
                    print(f"{Fore.GREEN}Porta {porta} está aberta em {ip}, localizado em {obter_localizacao(ip)}.{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}Banner: {banner}{Style.RESET_ALL}")
                    resultados.append((ip, banner))
                else:
                    print(f"{Fore.RED}Porta {porta} está aberta em {ip}, mas o serviço {servico} com versão {versao} NÃO está rodando.{Style.RESET_ALL}")
                    if banner:
                        print(f"{Fore.YELLOW}Banner: {banner}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.YELLOW}Banner não obtido.{Style.RESET_ALL}")
        else:
            with print_lock:
                print(f"{Fore.RED}Porta {porta} NÃO está aberta em {ip}{Style.RESET_ALL}")

    def tarefa_por_servico_e_pais(ip, porta, servico, versao, pais, resultados):
        """Executa a tarefa de testar serviços e filtra por país."""
        if testar_porta(ip, porta):
            codigo_pais = obter_localizacao(ip)
            nome_pais = codigo_para_nome_pais(codigo_pais)
            nome_pais_upper = nome_pais.upper()
            pais_upper = pais.upper()

            with print_lock:
                print(f"{Fore.GREEN}\nPorta {porta} está aberta em {ip}, localizado em {nome_pais}.{Style.RESET_ALL}\n")

            # Verifica se o país no IP corresponde ao país solicitado
            if nome_pais_upper == pais_upper or pais_upper == "BR":
                encontrado, banner = verificar_servico(ip, porta, servico, versao)
                if encontrado:
                    with print_lock:
                        print(f"{Fore.BLUE}O serviço {servico} com versão {versao} está rodando na porta {porta} em {ip}, localizado em {nome_pais}.{Style.RESET_ALL}")
                        print(f"{Fore.GREEN}Banner: {banner}{Style.RESET_ALL}")
                    resultados.append((ip, banner))
                else:
                    with print_lock:
                        print(f"{Fore.RED}O serviço {servico} com versão {versao} NÃO está rodando na porta {porta} em {ip}.{Style.RESET_ALL}")
                        if banner:
                            print(f"{Fore.YELLOW}Banner: {banner}{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.YELLOW}Banner não obtido.{Style.RESET_ALL}")
            else:
                with print_lock:
                    print(f"{Fore.YELLOW}IP {ip} está localizado em {nome_pais}, não corresponde ao país solicitado.{Style.RESET_ALL}")
        else:
            with print_lock:
                print(f"{Fore.RED}Porta {porta} NÃO está aberta em {ip}{Style.RESET_ALL}")

    def imprimir_resultados(resultados):
        """Imprime todos os resultados coletados no final dos testes."""
        print("\nResumo dos resultados:")
        for ip in resultados:
            print(f"{Fore.GREEN}IP: {ip}{Style.RESET_ALL}")

    print("\n\nEscolha uma opção:")
    print("\n1 - Buscar apenas portas abertas")
    print("2 - Buscar por serviços específicos")
    print("3 - Buscar por serviços e filtrar por país")

    opcao = input("\nDigite o número da opção: ")

    if opcao == "1":
        porta = int(input("Digite o número da porta: "))
        numero_de_ips = int(input("Digite o número de IPs: "))
        print("\n")

        resultados = []

        start_time = time.time()  # Início do tempo

        def buscar_por_porta():
            while len(resultados) < numero_de_ips:
                ip = gerar_ip_aleatorio()
                tarefa_por_porta(ip, porta, resultados)

        threads = []
        for _ in range(10):
            thread = threading.Thread(target=buscar_por_porta)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        end_time = time.time()  # Fim do tempo
        tempo_total = end_time - start_time
        print(f"\nTempo total: {tempo_total:.2f} segundos")

        # Imprime o resumo dos resultados
        imprimir_resultados(resultados)

    elif opcao == "2":
        servico = input("Digite o serviço a ser verificado (por exemplo, 'apache'): ")
        versao = input("Versão (opcional, pressione Enter para pular): ")
        porta = int(input("Digite o número da porta: "))
        numero_de_ips = int(input("Digite o número de IPs: "))
        print("\n")

        resultados = []

        start_time = time.time()  # Início do tempo

        def buscar_por_servico():
            while len(resultados) < numero_de_ips:
                ip = gerar_ip_aleatorio()
                tarefa_por_servico(ip, porta, servico, versao, resultados)

        threads = []
        for _ in range(10):
            thread = threading.Thread(target=buscar_por_servico)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        end_time = time.time()  # Fim do tempo
        tempo_total = end_time - start_time
        print(f"\nTempo total: {tempo_total:.2f} segundos")

        # Imprime o resumo dos resultados
        imprimir_resultados(resultados)

    elif opcao == "3":
        servico = input("Digite o serviço a ser verificado (por exemplo, 'apache'): ")
        versao = input("Versão (opcional, pressione Enter para pular): ")
        porta = int(input("Digite o número da porta: "))
        numero_de_ips = int(input("Digite o número de IPs: "))
        pais = input("País (nome completo ou código ISO, exemplo: Brazil ou BR): ")
        print("\n")

        resultados = []

        start_time = time.time()  # Início do tempo

        def buscar_por_servico_e_pais():
            while len(resultados) < numero_de_ips:
                ip = gerar_ip_aleatorio()
                tarefa_por_servico_e_pais(ip, porta, servico, versao, pais, resultados)

        threads = []
        for _ in range(10):
            thread = threading.Thread(target=buscar_por_servico_e_pais)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        end_time = time.time()  # Fim do tempo
        tempo_total = end_time - start_time
        print(f"\nTempo total: {tempo_total:.2f} segundos")

        # Imprime o resumo dos resultados
        imprimir_resultados(resultados)

    else:
        print("Opção inválida.")





########################################        Sendys        ######################################

def sendys():
    # Códigos ANSI para cores
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'
    
    print(f"{Fore.GREEN}\n███████╗███████╗███╗   ██╗██████╗ ██╗   ██╗███████╗{Fore.RESET}")
    print(f"{Fore.GREEN}██╔════╝██╔════╝████╗  ██║██╔══██╗╚██╗ ██╔╝██╔════╝{Fore.RESET}")
    print(f"{Fore.GREEN}███████╗█████╗  ██╔██╗ ██║██║  ██║ ╚████╔╝ ███████╗{Fore.RESET}")
    print(f"{Fore.GREEN}╚════██║██╔══╝  ██║╚██╗██║██║  ██║  ╚██╔╝  ╚════██║{Fore.RESET}")
    print(f"{Fore.GREEN}███████║███████╗██║ ╚████║██████╔╝   ██║   ███████║{Fore.RESET}")
    print(f"{Fore.GREEN}╚══════╝╚══════╝╚═╝  ╚═══╝╚═════╝    ╚═╝   ╚══════╝{Fore.RESET}")
    print(f"{Fore.YELLOW}Desenvolvido Por @WandrewTischler            {Fore.BLUE}v1.0{Fore.RESET}")

    target = input("\nDigite o IP ou o site (com ou sem http/https): ")

    if not target.startswith("http"):
        target = "http://" + target

    try:
        # Realizar várias requisições HTTP para detectar WAFs
        responses = [
            requests.get(target),
            requests.post(target, data={'test': 'test'}),
            requests.head(target)
        ]
        
        print(f"{GREEN}Conexão bem-sucedida com {target}{RESET}")

        for response in responses:
            headers = response.headers

            print("\nCabeçalhos:")
            for key, value in headers.items():
                print(f"{key}: {GREEN}{value}{RESET}")

    except requests.exceptions.RequestException as e:
        print(f"{RED}Erro ao conectar-se ao alvo: {e}{RESET}")







########################################        DeviceInfo        ######################################

def deviceinfo():
    YELLOW = '\033[93m'
    RESET = '\033[0m'

    print(YELLOW + "\n  _____             _          _____        __      ")
    print(" |  __ \\           (_)        |_   _|      / _|     ")
    print(" | |  | | _____   ___  ___ ___  | |  _ __ | |_ ___  ")
    print(" | |  | |/ _ \\ \\ / / |/ __/ _ \\ | | | '_ \\|  _/ _ \\ ")
    print(" | |__| |  __/\\ V /| | (_|  __/_| |_| | | | || (_) |")
    print(" |_____/ \\___| \\_/ |_|\\___\\___|_____|_| |_|_| \\___/ " + RESET)
    print(f"\n{Fore.YELLOW}   Desenvolvido Por @WandrewTischler     {Fore.BLUE}v1.0{Fore.RESET}")

    # Cores ANSI para formatação
    GREEN = '\033[92m'
    RESET = '\033[0m'

    # URL da API para geolocalização
    IPAPI_URL = "http://ip-api.com/json/"

    def get_size(bytes, suffix="B"):
        """
        Converte bytes em formato legível (KB, MB, GB, etc.).
        """
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor
        return f"{bytes:.2f}Y{suffix}"

    def get_ip_info():
        """
        Obtém informações de geolocalização com base no IP usando ip-api.
        """
        try:
            response = requests.get(IPAPI_URL)
            response.raise_for_status()  # Verifica se houve um erro HTTP
            data = response.json()
            
            ip_info = {
                'Endereço IP': data.get('query', 'Não disponível'),
                'País': data.get('country', 'Não disponível'),
                'Estado': data.get('regionName', 'Não disponível'),
                'Cidade': data.get('city', 'Não disponível'),
                'Provedor de Internet': data.get('isp', 'Não disponível'),
                'Coordenadas': f"{data.get('lat', 'Não disponível')}, {data.get('lon', 'Não disponível')}"
            }
            
            return ip_info
        except requests.RequestException as e:
            print("Erro ao fazer a solicitação para a API:", e)
            return {
                'Endereço IP': 'Não disponível',
                'País': 'Não disponível',
                'Estado': 'Não disponível',
                'Cidade': 'Não disponível',
                'Provedor de Internet': 'Não disponível',
                'Coordenadas': 'Não disponível'
            }

    def get_cooler_rpm():
        """
        Obtém a rotação do cooler, se disponível.
        """
        try:
            # Tenta acessar sensores do sistema
            sensors = psutil.sensors_fans()
            if sensors:
                for fan_name, fan_info in sensors.items():
                    if fan_info:
                        return f"{fan_info[0].current} RPM"  # Retorna a rotação do primeiro cooler
            return "Não disponível"
        except Exception as e:
            return "Não disponível"

    def get_device_info():
        device_info = {}

        # Informações básicas do sistema
        device_info['\n\nNome do Dispositivo'] = platform.node()
        device_info['Sistema Operacional'] = platform.system()
        device_info['Versão do SO'] = platform.version()
        device_info['Arquitetura do SO'] = f"{platform.architecture()[0]} ({platform.architecture()[1]})"
        
        # Informações sobre o usuário
        device_info['Usuário'] = os.getlogin()

        # Informações sobre o hardware
        device_info['Processador'] = platform.processor()
        device_info['Número de Núcleos'] = psutil.cpu_count(logical=True)
        device_info['Frequência do CPU'] = f"{psutil.cpu_freq().current} MHz"
        device_info['Memória RAM Total'] = f"{psutil.virtual_memory().total / (1024**3):.2f} GB"

        # Informações sobre a bateria
        battery = psutil.sensors_battery()
        if battery:
            device_info['Status da Bateria'] = f"{battery.percent}%"
            device_info['Carregando'] = 'Sim' if battery.power_plugged else 'Não'
            if battery.secsleft == psutil.POWER_TIME_UNLIMITED:
                device_info['Tempo Restante'] = 'Carregando'
            elif battery.secsleft == psutil.POWER_TIME_UNKNOWN:
                device_info['Tempo Restante'] = 'Desconhecido'
            else:
                device_info['Tempo Restante'] = f"{battery.secsleft // 60} minutos"
        else:
            device_info['Status da Bateria'] = 'Não disponível'
            device_info['Carregando'] = 'Não aplicável'
            device_info['Tempo Restante'] = 'Não aplicável'

        # Informações sobre os discos
        partitions = psutil.disk_partitions()
        disk_info = []
        for partition in partitions:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info.append(f"{partition.device}: {get_size(usage.total)} (Usado: {get_size(usage.used)}, Livre: {get_size(usage.free)}, Sistema de Arquivos: {partition.fstype})")
        
        device_info['Discos'] = ', '.join(disk_info)
        
        # Informações de rede
        interfaces = psutil.net_if_addrs()
        network_info = []
        for iface, addrs in interfaces.items():
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    network_info.append(f"{iface}: {addr.address} (Máscara: {addr.netmask})")
        
        device_info['Interfaces de Rede'] = ', '.join(network_info) if network_info else 'Não disponível'

        # Data e hora local
        now = datetime.now()
        device_info['Data e Hora Local'] = now.strftime("%Y-%m-%d %H:%M:%S")

        # Informações sobre o cooler
        device_info['RPM do Cooler'] = get_cooler_rpm()

        return device_info

    def print_device_info():
        info = get_device_info()
        ip_info = get_ip_info()

        for key, value in info.items():
            print(f"{key}: {GREEN}{value}{RESET}")

        print("\nInformações de Geolocalização:")
        for key, value in ip_info.items():
            print(f"{key}: {GREEN}{value}{RESET}")

        # Adiciona o link do Google Maps se as coordenadas estiverem disponíveis
        coordinates = ip_info.get('Coordenadas', 'Não disponível')
        if coordinates and coordinates != 'Não disponível':
            lat, lon = coordinates.split(', ')
            print(f"\nLink do Google Maps: {GREEN}https://www.google.com/maps?q={lat},{lon}{RESET}")

    print_device_info()







###############################################################################################################################################
###############################################################################################################################################



nomep = "\033[36m" + "DRICK FRAMEWORK" "\033[0;0m"



print("\n\n\n      ▄▄▄▄▄▄▄▄▄▄   ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄ ")
print("     ▐░░░░░░░░░░▌ ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌  ▐░▌")
print("     ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌ ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░▌ ▐░▌") 
print("     ▐░▌       ▐░▌▐░▌       ▐░▌     ▐░▌     ▐░▌          ▐░▌▐░▌")  
print("     ▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄█░▌     ▐░▌     ▐░▌          ▐░▌░▌")   
print("     ▐░▌       ▐░▌▐░░░░░░░░░░░▌     ▐░▌     ▐░▌          ▐░░▌")    
print("     ▐░▌       ▐░▌▐░█▀▀▀▀█░█▀▀      ▐░▌     ▐░▌          ▐░▌░▌")  
print("     ▐░▌       ▐░▌▐░▌     ▐░▌       ▐░▌     ▐░▌          ▐░▌▐░▌")  
print("     ▐░█▄▄▄▄▄▄▄█░▌▐░▌      ▐░▌  ▄▄▄▄█░█▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ ▐░▌ ▐░▌") 
print("      ░░░░░░░░░░▌ ▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌  ▐░▌")
print("      ▀▀▀▀▀▀▀▀▀▀   ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀    ▀ ")
                                                            

print("\n\n###########  ########  ##### ### ######  ########  ######## # ##  #####")
print ("####### ###### ##### --|", nomep, "|-- #########\033[36m v[1.0] \033[0;0m#########")
print("######## ###  ####### ############ ######## # ## #####  # # #  #### ### \n\n")


def get_random_line_from_github(url):
    response = requests.get(url)

    if response.status_code == 200:
        content = response.text
        
        lines = content.split('\n')
        
        random_line = random.choice(lines)
        
        return random_line
    else:
        return "Error fetching the file."


url = "https://raw.githubusercontent.com/secbras/drick-framework/main/frases.txt"
fraserandom = get_random_line_from_github(url)

style = "\033[31m" + " [+]" + "\033[0;0m"

print(style, fraserandom)

	
	
strr = "\033[33m" + "[+]" + "\033[0;0m"

print("\n\n")
print(" ", strr ,"Use (/c) para listar os comandos.")
print(" ", strr, "Use (/info) para mais informações.\n\n\n")



################################################################################################################################################



x = True

while x == True:
	
	y = input("\n[\033[32m#\033[0;0m] >> ")
	
	# Comando para fechar o programa
	if y == "/sair":		
		x = False
		
	elif y == "/c":
		print("\n\n\nPARA USAR UMA FERRAMENTA UTILIZE O COMANDO ENTRE PARENTESES.\n \n\n[#] COMANDOS USUAIS:\n\nPing Host                               (\033[32mping\033[0;0m)\nCapturar IP                             (\033[32mcapip\033[0;0m)\nTestar porta                            (\033[32mtporta\033[0;0m)\nCapturar banner                         (\033[32mcbanner\033[0;0m)\nLocalizar IP                            (\033[32mlocip\033[0;0m)\nExtrator de Links                       (\033[32melink\033[0;0m)\nEscaner de Portas                       (\033[32mpscan\033[0;0m)\nTestador de Links                       (\033[32msiteping\033[0;0m)\nBuscador de Serviços                    (\033[32manunn4ki\033[0;0m)\nAnálise de Cabeçalho                    (\033[32msendys\033[0;0m)\nSobre este Dispositivo                  (\033[32mdeviceinfo\033[0;0m)")


				
	elif y == "/info":
		print("\n\n                      \033[32mDRICK FRAMEWORK\033[0;0m")
		print("\n O software (Drick Framework) é um pacote com vários algoritimos essênciais para um bom pentesting e uma boa análise de um sistema ou rede, o nosso software busca sempre agrupar as melhores alternativas para uma boa análise e uma rede de testes.\n")
		print("\n\n                    \033[32mCOMANDOS ADICIONAIS\033[0;0m")
		print("\n1 - Caso queira consultar alguma informação a respeito de algum programa da plataforma use o comando (/info) + Programa, por exemplo (/info ping), este comando retornará as principais informações sobre o mesmo.\n\n2 - Caso deseje fechar a framework utilize o comando (/sair)\n\n3 - Utilize os comandos (/limpar),(/clear) ou (/cls) para limpar a tela.")
		
		
		
	##########################         requisitar informações de determinadas funções             ############################################
	
	elif y == "/info ping":
		print("\n\033[32m PING\n\033[0;0m\nPING é um algorítimo usado para testar uma máquina remota a fim de determinar se ela está online ou offline e obter dados de sua requisição como tempo de resposta.")
	
	elif y == "/info capip":
		print("\n\033[32m CAPIP (CAPTURAR IP)\n\033[0;0m\nCAPIP tem como função obter o endereço remoto de uma determinada máquina na rede, o algorítimo captura o IP (Internet Protocol) através de uma requisição.")
	
	elif y == "/info tporta":
		print("\n\033[32m TPORTA (TESTAR PORTA)\n\033[0;0m\nTPORTA é um testador de porta específica nativo da plataforma, basicamente ele testa se uma determinada porta de um dispositivo na rede está aberta ou fechada.")
	
	elif y == "/info localizar ip":
		print("\n\033[32m LOCIP\n\033[0;0m\nEsta função lhe permite rastrear um dispositivo e obter características de sua localização.")
	
	elif y == "/info cbanner":
			print("\n\033[32m CBANNER (CAPTURAR BANNER)\n\033[0;0m\nA partir de requisições ao alvo, é possível obter o serviço e sua versão que está a rodar em uma determinada porta. Com esta informação, é possível buscar um exploit.")
	
	elif y == "/info elink":
		print("\n\033[32m ELINK (Extraidor de Link)\n\033[0;0m\nEsse algoritmo tem como função extrair links de uma determinada página na web.")
	
	elif y == "/info pscan":
		print("\n\033[32m PSCAN (Scanner de Portas)\n\033[0;0m\nPSCAN é um scanner de portas simples que tem o intuito de testar as principais portas de um host e determinar se as mesmas estão abertas ou fechadas.")
          
	elif y == "/info siteping":
		print("\n\033[32m SITEPING\n\033[0;0m\nSITEPING é uma ferramenta que permite verificar o status de vários sites em massa, basta adicionar os sites em formato de lista no arquivo sites.txt no diretório do Drick Framework")


		
################################################################################################################################################



	# Teste ON/OFF Host
	elif y == "ping":
		ping()
	
	# Capturar IP
	elif y == "capip":
		capip()
          
	# Testar porta
	elif y == "tporta":
		tporta()
          
	# Capturar banner
	elif y == "cbanner":
		cbanner()
	
	# Localizar IP
	elif y == "locip":
		geoip()

	# Scanner de portas
	elif y == "pscan":
		pscan()

	# Extrator de links
	elif y == "elink":
		elink()

	# Scanner de portas
	elif y == "siteping":
		siteping()
          
	# Anunn4ki Project
	elif y == "luckfaha":
		luckfaha()
          
	# Sendys Project
	elif y == "sendys":
		sendys()

	# DeviceInfo Project
	elif y == "deviceinfo":
		deviceinfo()




	
	########### Limpar o console ###########

	elif y == "/limpar":
		a = "           " * 10000
		print(a)

	elif y == "/clear":
		a = "           " * 10000
		print(a)


	elif y == "/cls":
		a = "           " * 10000
		print(a)
	

		
		
	# Trata as exceções
	else:
          print("\nESSE COMANDO NÃO EXISTE.")
		









"""
...e viveram felizes para sempre, fim.

"""
