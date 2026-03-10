# 🐉 Kin Arsenal - Polygon Automation Tool

**Kin Arsenal** is a specialized Python-based CLI tool designed for efficient management and monitoring of assets on the **Polygon (MATIC) Blockchain**. Developed with a focus on speed, security, and dual-language accessibility, this tool provides a comprehensive suite of utilities for developers and crypto-enthusiasts alike.

## 🚀 Key Features

* **Real-Time Price Monitoring**: Instant MATIC/USDT price updates using Binance API with a secondary backup server (CryptoCompare) to ensure uptime.
* **Dual-Currency Support**: Full integration for both native **MATIC** and **USDT (Polygon PoS)** transactions.
* **Audit Logging System**: Optional session recording that saves every operation (prices, balances, and transaction hashes) into a `kin_log.txt` file for future auditing.
* **Bilingual Interface**: Seamlessly switch between **English** and **Spanish** in real-time within the dashboard.
* **Advanced Networking**: Built-in resilience for VPN users with extended timeouts and a multi-node rotation system (Ankr, 1RPC, LlamaNodes).
* **Gas Station Integration**: Real-time gas price tracking to optimize transaction costs.
* **Wallet Security**: Secure wallet generation using `secrets` and `eth_account`, ensuring high-entropy private keys.

## 🛠️ Modules Included

1. **Price Monitor**: Current MATIC value in USD.
2. **Gas Tracker**: Monitor network congestion (Gwei).
3. **Address Validator**: RegEx-based format validation for Ethereum-style addresses.
4. **Balance Checker**: Simultaneous MATIC and USDT balance lookup for any public address.
5. **Wallet Generator**: Create new secure wallets for the Polygon network.
6. **Transaction Module**: Securely send MATIC or USDT with manual confirmation and automatic gas adjustment (+20% for faster mining).
7. **Log System (Toggle)**: Enable/Disable the local activity recorder.
8. **Language Switch**: Toggle the entire UI between English and Spanish.

## 📦 Installation

1. **Clone the repository**:
```bash
git clone https://github.com/luisenriquepupo16-rgb/Polygon-Python-Automation.git
cd Polygon-Python-Automation

```


2. **Install dependencies**:
```bash
pip install web3 requests eth-account

```


3. **Run the tool**:
```bash
python Kin_Panel.py

```



## 🛡️ Security Disclaimer

This tool handles sensitive information (Private Keys). **Never share your `kin_log.txt` if it contains private keys** and never upload your private keys to GitHub. The developer is not responsible for any lost funds. Use with caution and always verify recipient addresses before broadcasting transactions.
