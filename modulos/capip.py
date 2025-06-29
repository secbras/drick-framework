import socket

def capip():
    try:
        # Solicita entrada do usuário
        ent = input("\n[\033[93m#\033[0m] Host >> ").strip()
        
        # Verifica se a entrada não está vazia
        if not ent:
            raise ValueError("\033[31mErro: Nenhum host foi informado.\033[0m")
        
        # Tenta resolver o IP
        try:
            ip = socket.gethostbyname(ent)
        except socket.gaierror as e:
            # Trata diferentes tipos de erros de resolução
            if "Name or service not known" in str(e):
                raise ValueError("\033[31mErro: Host não encontrado ou não resolvível.\033[0m")
            elif "Temporary failure in name resolution" in str(e):
                raise ConnectionError("\033[31mErro: Falha temporária na resolução de nome. Verifique sua conexão.\033[0m")
            else:
                raise
            
        # Formata a saída
        ip_formatado = f"\033[32m{ip}\033[0m"
        print(f"\nIP: {ip_formatado}")
        
    except ValueError as e:
        print(f"\n{e}")
    except ConnectionError as e:
        print(f"\n{e}")
    except socket.herror:
        print("\n\033[31mErro: Endereço IP inválido.\033[0m")
    except socket.timeout:
        print("\n\033[31mErro: Tempo excedido ao tentar resolver o host.\033[0m")
    except KeyboardInterrupt:
        print("\n\033[31mOperação cancelada pelo usuário.\033[0m")
    except Exception as e:
        print(f"\n\033[31mErro inesperado: {str(e)}\033[0m")

