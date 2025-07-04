# EVM Wallet Generator

This Python script allows you to generate multiple EVM-compatible wallets (e.g. for Ethereum) using BIP39 mnemonics. Each wallet includes an address, private key, and a 12-word mnemonic phrase. The results are saved into an Excel file.

## Features

- Fast wallet generation using multithreading.
- Clean Excel export (wallets.xlsx) with address, private key, and mnemonic.
- Adjustable number of wallets and threads.

## Requirements

- Python 3.7 or higher
- pip (Python package manager)

## Installation & Usage

First, make sure you have Python installed. To set up the project, run the following commands in your terminal or command prompt:

```bash
# Clone the project (if applicable) or move to your project folder
git clone https://github.com/your-username/evm-wallet-generator.git
cd evm-wallet-generator

# Create and activate a virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install the required dependencies
pip install -r requirements.txt

# Run the wallet generator script
python wallet_generator.py