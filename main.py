import os
import sys
import random
import requests
from colorama import Fore, Style, init
init()

# Adiciona o diretório raiz ao path para importações
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importações modulares
from modulos.ping import ping
from modulos.capip import capip
from modulos.cbanner import cbanner
from modulos.geoip import geoip
from modulos.pscan import pscan
from modulos.elink import elink
from modulos.siteping import siteping
from modulos.luckfaha import luckfaha
from modulos.sendys import sendys
from modulos.deviceinfo import deviceinfo
from modulos.yanshu import yanshu

def mostrar_banner():
    nomep = "\033[36mDRICK FRAMEWORK\033[0;0m"

    print("""\n\n\n      ▄▄▄▄▄▄▄▄▄▄   ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄ 
     ▐░░░░░░░░░░▌ ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌  ▐░▌
     ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌ ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░▌ ▐░▌
     ▐░▌       ▐░▌▐░▌       ▐░▌     ▐░▌     ▐░▌          ▐░▌▐░▌
     ▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄█░▌     ▐░▌     ▐░▌          ▐░▌░▌
     ▐░▌       ▐░▌▐░░░░░░░░░░░▌     ▐░▌     ▐░▌          ▐░░▌
     ▐░▌       ▐░▌▐░█▀▀▀▀█░█▀▀      ▐░▌     ▐░▌          ▐░▌░▌
     ▐░▌       ▐░▌▐░▌     ▐░▌       ▐░▌     ▐░▌          ▐░▌▐░▌
     ▐░█▄▄▄▄▄▄▄█░▌▐░▌      ▐░▌  ▄▄▄▄█░█▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ ▐░▌ ▐░▌
      ░░░░░░░░░░▌ ▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌  ▐░▌
      ▀▀▀▀▀▀▀▀▀▀   ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀    ▀""")

    print("\n\n###########  ########  ##### ### ######  ########  ######## # ##  #####")
    print(f"####### ###### ##### --| {nomep} |-- #########\033[36m v[1.1] \033[0;0m#########")
    print("######## ###  ####### ############ ######## # ## #####  # # #  #### ### \n\n")

def get_random_phrase():
    url = "https://raw.githubusercontent.com/secbras/drick-framework/main/frases.txt"
    try:
        response = requests.get(url)
        lines = response.text.split('\n')
        return random.choice(lines) if lines else "Bem-vindo ao Drick Framework"
    except:
        return "Error fetching the file."

def mostrar_comandos():
    print("""\n\nPARA USAR UMA FERRAMENTA UTILIZE O COMANDO ENTRE PARENTESES.\n \n\n[#] COMANDOS USUAIS:\n\nPing Host                               (\033[32mping\033[0;0m)\nCapturar IP                             (\033[32mcapip\033[0;0m)\nCapturar banner                         (\033[32mcbanner\033[0;0m)\nLocalizar IP                            (\033[32mlocip\033[0;0m)\nExtrator de Links                       (\033[32melink\033[0;0m)\nEscaner de Portas                       (\033[32mpscan\033[0;0m)\nTestador de Links                       (\033[32msiteping\033[0;0m)\nBuscador de Serviços                    (\033[32manunn4ki\033[0;0m)\nAnálise de Cabeçalho                    (\033[32msendys\033[0;0m)\nBuscador de Subdomínio                  (\033[32myanshu\033[0;0m)\nSobre este Dispositivo                  (\033[32mdeviceinfo\033[0;0m)""")

def mostrar_info():
    print("""\n\n                      \033[32mDRICK FRAMEWORK\033[0;0m\n O software (Drick Framework) é um pacote com vários algoritimos essênciais para um bom pentesting e uma boa análise de um sistema ou rede, o nosso software busca sempre agrupar as melhores alternativas para uma boa análise e uma rede de testes.\n\n\n                    \033[32mCOMANDOS ADICIONAIS\033[0;0m\n1 - Caso queira consultar alguma informação a respeito de algum programa da plataforma use o comando (/info) + Programa, por exemplo (/info ping), este comando retornará as principais informações sobre o mesmo.\n\n2 - Caso deseje fechar a framework utilize o comando (/sair)\n\n3 - Utilize os comandos (/limpar),(/clear) ou (/cls) para limpar a tela.""")

def mostrar_info_especifica(comando):
    info_dict = {
        "ping": "\n\033[32m PING\n\033[0;0m\nPING é um algorítimo usado para testar uma máquina remota a fim de determinar se ela está online ou offline e obter dados de sua requisição como tempo de resposta.",
        "capip": "\n\033[32m CAPIP (CAPTURAR IP)\n\033[0;0m\nCAPIP tem como função obter o endereço remoto de uma determinada máquina na rede, o algorítimo captura o IP (Internet Protocol) através de uma requisição.",
        "locip": "\n\033[32m LOCIP\n\033[0;0m\nEsta função lhe permite rastrear um dispositivo e obter características de sua localização.",
        "cbanner": "\n\033[32m CBANNER (CAPTURAR BANNER)\n\033[0;0m\nA partir de requisições ao alvo, é possível obter o serviço e sua versão que está a rodar em uma determinada porta. Com esta informação, é possível buscar um exploit.",
        "elink": "\n\033[32m ELINK (Extraidor de Link)\n\033[0;0m\nEsse algoritmo tem como função extrair links de uma determinada página na web.",
        "pscan": "\n\033[32m PSCAN (Scanner de Portas)\n\033[0;0m\nPSCAN é um scanner de portas simples que tem o intuito de testar as principais portas de um host e determinar se as mesmas estão abertas ou fechadas.",
        "siteping": "\n\033[32m SITEPING\n\033[0;0m\nSITEPING é uma ferramenta que permite verificar o status de vários sites em massa, basta adicionar os sites em formato de lista no arquivo sites.txt no diretório do Drick Framework"
    }
    
    comando = comando.replace("/info ", "").strip()
    print(info_dict.get(comando, "\nComando não encontrado. Use /c para ver a lista de comandos."))

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    mostrar_banner()
    fraserandom = get_random_phrase()
    print(f"\033[31m[+]\033[0;0m {fraserandom}")
    print("\n\n", f"\033[33m[+]\033[0;0m Use (/c) para listar os comandos.", 
          f"\033[33m\n")
    
    while True:
        try:
            comando = input("\n[\033[32m#\033[0;0m] >> ").strip().lower()
            
            if comando == "/sair":
                print("Saindo do Drick Framework...")
                break
                
            elif comando == "/c":
                mostrar_comandos()
                
            elif comando == "/info":
                mostrar_info()
                
            elif comando.startswith("/info "):
                mostrar_info_especifica(comando)
                
            elif comando in ["/limpar", "/clear", "/cls"]:
                limpar_tela()
                
            # Chamadas de funções dos módulos
            elif comando == "ping": ping()
            elif comando == "capip": capip()
            elif comando == "cbanner": cbanner()
            elif comando == "locip": geoip()
            elif comando == "pscan": pscan()
            elif comando == "elink": elink()
            elif comando == "siteping": siteping()
            elif comando == "luckfaha": luckfaha()
            elif comando == "sendys": sendys()
            elif comando == "deviceinfo": deviceinfo()
            elif comando == "yanshu": yanshu()
                
            else:
                print("\033[31m[!] Comando não reconhecido. Digite /c para ver os comandos disponíveis.\033[0;0m")
                
        except KeyboardInterrupt:
            print("\n\nUse o comando /sair para encerrar o programa corretamente.")
        except Exception as e:
            print(f"\033[31m[!] Erro: {e}\033[0;0m")

if __name__ == "__main__":
    main()