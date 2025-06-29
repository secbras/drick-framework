import socket

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
