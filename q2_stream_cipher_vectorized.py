from Crypto.Cipher import Salsa20
from Crypto.Random import get_random_bytes

shared_nonce = get_random_bytes(8)
# Stream Cipher

def encrypt2(bitstream, key):
    cipher = Salsa20.new(key, shared_nonce)
    ciphertext = cipher.encrypt(bitstream)
    return ciphertext
def decrypt(ciphertext, key):
    cipher = Salsa20.new(key, shared_nonce)
    decrypted_bitstream = cipher.decrypt(ciphertext)
    return decrypted_bitstream
def demo_stream_cipher_vectorized(plaintext, key):
    print("plaintext: ", plaintext)
    #print("bitstream: ", text_bits)
    text_bytes = plaintext.encode()
    text_ciphertext = encrypt2(text_bytes, key)
    print("encryption ciphertext", text_ciphertext)
    text_decrypted_bytes = decrypt(text_ciphertext, key)
    print("decryption bitstream", text_decrypted_bytes)
    text_recovered = text_decrypted_bytes.decode() #bits_to_text_vectorized(text_decrypted_bits)
    print("decrypted plaintext", text_recovered)
def run_stream_cipher_vectorized(plaintext, key):
    #text_bits = text_to_bits_vectorized(plaintext)
    text_bytes = plaintext.encode()
    text_ciphertext = encrypt2(text_bytes, key)
    text_decrypted_bytes = decrypt(text_ciphertext, key)
    # Convert the bytes object to text
    text_recovered = text_decrypted_bytes.decode()
def demo_vectorized():
    text1 = "Hi there!"
    key = get_random_bytes(32)
    print("Stream cipher vectorized demo: Salsa20")
    demo_stream_cipher_vectorized(text1, key)
    print(" ")
    text2 = "I hope to see you soon"
    demo_stream_cipher_vectorized(text2, key)
demo_vectorized()