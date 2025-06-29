import os
import platform
import psutil
import socket
import requests
from datetime import datetime
from colorama import Fore, Style
import traceback
import sys

def deviceinfo():
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'

    try:
        print(YELLOW + "\n  _____             _          _____        __      ")
        print(" |  __ \\           (_)        |_   _|      / _|     ")
        print(" | |  | | _____   ___  ___ ___  | |  _ __ | |_ ___  ")
        print(" | |  | |/ _ \\ \\ / / |/ __/ _ \\ | | | '_ \\|  _/ _ \\ ")
        print(" | |__| |  __/\\ V /| | (_|  __/_| |_| | | | || (_) |")
        print(" |_____/ \\___| \\_/ |_|\\___\\___|_____|_| |_|_| \\___/ " + RESET)
    except Exception as e:
        print(f"{RED}Erro ao exibir o banner: {e}{RESET}")

    IPAPI_URL = "http://ip-api.com/json/"
    TIMEOUT = 10  # segundos para timeout das requisições

    def get_size(bytes, suffix="B"):
        try:
            factor = 1024
            for unit in ["", "K", "M", "G", "T", "P"]:
                if bytes < factor:
                    return f"{bytes:.2f}{unit}{suffix}"
                bytes /= factor
            return f"{bytes:.2f}Y{suffix}"
        except Exception as e:
            print(f"{RED}Erro ao formatar tamanho: {e}{RESET}")
            return "Erro"

    def get_ip_info():
        try:
            response = requests.get(IPAPI_URL, timeout=TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 'fail':
                error_message = data.get('message', 'Erro desconhecido na API')
                print(f"{RED}API retornou erro: {error_message}{RESET}")
                return {
                    'Endereço IP': 'Erro na API',
                    'País': 'Erro na API',
                    'Estado': 'Erro na API',
                    'Cidade': 'Erro na API',
                    'Provedor de Internet': 'Erro na API',
                    'Coordenadas': 'Erro na API'
                }
                
            ip_info = {
                'Endereço IP': data.get('query', 'Não disponível'),
                'País': data.get('country', 'Não disponível'),
                'Estado': data.get('regionName', 'Não disponível'),
                'Cidade': data.get('city', 'Não disponível'),
                'Provedor de Internet': data.get('isp', 'Não disponível'),
                'Coordenadas': f"{data.get('lat', 'Não disponível')}, {data.get('lon', 'Não disponível')}"
            }
            return ip_info
            
        except requests.exceptions.RequestException as e:
            error_type = type(e).__name__
            print(f"{RED}Erro ao obter informações de IP ({error_type}): {e}{RESET}")
            return {
                'Endereço IP': 'Erro de conexão',
                'País': 'Erro de conexão',
                'Estado': 'Erro de conexão',
                'Cidade': 'Erro de conexão',
                'Provedor de Internet': 'Erro de conexão',
                'Coordenadas': 'Erro de conexão'
            }
        except Exception as e:
            print(f"{RED}Erro inesperado ao obter informações de IP: {e}{RESET}")
            return {
                'Endereço IP': 'Erro inesperado',
                'País': 'Erro inesperado',
                'Estado': 'Erro inesperado',
                'Cidade': 'Erro inesperado',
                'Provedor de Internet': 'Erro inesperado',
                'Coordenadas': 'Erro inesperado'
            }

    def get_cooler_rpm():
        try:
            if not hasattr(psutil, 'sensors_fans'):
                return "Função não suportada"
                
            sensors = psutil.sensors_fans()
            if not sensors:
                return "Nenhum sensor encontrado"
                
            rpm_info = []
            for fan_name, fan_info in sensors.items():
                if fan_info:
                    for fan in fan_info:
                        rpm_info.append(f"{fan_name}: {fan.current} RPM")
            return ", ".join(rpm_info) if rpm_info else "Sem dados de RPM"
            
        except Exception as e:
            print(f"{RED}Erro ao obter RPM do cooler: {e}{RESET}")
            return "Erro"

    def safe_get(func, default="Não disponível", *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"{RED}Erro ao obter informação: {e}{RESET}")
            return default

    def get_device_info():
        device_info = {}
        
        try:
            # Informações básicas do sistema
            device_info['\n\nNome do Dispositivo'] = safe_get(platform.node)
            device_info['Sistema Operacional'] = safe_get(platform.system)
            device_info['Versão do SO'] = safe_get(platform.version)
            
            try:
                arch_info = f"{platform.architecture()[0]} ({platform.architecture()[1]})"
                device_info['Arquitetura do SO'] = arch_info
            except Exception as e:
                device_info['Arquitetura do SO'] = f"Erro: {e}"
            
            device_info['Usuário'] = safe_get(os.getlogin)
            
            # Informações da CPU
            device_info['Processador'] = safe_get(platform.processor)
            device_info['Número de Núcleos'] = safe_get(psutil.cpu_count, default="Erro", logical=True)
            
            try:
                cpu_freq = psutil.cpu_freq()
                device_info['Frequência do CPU'] = f"{cpu_freq.current} MHz" if cpu_freq else "Não disponível"
            except Exception as e:
                device_info['Frequência do CPU'] = f"Erro: {e}"
            
            # Informações de memória
            try:
                mem = psutil.virtual_memory()
                device_info['Memória RAM Total'] = f"{mem.total / (1024**3):.2f} GB"
            except Exception as e:
                device_info['Memória RAM Total'] = f"Erro: {e}"
            
            # Informações da bateria
            try:
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
            except Exception as e:
                device_info['Status da Bateria'] = f"Erro: {e}"
                device_info['Carregando'] = 'Erro'
                device_info['Tempo Restante'] = 'Erro'
            
            # Informações de disco
            try:
                partitions = psutil.disk_partitions()
                disk_info = []
                for partition in partitions:
                    try:
                        usage = psutil.disk_usage(partition.mountpoint)
                        disk_info.append(
                            f"{partition.device}: {get_size(usage.total)} "
                            f"(Usado: {get_size(usage.used)}, "
                            f"Livre: {get_size(usage.free)}, "
                            f"Sistema de Arquivos: {partition.fstype})"
                        )
                    except Exception as e:
                        disk_info.append(f"{partition.device}: Erro ao obter informações")
                device_info['Discos'] = '\n  '.join(disk_info) if disk_info else 'Nenhum disco encontrado'
            except Exception as e:
                device_info['Discos'] = f"Erro ao obter informações de disco: {e}"
            
            # Informações de rede
            try:
                interfaces = psutil.net_if_addrs()
                network_info = []
                for iface, addrs in interfaces.items():
                    for addr in addrs:
                        if addr.family == socket.AF_INET:
                            network_info.append(f"{iface}: {addr.address} (Máscara: {addr.netmask})")
                device_info['Interfaces de Rede'] = '\n  '.join(network_info) if network_info else 'Nenhuma interface encontrada'
            except Exception as e:
                device_info['Interfaces de Rede'] = f"Erro ao obter informações de rede: {e}"
            
            # Data e hora
            try:
                now = datetime.now()
                device_info['Data e Hora Local'] = now.strftime("%Y-%m-%d %H:%M:%S")
            except Exception as e:
                device_info['Data e Hora Local'] = f"Erro: {e}"
            
            # Informações do cooler
            device_info['RPM do Cooler'] = get_cooler_rpm()
            
            return device_info
            
        except Exception as e:
            print(f"{RED}Erro crítico ao obter informações do dispositivo: {e}{RESET}")
            return {'Erro': f"Falha crítica ao coletar informações: {e}"}

    def print_device_info():
        try:
            info = get_device_info()
            ip_info = get_ip_info()

            print(f"\n{GREEN}=== Informações do Dispositivo ==={RESET}")
            for key, value in info.items():
                if key.startswith('\n'):
                    print(f"{RESET}{key}: {GREEN}{value}{RESET}")
                else:
                    print(f"{RESET}{key}: {GREEN}{value}{RESET}")

            print(f"\n{GREEN}=== Informações de Geolocalização ==={RESET}")
            for key, value in ip_info.items():
                print(f"{RESET}{key}: {GREEN}{value}{RESET}")

            coordinates = ip_info.get('Coordenadas', 'Não disponível')
            if coordinates and coordinates != 'Não disponível' and coordinates != 'Erro' and ',' in coordinates:
                try:
                    lat, lon = coordinates.split(', ')
                    print(f"\n{RESET}Link do Google Maps: {GREEN}https://www.google.com/maps?q={lat},{lon}{RESET}")
                except Exception as e:
                    print(f"{RED}Erro ao processar coordenadas: {e}{RESET}")
                    
        except Exception as e:
            print(f"{RED}Erro ao imprimir informações: {e}{RESET}")
            print(f"{RED}Traceback:{RESET}")
            traceback.print_exc()

    try:
        print_device_info()
    except KeyboardInterrupt:
        print(f"\n{RED}Operação interrompida pelo usuário{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{RED}Erro fatal no programa principal: {e}{RESET}")
        print(f"{RED}Traceback:{RESET}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    deviceinfo()