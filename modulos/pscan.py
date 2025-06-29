import socket

def pscan():
    class bcolors:
        GREEN = '\033[92m'
        RED = '\033[91m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        CYAN = '\033[96m'
        END = '\033[0m'

    SERVICE_DB = {
        21: 'FTP',
        22: 'SSH',
        23: 'Telnet',
        25: 'SMTP',
        53: 'DNS',
        80: 'HTTP',
        110: 'POP3',
        115: 'SFTP',
        135: 'MS RPC',
        139: 'NetBIOS',
        143: 'IMAP',
        161: 'SNMP',
        194: 'IRC',
        443: 'HTTPS',
        445: 'SMB',
        993: 'IMAPS',
        995: 'POP3S',
        1723: 'PPTP',
        3306: 'MySQL',
        3389: 'RDP',
        5900: 'VNC',
        8080: 'HTTP Alt',
        8443: 'HTTPS Alt',
        6667: 'IRC',
        5432: 'PostgreSQL',
        5800: 'VNC HTTP',
        5901: 'VNC Alt',
        5902: 'VNC Alt 2',
        2222: 'SSH Alt',
        2000: 'Call of Duty'
    }

    def get_service_name(port):
        return SERVICE_DB.get(port, 'Serviço desconhecido')

    def resolve_host(host):
        try:
            return socket.gethostbyname(host)
        except socket.gaierror:
            return None

    print(f"\n{bcolors.YELLOW}[+] Port Scanner Avançado{bcolors.END}\n")

    while True:
        host = input(f"[{bcolors.YELLOW}#{bcolors.END}] Host (IP ou domínio) >> ")
        ip = resolve_host(host)
        if ip:
            print(f"{bcolors.BLUE}[*] Resolvido: {host} → {ip}{bcolors.END}")
            break
        print(f"{bcolors.RED}[!] Não foi possível resolver o host. Tente novamente.{bcolors.END}")

    while True:
        scan_mode = input("Escolha o modo de escaneamento (1 - Portas Comuns / 2 - Todas as Portas / 3 - Portas Personalizadas): ")
        if scan_mode in ['1', '2', '3']:
            break
        print(f"{bcolors.RED}[!] Opção inválida. Escolha 1, 2 ou 3.{bcolors.END}")

    if scan_mode == '1':
        ports = list(SERVICE_DB.keys())
    elif scan_mode == '2':
        ports = range(1, 65536)
    else:
        port_input = input("Digite as portas a serem verificadas (separadas por vírgula): ")
        ports = [int(p.strip()) for p in port_input.split(',') if p.strip().isdigit()]

    open_ports = []
    
    print(f"\n{bcolors.BLUE}[*] Iniciando escaneamento em {host} ({ip}){bcolors.END}\n")

    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(2)
                result = sock.connect_ex((ip, port))
                
                if result == 0:
                    service = get_service_name(port)
                    open_ports.append((port, service))
                    print(f"{bcolors.GREEN}[+] Porta {port} ({service}) está aberta{bcolors.END}")
                else:
                    if scan_mode == '1':
                        service = get_service_name(port)
                        print(f"{bcolors.RED}[-] Porta {port} ({service}) não está respondendo{bcolors.END}")
        except KeyboardInterrupt:
            print(f"\n{bcolors.YELLOW}[!] Escaneamento interrompido pelo usuário{bcolors.END}")
            return
        except Exception as e:
            print(f"{bcolors.RED}[!] Erro ao verificar porta {port}: {str(e)}{bcolors.END}")

    print(f"\n{bcolors.BLUE}[*] Escaneamento concluído{bcolors.END}\n")

    if open_ports:
        print(f"{bcolors.GREEN}[+] Portas abertas encontradas:{bcolors.END}")
        print(f"{bcolors.CYAN}{'-'*60}{bcolors.END}")
        print(f"{bcolors.YELLOW}| {'Porta':<8} | {'Serviço':<20} |{bcolors.END}")
        print(f"{bcolors.CYAN}{'-'*60}{bcolors.END}")
        
        for port, service in open_ports:
            print(f"| {port:<8} | {service:<20} |")
        
        print(f"{bcolors.CYAN}{'-'*60}{bcolors.END}\n")
    else:
        print(f"{bcolors.RED}[-] Nenhuma porta aberta encontrada{bcolors.END}")

if __name__ == "__main__":
    pscan()