import requests
from colorama import Fore, Style


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

    target = input("\nDigite o IP ou o site (com ou sem http/https): ").strip()

    if not target:
        print(f"{RED}Erro: Nenhum alvo foi especificado.{RESET}")
        return

    if not target.startswith(("http://", "https://")):
        target = "http://" + target

    try:
        # Verificar primeiro se o site está acessível
        test_response = requests.head(target, timeout=10)
        test_response.raise_for_status()

        print(f"{GREEN}Conexão bem-sucedida com {target}{RESET}")

        try:
            # Realizar várias requisições HTTP para detectar WAFs
            responses = [
                requests.get(target, timeout=10),
                requests.post(target, data={'test': 'test'}, timeout=10),
                requests.head(target, timeout=10)
            ]
            
            for response in responses:
                headers = response.headers

                print("\nCabeçalhos:")
                for key, value in headers.items():
                    print(f"{key}: {GREEN}{value}{RESET}")

        except requests.exceptions.RequestException as e:
            print(f"{RED}Erro durante as requisições de teste: {e}{RESET}")

    except requests.exceptions.SSLError:
        print(f"{RED}Erro de SSL: Tentando com HTTPS...{RESET}")
        try:
            target = target.replace("http://", "https://")
            test_response = requests.head(target, timeout=10)
            test_response.raise_for_status()
            print(f"{GREEN}Conexão segura bem-sucedida com {target}{RESET}")
        except requests.exceptions.RequestException as e:
            print(f"{RED}Falha na conexão HTTPS: {e}{RESET}")

    except requests.exceptions.Timeout:
        print(f"{RED}Erro: Tempo de conexão excedido.{RESET}")

    except requests.exceptions.TooManyRedirects:
        print(f"{RED}Erro: Muitos redirecionamentos para o alvo.{RESET}")

    except requests.exceptions.RequestException as e:
        print(f"{RED}Erro ao conectar-se ao alvo: {e}{RESET}")

    except Exception as e:
        print(f"{RED}Erro inesperado: {e}{RESET}")