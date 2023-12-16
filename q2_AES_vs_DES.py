from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import random, string, time, matplotlib.pyplot as plt
def run_DES_CBC(text):
    key = get_random_bytes(8)
    iv = get_random_bytes(8)
    # Create a cipher object with the key and the IV
    cipher = DES.new(key, DES.MODE_CBC, iv)
    text = text.encode('utf-8')
    # Pad the text with bytes
    text = pad(text, 8)
    ciphertext = cipher.encrypt(text)
    new_cipher = DES.new(key, DES.MODE_CBC, iv)
    recovered_text = new_cipher.decrypt(ciphertext)
    recovered_text = unpad(recovered_text, 8)
    recovered_text = recovered_text.decode('utf-8')
def run_DES_ECB(text):
    key = get_random_bytes(8)
    cipher = DES.new(key, DES.MODE_ECB)
    text = text.encode('utf-8')
    # Pad the text with bytes
    text = pad(text, 8)
    ciphertext = cipher.encrypt(text)
    new_cipher = DES.new(key, DES.MODE_ECB)
    recovered_text = new_cipher.decrypt(ciphertext)
    recovered_text = unpad(recovered_text, 8)
    recovered_text = recovered_text.decode('utf-8')

def generate_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def run_AES_ECB(text):
    key = get_random_bytes(32)
    cipher = AES.new(key, AES.MODE_ECB)
    text = text.encode('utf-8')
    # Pad the text with bytes since AES is a block cipher
    text = pad(text, 16)
    ciphertext = cipher.encrypt(text)

    # Create a new cipher for user 2 to decrypt the ciphertext
    new_cipher = AES.new(key, AES.MODE_ECB)
    recovered_text = new_cipher.decrypt(ciphertext)
    recovered_text = unpad(recovered_text, 16)
    recovered_text = recovered_text.decode('utf-8')

def run_AES_CBC(text):
    key = get_random_bytes(32)
    initial_value = get_random_bytes(16)

    # Create a cipher object with the key and initial value
    cipher = AES.new(key, AES.MODE_CBC, initial_value)
    text = text.encode('utf-8')

    # Pad the text with bytes
    text = pad(text, 16)
    ciphertext = cipher.encrypt(text)

    # Create new cipher to decrypt cipher text for user 2
    new_cipher = AES.new(key, AES.MODE_CBC, initial_value)
    recovered_text = new_cipher.decrypt(ciphertext)
    recovered_text = unpad(recovered_text, 16)
    recovered_text = recovered_text.decode('utf-8')

def generate_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
def benchmark_lengths_AES_vs_DES():
    text_len = 10
    text1 = generate_string(text_len)
    text2 = generate_string(text_len * 100)
    text3 = generate_string(text_len * 10000)
    texts = [text1, text2, text3]
    modes = ["CBC"]
    aes_runtimes = {}
    des_runtimes = {}
    iterations = 10000
    for mode in modes:
        for text in texts:
            text_length = len(text)
            start = time.time()
            for i in range(iterations):
                if mode == "ECB":
                    run_AES_ECB(text)
                else:
                    run_AES_CBC(text)
            end = time.time()
            runtime = end - start
            aes_runtimes[text_length] = runtime
        for text in texts:
            text_length = len(text)
            start = time.time()
            for i in range(iterations):
                if mode == "ECB":
                    run_DES_ECB(text)
                else:
                    run_DES_CBC(text)
            end = time.time()
            runtime = end - start
            des_runtimes[text_length] = runtime

    # Plotting the grouped bar chart
    bar_width = 0.35
    text_lengths = list(aes_runtimes.keys())
    index = list(range(len(text_lengths)))
    aes_y = [aes_runtimes[length] for length in aes_runtimes]
    des_y = [des_runtimes[length] for length in des_runtimes]
    print(aes_runtimes)
    fig, ax = plt.subplots()
    aes_bars = ax.bar(index, aes_y, bar_width, label='AES', color='red')
    des_bars = ax.bar([i + bar_width for i in index], des_y, bar_width, label='DES', color='blue')

    ax.set_title('Average Runtimes of AES and DES with CBC Modes')
    ax.set_xlabel('Text Length (characters)')
    ax.set_ylabel('Average Runtime (s)')
    ax.set_xticks([i + bar_width / 2 for i in index])
    ax.set_xticklabels(text_lengths)
    ax.legend()

    plt.tight_layout()
    plt.show()
benchmark_lengths_AES_vs_DES()