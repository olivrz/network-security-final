from Crypto.Cipher import Salsa20
from Crypto.Random import get_random_bytes
import random
import string
import time
import matplotlib.pyplot as plt
import numpy as np

shared_nonce = get_random_bytes(8)
# Stream Cipher
def text_to_bits(text):
    binary_list = []
    for char in text:
        ascii_code = ord(char)
        # Convert ASCII code to a binary string with 8 bits
        binary_string = format(ascii_code, '08b')
        binary_list.append(binary_string)

    bit_stream = ''.join(binary_list)
    return bit_stream
def encrypt(bitstream, key):
    cipher = Salsa20.new(key, shared_nonce)
    ciphertext = cipher.encrypt(bitstream.encode('utf-8'))
    return ciphertext
def decrypt(ciphertext, key):
    cipher = Salsa20.new(key, shared_nonce)
    decrypted_bitstream = cipher.decrypt(ciphertext)
    return decrypted_bitstream
def bits_to_text(bitstream):
    bit_stream = bitstream.decode('utf-8')
    char_list = []

    for i in range(0, len(bit_stream), 8):
        ascii_code = int(bit_stream[i:i + 8], 2)
        char = chr(ascii_code)
        char_list.append(char)

    text = ''.join(char_list)
    return text


def demo_stream_cipher(plaintext, key):
    print("plaintext: ", plaintext)
    text_bits = text_to_bits(plaintext)
    print("bitstream: ", text_bits)
    text_ciphertext = encrypt(text_bits, key)
    print("encryption ciphertext", text_ciphertext)
    text_decrypted_bits = decrypt(text_ciphertext, key)
    print("decryption bitstream", text_decrypted_bits)
    text_recovered = bits_to_text(text_decrypted_bits)
    print("decrypted plaintext", text_recovered)

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
    text_bytes = plaintext.encode()
    text_ciphertext = encrypt2(text_bytes, key)
    print("encryption ciphertext", text_ciphertext)
    text_decrypted_bytes = decrypt(text_ciphertext, key)
    print("decryption bitstream", text_decrypted_bytes)
    text_recovered = text_decrypted_bytes.decode()
    print("decrypted plaintext", text_recovered)
def run_stream_cipher_vectorized(plaintext, key):
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

def demo():
    text1 = "Hi there!"
    key = get_random_bytes(32)

    print("Stream cipher demo: Salsa20")
    demo_stream_cipher(text1, key)
    print(" ")
    text2 = "I hope to see you soon"
    demo_stream_cipher(text2, key)
#demo()

def run_stream_cipher(plaintext, key):
    text_bits = text_to_bits(plaintext)
    text_ciphertext = encrypt(text_bits, key)
    text_decrypted_bits = decrypt(text_ciphertext, key)
    text_recovered = bits_to_text(text_decrypted_bits)

def generate_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
def benchmark_lengths():
    text_len = 10
    text1 = generate_string(text_len)
    text2 = generate_string(text_len * 100)
    text3 = generate_string(text_len * 1000)
    texts = [text1, text2, text3]
    runtimes = {}
    iterations = 1000
    for text in texts:
        text_length = len(text)
        start = time.time()
        print("on new text")
        for i in range(iterations):
            key = get_random_bytes(32)
            run_stream_cipher(text, key)
        end = time.time()
        runtime = end - start
        runtimes[text_length] = runtime
    runtimes_vectorized = {}
    for text in texts:
        text_length = len(text)
        start = time.time()
        print("on new text")
        for i in range(iterations):
            key = get_random_bytes(32)
            run_stream_cipher_vectorized(text, key)
        end = time.time()
        runtime = end - start
        runtimes_vectorized[text_length] = runtime
    x = list(runtimes.keys())
    y = list(runtimes.values())
    y_vector = list(runtimes_vectorized.values())
    plt.plot(x, y, marker='o', linestyle='-', color='b', label='Non-optimized')
    plt.plot(x, y_vector, marker='x', linestyle='-', color='r', label='Vectorized')
    plt.xlabel('Text Length (characters)')
    plt.ylabel('Runtime (s)')
    plt.title('Salsa20 Stream Cipher Runtime vs Text Length')
    plt.grid()
    plt.tight_layout()
    plt.show()
benchmark_lengths()