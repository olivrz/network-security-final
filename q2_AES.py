import time
import matplotlib.pyplot as plt
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import random
import string

def demo_AES_ECB(text):
    key = get_random_bytes(32)

    print("AES demo with ECB mode")
    print("text plaintext: ", text)

    cipher = AES.new(key, AES.MODE_ECB)
    text = text.encode('utf-8')
    # Pad the text with bytes since AES is a block cipher
    text = pad(text, 16)
    ciphertext = cipher.encrypt(text)

    print("text ciphertext: ", ciphertext.hex())

    # Create a new cipher for user 2 to decrypt the ciphertext
    new_cipher = AES.new(key, AES.MODE_ECB)
    recovered_text = new_cipher.decrypt(ciphertext)
    recovered_text = unpad(recovered_text, 16)
    recovered_text = recovered_text.decode('utf-8')
    print("recovered text: ", recovered_text)


def demo_AES_CBC(text):
    print("AES demo with CBC mode")
    print("text plaintext: ", text)

    key = get_random_bytes(32)
    initial_value = get_random_bytes(16)

    # Create a cipher object with the key and initial value
    cipher = AES.new(key, AES.MODE_CBC, initial_value)
    text = text.encode('utf-8')

    # Pad the text with bytes
    text = pad(text, 16)
    ciphertext = cipher.encrypt(text)
    print("text ciphertext: ", ciphertext.hex())

    # Create new cipher to decrypt cipher text for user 2
    new_cipher = AES.new(key, AES.MODE_CBC, initial_value)
    recovered_text = new_cipher.decrypt(ciphertext)
    recovered_text = unpad(recovered_text, 16)
    recovered_text = recovered_text.decode('utf-8')
    print("recovered text: ", recovered_text)

text1 = "Hi there! This is a text message with short length"
text2 = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."

#demo_AES_ECB(text1)
#demo_AES_CBC(text1)

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
                    run_AES_ECB(text)
                else:
                    run_AES_CBC(text)
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

    ax.set_title('Comparison in Runtime of AES modes and text length')
    ax.set_xlabel('Text Length (characters)')
    ax.set_ylabel('Runtime (s)')
    ax.set_xticks([i + bar_width / 2 for i in index])
    ax.set_xticklabels(text_lengths)
    ax.legend()

    plt.tight_layout()
    plt.show()


benchmark_lengths()