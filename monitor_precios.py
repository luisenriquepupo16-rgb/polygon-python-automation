import requests

def check_price():
    # Usamos la API de CoinLore que no tiene bloqueos geográficos
    url = "https://api.coinlore.com/api/ticker/?id=33536" # ID 33536 = Polygon (MATIC)
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0:
            price = float(data[0]['price_usd'])
            print("--- CONEXIÓN EXITOSA ---")
            print(f"El precio de MATIC (Polygon) es: ${price:.4f} USD")

            if price > 1.00:
                print("Sugerencia: Vender")
            else:
                print("Sugerencia: Comprar")
        else:
            print("Error: No se pudieron obtener los datos.")

    except Exception as e:
        print(f"Error de red: {e}")

if __name__ == "__main__":
    check_price()

