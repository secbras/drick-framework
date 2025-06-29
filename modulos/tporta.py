import socket

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
