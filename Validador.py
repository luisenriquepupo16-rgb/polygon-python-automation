import re

def validar_direccion_polygon(wallet):
    # Una dirección real empieza por 0x y tiene 40 caracteres más (42 total)
    patron = r"^0x[a-fA-F0-9]{40}$"
    
    if re.match(patron, wallet):
        return True
    else:
        return False

# Prueba con tu dirección (pon la tuya entre las comillas)
mi_wallet = "TU_DIRECCION_AQUI" 

if validar_direccion_polygon(mi_wallet):
    print("✅ DIRECCION VALIDA: Lista para recibir USDT")
else:
    print("❌ ERROR: Formato de direccion incorrecto")

