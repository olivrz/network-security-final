from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import random, string, time, matplotlib.pyplot as plt
def demo_DES_CBC(text):
    print("DES demo with CBC mode")
    print("text plaintext: ", text)
    key = get_random_bytes(8)
    iv = get_random_bytes(8)
    # Create a cipher object with the key and the IV
    cipher = DES.new(key, DES.MODE_CBC, iv)
    text = text.encode('utf-8')
    # Pad the text with bytes
    text = pad(text, 8)
    ciphertext = cipher.encrypt(text)
    print("text ciphertext: ", ciphertext.hex())
    new_cipher = DES.new(key, DES.MODE_CBC, iv)
    recovered_text = new_cipher.decrypt(ciphertext)
    recovered_text = unpad(recovered_text, 8)
    recovered_text = recovered_text.decode('utf-8')
    print("recovered text: ", recovered_text)
def demo_DES_ECB(text):
    key = get_random_bytes(8)
    print("DES demo with ECB mode")
    print("text plaintext: ", text)
    cipher = DES.new(key, DES.MODE_ECB)
    text = text.encode('utf-8')
    # Pad the text with bytes
    text = pad(text, 8)
    ciphertext = cipher.encrypt(text)
    print("text ciphertext: ", ciphertext.hex())
    new_cipher = DES.new(key, DES.MODE_ECB)
    recovered_text = new_cipher.decrypt(ciphertext)
    recovered_text = unpad(recovered_text, 8)
    recovered_text = recovered_text.decode('utf-8')
    print("recovered text: ", recovered_text)
text1 = "Hi there! This is a text message with short length"
demo_DES_CBC(text1)
demo_DES_ECB(text1)

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
def benchmark_lengths():
    text_len = 10
    text1 = generate_string(text_len)
    text2 = generate_string(text_len * 100)
    text3 = generate_string(text_len * 10000)
    texts = [text1, text2, text3]
    modes = ["ECB", "CBC"]
    runtimes = {}
    iterations = 10000
    for mode in modes:
        runtimes[mode] = {}
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
            runtimes[mode][text_length] = runtime
    ECB_runtimes = [runtimes["ECB"][length] for length in runtimes["ECB"]]
    CBC_runtimes = [runtimes["CBC"][length] for length in runtimes["CBC"]]
    text_lengths = list(runtimes["ECB"].keys())
    # Plotting the grouped bar chart
    bar_width = 0.35
    index = list(range(len(text_lengths)))
    fig, ax = plt.subplots()
    bar1 = ax.bar(index, ECB_runtimes, bar_width, label='ECB')
    bar2 = ax.bar([i + bar_width for i in index], CBC_runtimes, bar_width, label='CBC')
    ax.set_title('Comparison in Runtime of DES modes and text length')
    ax.set_xlabel('Text Length (characters)')
    ax.set_ylabel('Runtime (s)')
    ax.set_xticks([i + bar_width / 2 for i in index])
    ax.set_xticklabels(text_lengths)
    ax.legend()

    plt.tight_layout()
    plt.show()
benchmark_lengths()