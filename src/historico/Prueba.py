import requests
import time

url = "https://cornerprobet.com/analysis/khujand-cska-pomir/qdk21"
requests_per_minute = 0
start_time = time.time()

# Realizamos solicitudes GET durante un minuto
while time.time() - start_time < 60:
    try:
        response = requests.get(url)
        response.raise_for_status()
        requests_per_minute += 1
        time.sleep(1) # esperamos un segundo antes de realizar la siguiente solicitud
    except requests.exceptions.RequestException:
        print("roto")
        break

print(f"La página {url} admite aproximadamente {requests_per_minute} solicitudes por minuto")
