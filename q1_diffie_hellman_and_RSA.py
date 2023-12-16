from sympy import randprime, mod_inverse
from pylfsr import LFSR
import time, matplotlib.pyplot as plt
# Efficient modular exponentiation
def power(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result
def diffie_hellman_method(prime, primitive_root, private_key_A, private_key_B):
    A = power(primitive_root, private_key_A, prime)
    B = power(primitive_root, private_key_B, prime)
    shared_secret_A = power(B, private_key_A, prime)
    shared_secret_B = power(A, private_key_B, prime)
    return shared_secret_A, shared_secret_B
def runnerq1a():
    prime = 102188617217178804476387977160129334431745945009730065519337094992129677228373
    primitive_root = 2
    private_key_A = 11
    private_key_B = 23
    print("User 1 private key is: ", private_key_A)
    print("User 2 private key is: ", private_key_B)
    key1, key2 = diffie_hellman_method(prime, primitive_root, private_key_A, private_key_B)
    print("key 1 is: ", key1)
    print("key 2 is: ", key2)
    print("True/false key 1 is equal to key 2: ", key1 == key2)
#runnerq1a()

def is_coprime(a, b):
    while b != 0:
        a, b = b, a % b
    return a == 1
class RSA_Public_Key:
    def __init__(self, e, n):
        self.e = e
        self.n = n
class RSA_Private_Key:
    def __init__(self, d, n):
        self.d = d
        self.n = n
# Generate the keys
def RSA_key_generate(e=3):   # e is optional
    # Generate two random prime integers p and q
    p = randprime(0, 2 ** 512)
    q = randprime(0, 2 ** 512)
    while q == p:
        q = randprime(0, 2 ** 512)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    if e is None or not is_coprime(e, phi_n) or e >= phi_n:
        e = 65537   # default value for e
    # Calculate the modular inverse of e
    d = mod_inverse(e, phi_n)
    # Output public and private key (e,n) and (d,n)
    public_key = RSA_Public_Key(e,n)
    private_key = RSA_Private_Key(d,n)
    return public_key, private_key
# Encrypt the message
def RSA_encrypt(m, e, n):
    c = power(m, e, n)    # Ciphertext c = m^e mod n
    return c
# Decrypt the message
def RSA_decrypt(c, d, n):
    m = power(c, d, n)    # Message m = c^d mod n
    return m
def message_to_int(message):
    return int.from_bytes(message.encode(), 'big')
def int_to_message(message_int):
    return message_int.to_bytes((message_int.bit_length() + 7) // 8, 'big').decode()
def runnerq1c():
    #use LFSR to generate a key and share it with user 2 using RSA
    feedback_polynomial = [1, 3, 4, 7]
    seed = [1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0]
    L = LFSR(initstate=seed, fpoly=feedback_polynomial)
    lfsr_key = L.runKCycle(32)
    public_RSA_key, private_RSA_key = RSA_key_generate()

    int_key = lfsr_key.tolist()
    message = ''.join(map(str, int_key))
    print("Plaintext: ", message)
    message = message_to_int(message)
    ciphertext = RSA_encrypt(message, public_RSA_key.e, public_RSA_key.n)
    print("Ciphertext: ", ciphertext)

    #on user 2's side: decrypt RSA message
    decrypted_message_int = RSA_decrypt(ciphertext, private_RSA_key.d, private_RSA_key.n)
    print("decrypted message int: ", decrypted_message_int)
    decrypted_message = int_to_message(decrypted_message_int)
    print(f"Decrypted message: {decrypted_message}")
runnerq1c()

def run_diffie_hellman():
    prime = 102188617217178804476387977160129334431745945009730065519337094992129677228373
    primitive_root = 2
    private_key_A = 11
    private_key_B = 23
    key1, key2 = diffie_hellman_method(prime, primitive_root, private_key_A, private_key_B)
def benchmark_diffie_vs_rsa():
    iterations = [10, 100, 1000]
    dh_runtimes = {}
    rsa_runtimes = {}
    for num in iterations:
        start = time.time()
        for i in range(num):
            run_diffie_hellman()
        elapsed = time.time() - start
        dh_runtimes[num] = elapsed
        print("diffie hellman method iteration finished")
        start = time.time()
        for i in range(num):
            RSA_key_generate()
        elapsed = time.time() - start
        rsa_runtimes[num] = elapsed
        print("rsa method iteration finished")
    print(rsa_runtimes)
    print(dh_runtimes)
    bar_width = 0.35
    text_lengths = list(dh_runtimes.keys())
    index = list(range(len(text_lengths)))
    dh_y = [dh_runtimes[length] for length in dh_runtimes]
    rsa_y = [rsa_runtimes[length] for length in rsa_runtimes]
    fig, ax = plt.subplots()
    dh_bars = ax.bar(index, dh_y, bar_width, label='Diffie-Hellman')
    rsa_bars = ax.bar([i + bar_width for i in index], rsa_y, bar_width, label='RSA', color='red')
    ax.set_title('Runtimes of Diffie-Hellman and RSA Key Generation')
    ax.set_xlabel('Number of keys generated')
    ax.set_ylabel('Runtime (s)')
    ax.set_xticks([i + bar_width / 2 for i in index])
    ax.set_xticklabels(text_lengths)
    ax.legend()
    ax.set_yscale('log')
    plt.tight_layout()
    plt.show()
benchmark_diffie_vs_rsa()