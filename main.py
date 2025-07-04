from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
from eth_account import Account
import openpyxl

Account.enable_unaudited_hdwallet_features()

def generate_wallet():
    mnemonic = Bip39MnemonicGenerator().FromWordsNumber(12)
    
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
    
    bip44_wallet = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM).Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
    
    private_key = bip44_wallet.PrivateKey().Raw().ToHex()
    address = bip44_wallet.PublicKey().ToAddress()

    return {
        "address": address,
        "private_key": private_key,
        "mnemonic": str(mnemonic)
    }

def save_to_excel(wallets, filename="wallets.xlsx"):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "EVM Wallets"
    ws.append(["Address", "Private Key", "Mnemonic"])
    
    for wallet in wallets:
        ws.append([wallet["address"], wallet["private_key"], wallet["mnemonic"]])
    
    wb.save(filename)
    print(f"[+] Сохранено в {filename}")

def main():
    count = int(input("Сколько кошельков сгенерировать? "))
    wallets = [generate_wallet() for _ in range(count)]
    save_to_excel(wallets)

if __name__ == "__main__":
    main()
