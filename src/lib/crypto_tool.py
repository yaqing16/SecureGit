import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA1, HMAC
from Crypto.Util import Counter
import os
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
from src.lib.Git_command import *



def derive_aes_key_from_password(password: str, salt: bytes = None, key_length: int = 32) -> bytes:
    """
    Derive password using HKDF-SHA-256

    :param password: the input password
    :param salt: if not provided, randomly generate
    :param key_length: 16 for AES-128，24 for AES-192，32 for AES-256, default 32
    :return: the AES key
    """
    if salt is None:
        salt = os.urandom(16)

    password_bytes = password.encode("utf-8")

    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=key_length,
        salt=salt,
        info=b"AES Key Derivation", # optional
    )
    aes_key = hkdf.derive(password_bytes)

    return aes_key, salt



#aes_private_key = b'atfwus_test_0011'

password = 'my_secure_password'

salt = b'12345'

aes_private_key, salt = derive_aes_key_from_password(password, salt)

def encrypt_aes(data):
    iv = get_random_bytes(16)

    ctr = Counter.new(128, initial_value=int.from_bytes(iv, 'big'))

    key = aes_private_key.ljust(32, b'\0')[:32]

    # use AES CTR
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)

    ct = cipher.encrypt(data)

    return iv + ct


def decrypt_aes(ct):
    iv = ct[:16]

    key = aes_private_key.ljust(32, b'\0')[:32]

    ctr = Counter.new(128, initial_value=int.from_bytes(iv, 'big'))

    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)

    pt = cipher.decrypt(ct[16:])

    return pt


def der_encrypt_file(data):
    key = aes_private_key.ljust(32, b'\0')[:32]
    hmac = HMAC.new(key, digestmod=SHA1)
    hmac.update(data)
    iv = hmac.digest()


    ctr = Counter.new(128, initial_value=int.from_bytes(iv[:16], 'big'))

    # using CTR mode
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)

    ct = cipher.encrypt(data)

    return iv[:16] + ct

def der_decrypt_file(ct):
    key = aes_private_key.ljust(32, b'\0')[:32]
    iv = ct[:16]

    ctr = Counter.new(128, initial_value=int.from_bytes(iv[:16], 'big'))

    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)

    pt = cipher.decrypt(ct[16:])

    return pt


def generate_Signature(commit, sign_key):
    data_bytes, committer_time, commit_message = get_commit_bytes(commit)

    # print('data_bytes:', data_bytes)

    # Hash the data using SHA-256
    data_hash_obj = SHA256.new(data_bytes)
    # print('hash value:', data_hash_obj.hexdigest())

    # Create a signature using ECDSA (private key)
    signer = DSS.new(sign_key, 'fips-186-3')
    signature = signer.sign(data_hash_obj)
    # print("signature:", signature.hex())

    sigma_str = base64.b64encode(signature).decode('utf-8')

    merged_str = committer_time + "|" + commit_message + "|" + sigma_str

    return merged_str

def test():
    data = '12345'

    #ciphertext = base64.b64encode(encrypt_aes(data.encode()))
    #print("Encrypted:", ciphertext)

    ciphertext = 'gGhbV5NJrpTe3XT5ajmlh0w='

    print(decrypt_aes(base64.b64decode(ciphertext)))




    # # Enc
    # ciphertext = encrypt_aes(data)
    # print("Encrypted:", ciphertext)
    #
    # with open('example_dec.py', 'ab') as sf:
    #     sf.write(ciphertext)
    #
    # # Dec
    # plaintext = decrypt_aes(ciphertext)
    # print("Decrypted:", plaintext.decode())

    # password = "my_secure_password"
    # aes_key, salt = derive_aes_key_from_password(password)
    #
    # print(type(password))
    # print(type(aes_key))
    #
    # print(f"Derived AES Key: {aes_key.hex()}")
    # print(f"Salt: {salt.hex()}")

    # pass
if __name__ == '__main__':
   test()
