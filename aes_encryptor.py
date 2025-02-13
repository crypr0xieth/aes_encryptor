from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

# Генерация ключа и вектора инициализации (IV)
def generate_key_iv():
    key = os.urandom(32)  # 256-битный ключ
    iv = os.urandom(16)   # 128-битный IV
    return key, iv

# Шифрование текста
def encrypt_text(plaintext, key, iv):
    # Добавление padding для соответствия размеру блока
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()

    # Шифрование
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return ciphertext

# Дешифрование текста
def decrypt_text(ciphertext, key, iv):
    # Дешифрование
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Удаление padding
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext.decode()

# Основная функция
def main():
    print("AES Text Encryptor/Decryptor")
    key, iv = generate_key_iv()

    while True:
        print("\n1. Encrypt Text")
        print("2. Decrypt Text")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            plaintext = input("Enter text to encrypt: ")
            ciphertext = encrypt_text(plaintext, key, iv)
            print(f"Encrypted Text (hex): {ciphertext.hex()}")
            print(f"Key (hex): {key.hex()}")
            print(f"IV (hex): {iv.hex()}")

        elif choice == "2":
            ciphertext_hex = input("Enter encrypted text (hex): ")
            key_hex = input("Enter key (hex): ")
            iv_hex = input("Enter IV (hex): ")

            try:
                ciphertext = bytes.fromhex(ciphertext_hex)
                key = bytes.fromhex(key_hex)
                iv = bytes.fromhex(iv_hex)

                plaintext = decrypt_text(ciphertext, key, iv)
                print(f"Decrypted Text: {plaintext}")
            except ValueError:
                print("Invalid input. Please check your hex values.")

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
