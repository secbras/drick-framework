import socket

def ping():
    try:
        # Exibe as opções de teste
        print("Você pode testar os seguintes modelos:\n")
        print("1 - \033[33m\"www.google.com\"\033[0m")
        print("2 - \033[33m\"google.com\"\033[0m")
        print("3 - \033[33m\"8.8.8.8 (Google DNS)\"\033[0m")

        # Solicita entrada do usuário
        host = input("\n[\033[93m#\033[0m] Host >> ").strip()
        
        # Verifica se o host foi informado
        if not host:
            raise ValueError("\033[31mErro: Nenhum host foi informado.\033[0m")
        
        print("\n")

        # Verifica se é um IP válido
        try:
            socket.inet_aton(host)
            is_ip = True
        except socket.error:
            is_ip = False

        host_online = False

        def check_port(host, port, service):
            nonlocal host_online
            try:
                # Cria e configura o socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)  # Timeout reduzido para 3 segundos
                
                # Tenta conectar
                result = sock.connect_ex((host, port))
                
                # Exibe o resultado
                if result == 0:
                    print(f"\033[32m ✔️ \033[0m {host}:{port} ({service}) está online.")
                    host_online = True
                else:
                    print(f"\033[33m ❌ \033[0m {host}:{port} ({service}) está offline ou inacessível.")
                
                sock.close()
                
            except socket.timeout:
                print(f"\033[33m ⏱️ \033[0m {host}:{port} ({service}) timeout - sem resposta.")
            except socket.gaierror:
                print(f"\033[31m 🔍 \033[0m {host}:{port} ({service}) - não foi possível resolver o host.")
            except ConnectionRefusedError:
                print(f"\033[33m 🚪 \033[0m {host}:{port} ({service}) - conexão recusada.")
            except Exception as e:
                print(f"\033[31m ⚠️ \033[0m Erro ao testar {host}:{port} ({service}): {str(e)}")

        # Lista de portas para testar
        ports_to_check = [
            (80, "HTTP"),
            (443, "HTTPS"),
            (21, "FTP"),
            (22, "SSH"),
            (25, "SMTP"),
            (110, "POP3"),
            (143, "IMAP"),
            (3306, "MySQL"),
            (5432, "PostgreSQL"),
            (27017, "MongoDB")
        ]

        # Testa todas as portas
        for port, service in ports_to_check:
            check_port(host, port, service)

        # Resumo final
        if host_online:
            print(f"\nHost {host} está \033[32monline\033[0m (pelo menos um serviço respondendo).")
        else:
            print(f"\nHost {host} está \033[31moffline\033[0m ou todos os serviços testados não responderam.")

    except ValueError as e:
        print(f"\n{e}")
    except KeyboardInterrupt:
        print("\n\033[31mOperação cancelada pelo usuário.\033[0m")
    except Exception as e:
        print(f"\n\033[31mErro inesperado: {str(e)}\033[0m")

if __name__ == "__main__":
    ping()