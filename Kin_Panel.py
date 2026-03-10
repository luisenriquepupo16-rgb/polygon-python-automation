import requests
import re
import sys
import secrets
import json
import os
from datetime import datetime
from eth_account import Account
from web3 import Web3

# --- CONFIGURACIÓN DE RED Y CONTRATOS (POLYGON) ---
USDT_CONTRACT = "0xc2132D05D31c914a87C6611C10748AEb04B58e8F"
ERC20_ABI = json.loads('[{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"}]')

# --- VARIABLES DE ESTADO LOCAL ---
LOG_ACTIVADO = False
ARCHIVO_LOG = "kin_log.txt"
IDIOMA = "ES"  # "ES" o "EN"

# --- DICCIONARIO DE INTERFAZ MULTI-IDIOMA ---
TEXTOS = {
    "ES": {
        "menu_titulo": "ARSENAL DE KIN - POLYGON",
        "opciones": ["Salir", "Ver Precio MATIC", "Ver Estado Gas", "Validar Direccion", "Consultar Saldos", "Generar Billetera", "Enviar Fondos", "Registro (LOG)", "Cambiar Idioma / Change Language"],
        "status_log": "Registro ahora:",
        "precio_info": "[INFO] Precio MATIC (Binance):",
        "precio_alt": "[INFO] Precio MATIC (Respaldo):",
        "err_conexion": "[!] Error de conexion. Reintentando...",
        "err_nodos": "[!] Error: Los nodos no responden (Verifica tu conexion/VPN).",
        "gas_titulo": "--- ESTADO DEL GAS ---",
        "valida": "[OK] VALIDA:",
        "invalida": "[X] ERROR: Formato incorrecto.",
        "saldos_titulo": "--- SALDOS EN RED (POLYGON) ---",
        "cuenta": "Cuenta:",
        "gen_titulo": "--- NUEVA BILLETERA GENERADA ---",
        "envio_titulo": "--- MODULO DE ENVIO (MATIC/USDT) ---",
        "sel_moneda": "Seleccione moneda (1: MATIC, 2: USDT): ",
        "tu_dir": "Tu direccion: ",
        "tu_key": "Tu CLAVE PRIVADA: ",
        "dest": "Destinatario: ",
        "cant": "Cantidad a enviar: ",
        "confirmar": "¿Confirmar? (s/n): ",
        "exito": "✅ ENVIADO EXITOSAMENTE. Hash:",
        "sistema_conn": "[SISTEMA] Estableciendo conexión segura...",
        "input_opcion": "Seleccione una opcion: ",
        "input_dir": "Pegue la direccion: "
    },
    "EN": {
        "menu_titulo": "KIN ARSENAL - POLYGON",
        "opciones": ["Exit", "View MATIC Price", "View Gas Status", "Validate Address", "Check Balances", "Generate Wallet", "Send Funds", "Log Recording", "Cambiar Idioma / Change Language"],
        "status_log": "Log now:",
        "precio_info": "[INFO] MATIC Price (Binance):",
        "precio_alt": "[INFO] MATIC Price (Backup):",
        "err_conexion": "[!] Connection error. Retrying...",
        "err_nodos": "[!] Error: Nodes not responding (Check your connection/VPN).",
        "gas_titulo": "--- GAS STATUS ---",
        "valida": "[OK] VALID:",
        "invalida": "[X] ERROR: Incorrect format.",
        "saldos_titulo": "--- NETWORK BALANCES (POLYGON) ---",
        "cuenta": "Account:",
        "gen_titulo": "--- NEW WALLET GENERATED ---",
        "envio_titulo": "--- SENDING MODULE (MATIC/USDT) ---",
        "sel_moneda": "Select currency (1: MATIC, 2: USDT): ",
        "tu_dir": "Your address: ",
        "tu_key": "Your PRIVATE KEY: ",
        "dest": "Recipient: ",
        "cant": "Amount to send: ",
        "confirmar": "Confirm? (y/n): ",
        "exito": "✅ SENT SUCCESSFULLY. Hash:",
        "sistema_conn": "[SYSTEM] Establishing secure connection...",
        "input_opcion": "Select an option: ",
        "input_dir": "Paste address: "
    }
}

def t(clave): return TEXTOS[IDIOMA][clave]

# --- LOGICA DE FUNCIONAMIENTO ---

def registrar_evento(mensaje):
    if LOG_ACTIVADO:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(ARCHIVO_LOG, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] {mensaje}\n")
        except: pass

def consultar_precio():
    try:
        data = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=MATICUSDT", timeout=10).json()
        print(f"\n{t('precio_info')} ${float(data['price']):.4f} USD")
    except:
        try:
            res_alt = requests.get("https://min-api.cryptocompare.com/data/price?fsym=MATIC&tsyms=USD").json()
            print(f"\n{t('precio_alt')} ${res_alt['USD']} USD")
        except: print(f"\n{t('err_conexion')}")

def get_gas_price():
    try:
        data = requests.get("https://gasstation.polygon.technology/v2", timeout=10).json()
        print(f"\n{t('gas_titulo')}\nStandard: {data['standard']['maxFee']:.2f} Gwei")
    except: print(f"\n{t('err_conexion')}")

def validar_direccion(wallet):
    wallet = wallet.strip().replace("'", "").replace('"', "")
    if re.match(r"^0x[a-fA-F0-9]{40}$", wallet):
        print(f"\n{t('valida')} {wallet}")
        return True
    print(f"\n{t('invalida')}")
    return False

def consultar_saldo(direccion):
    nodos = ["https://polygon-rpc.com", "https://rpc.ankr.com/polygon"]
    direccion = direccion.strip().replace("'", "").replace('"', "")
    if not re.match(r"^0x[a-fA-F0-9]{40}$", direccion): return
    for url in nodos:
        try:
            w3 = Web3(Web3.HTTPProvider(url, request_kwargs={'timeout': 15}))
            if w3.is_connected():
                check_dir = w3.to_checksum_address(direccion)
                balance_matic = w3.eth.get_balance(check_dir) / 10**18
                contract = w3.eth.contract(address=USDT_CONTRACT, abi=ERC20_ABI)
                balance_usdt = contract.functions.balanceOf(check_dir).call() / 10**6
                print(f"\n{t('saldos_titulo')}\n{t('cuenta')} {check_dir}\nMATIC: {balance_matic:.6f}\nUSDT: {balance_usdt:.2f}")
                return
        except: continue
    print(f"\n{t('err_nodos')}")

def generar_billetera():
    priv = "0x" + secrets.token_hex(32)
    acct = Account.from_key(priv)
    print(f"\n{t('gen_titulo')}\nADDRESS: {acct.address}\nPRIVATE KEY: {priv}")

def enviar_fondos():
    nodos = ["https://polygon-rpc.com", "https://rpc.ankr.com/polygon"]
    w3 = None
    print(f"\n{t('sistema_conn')}")
    for url in nodos:
        try:
            temp_w3 = Web3(Web3.HTTPProvider(url, request_kwargs={'timeout': 20}))
            if temp_w3.is_connected():
                w3 = temp_w3
                break
        except: continue
    if not w3:
        print(f"\n{t('err_nodos')}")
        return
    print(f"\n{t('envio_titulo')}")
    try:
        tipo = input(t('sel_moneda'))
        orig = w3.to_checksum_address(input(t('tu_dir')).strip())
        key = input(t('tu_key')).strip()
        dest = w3.to_checksum_address(input(t('dest')).strip())
        cantidad = float(input(t('cant')))
        gas_price = int(w3.eth.gas_price * 1.2)
        nonce = w3.eth.get_transaction_count(orig)
        if tipo == "1":
            tx = {'nonce': nonce, 'to': dest, 'value': w3.to_wei(cantidad, 'ether'), 'gas': 21000, 'gasPrice': gas_price, 'chainId': 137}
        else:
            contract = w3.eth.contract(address=USDT_CONTRACT, abi=ERC20_ABI)
            tx = contract.functions.transfer(dest, int(cantidad * 10**6)).build_transaction({'chainId': 137, 'gas': 65000, 'gasPrice': gas_price, 'nonce': nonce})
        
        confirm_key = 's' if IDIOMA == "ES" else 'y'
        if input(t('confirmar')).lower() == confirm_key:
            signed = w3.eth.account.sign_transaction(tx, key)
            h = w3.eth.send_raw_transaction(signed.raw_transaction)
            print(f"\n{t('exito')} {w3.to_hex(h)}")
    except Exception as e: print(f"\n[X] Error: {e}")

# --- MENÚ DE CONTROL ---
def main():
    global LOG_ACTIVADO, IDIOMA
    Account.enable_unaudited_hdwallet_features()
    while True:
        txt = TEXTOS[IDIOMA]
        st_log = "ON" if LOG_ACTIVADO else "OFF"
        print("\n" + "="*40 + f"\n         {txt['menu_titulo']}\n" + "="*40)
        for i, opcion in enumerate(txt['opciones'][1:], 1):
            if i == 7: print(f" 7. {opcion}: {st_log}")
            else: print(f" {i}. {opcion}")
        print(f" 0. {txt['opciones'][0]}")
        print("-" * 40)
        
        opc = input(txt['input_opcion'])
        if opc == "1": consultar_precio()
        elif opc == "2": get_gas_price()
        elif opc == "3": validar_direccion(input(txt['input_dir']))
        elif opc == "4": consultar_saldo(input(txt['input_dir']))
        elif opc == "5": generar_billetera()
        elif opc == "6": enviar_fondos()
        elif opc == "7":
            LOG_ACTIVADO = not LOG_ACTIVADO
            print(f"\n{txt['status_log']} {LOG_ACTIVADO}")
        elif opc == "8":
            IDIOMA = "EN" if IDIOMA == "ES" else "ES"
        elif opc == "0": break
        else: print("\nInvalid / No valida")

if __name__ == "__main__":
    main()
