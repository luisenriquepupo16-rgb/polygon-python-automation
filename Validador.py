import re
import sys

def validar_direccion_polygon(wallet):
    # Esto limpia espacios y comillas accidentales.
    wallet = wallet.strip().replace("'", "").replace('"', "")
    
    # Patrón oficial: 0x + 40 caracteres hexadecimales
    patron = r"^0x[a-fA-F0-9]{40}$"
    
    if re.match(patron, wallet):
        return True
    return False

if __name__ == "__main__":
        direccion_a_probar = sys.argv[1]
    else:
        direccion_a_probar = "0xD9D9300003b141D825cB7f217162be01F5fe3871"

    if validar_direccion_polygon(direccion_a_probar):
        print(f"✅ VALIDA: {direccion_a_probar}")
    else:
        print(f"❌ ERROR: Formato incorrecto (Longitud: {len(direccion_a_probar)} caracteres)")

