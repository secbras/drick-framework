import socket
import requests
from urllib.parse import urlparse

def geoip():
    try:
        host = input("\n[\033[93m#\033[0m] Host >> ").strip()
        
        if not host:
            print("\033[31mErro: Nenhum host foi informado.\033[0m")
            return

        # Verifica se o input é um URL completo e extrai o hostname
        parsed_url = urlparse(host)
        if parsed_url.scheme and parsed_url.netloc:
            host = parsed_url.netloc
        
        try:
            ip_address = socket.gethostbyname(host)
        except socket.gaierror:
            print("\033[31mErro: Não foi possível resolver o host. Verifique a conexão ou o nome digitado.\033[0m")
            return

        endpoints = {
            "País": f"https://ipapi.co/{ip_address}/country_name/",
            "Estado": f"https://ipapi.co/{ip_address}/region/",
            "Cidade": f"https://ipapi.co/{ip_address}/city/",
            "Organização": f"https://ipapi.co/{ip_address}/org/",
            "ASN": f"https://ipapi.co/{ip_address}/asn/",
            "Coordenadas": f"https://ipapi.co/{ip_address}/latlong/"
        }

        info_list = [f"IP: \033[32m{ip_address}\033[0m"]

        def fetch_geo_data(url, field_name):
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    data = response.text.strip()
                    return data if data != "None" else None
                return None
            except (requests.RequestException, requests.Timeout) as e:
                print(f"\033[33mAviso: Falha ao obter {field_name} - {str(e)}\033[0m")
                return None

        for key in ["País", "Estado", "Cidade", "Organização", "ASN", "Coordenadas"]:
            data = fetch_geo_data(endpoints[key], key)
            if data:
                info_list.append(f"{key}: \033[32m{data}\033[0m")

        # Exibe os resultados encontrados
        print("\n" + "\n".join(info_list) + "\n")

        # Processamento especial para coordenadas
        coord_info = next((info for info in info_list if info.startswith("Coordenadas:")), None)
        if coord_info:
            try:
                lat_long = coord_info.split(":")[1].strip()
                if "," in lat_long:
                    latitude, longitude = [x.strip() for x in lat_long.split(",")]
                    maps_link = f"\033[32mhttps://www.google.com/maps/search/?api=1&query={latitude},{longitude}\033[0m"
                    print(f"Link para o Google Maps: {maps_link}")
            except Exception as e:
                print(f"\033[33mAviso: Não foi possível gerar link do Maps - {str(e)}\033[0m")
        else:
            print("\033[33mInfo: Coordenadas geográficas não disponíveis para este endereço.\033[0m")

    except KeyboardInterrupt:
        print("\n\033[31mOperação cancelada pelo usuário.\033[0m")
    except Exception as e:
        print(f"\033[31mErro inesperado: {str(e)}\033[0m")

if __name__ == "__main__":
    geoip()