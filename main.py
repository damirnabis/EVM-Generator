from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
from eth_account import Account
import openpyxl
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

Account.enable_unaudited_hdwallet_features()

lock = threading.Lock()  # Для потокобезопасной записи в список

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
    max_threads = int(input("Сколько потоков использовать? (напр. 4, 8, 16): "))

    wallets = []
    progress_bar = tqdm(total=count, desc="Генерация", ncols=80)

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(generate_wallet) for _ in range(count)]

        for future in as_completed(futures):
            wallet = future.result()
            with lock:
                wallets.append(wallet)
                progress_bar.update(1)

    progress_bar.close()
    save_to_excel(wallets)

if __name__ == "__main__":
    main()