from sympy import randprime, mod_inverse


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

    key1, key2 = diffie_hellman_method(prime, primitive_root, private_key_A, private_key_B)
    print("key 1 is: ", key1)
    print("key 2 is: ", key2)
    print("True/false key 1 is equal to key 2: ", key1 == key2)


runnerq1a()



def is_coprime(a, b):
    while b != 0:
        a, b = b, a % b
    return a == 1


# Generate the keys
def RSA_key_generate(e=None):   # e is optional
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
    return (e, n), (d, n)


# Encrypt the message
def RSA_encrypt(m, ke):
    e, n = ke
    c = pow(m, e, n)    # Ciphertext c = m^e mod n
    return c


# Decrypt the message
def RSA_decrypt(c, kd):
    d, n = kd
    m = pow(c, d, n)    # Message m = c^d mod n
    return m


def message_to_int(message):
    return int.from_bytes(message.encode(), 'big')

def int_to_message(message_int):
    return message_int.to_bytes((message_int.bit_length() + 7) // 8, 'big').decode()


# Test function
def test(message, e=None):
    public_key, private_key = RSA_key_generate(e)
    print(f"Public key: {public_key}")
    print(f"Private key: {private_key}")

    message_int = message_to_int(message)
    ciphertext = RSA_encrypt(message_int, public_key)
    print(f"Encrypted message: {ciphertext}")

    decrypted_message_int = RSA_decrypt(ciphertext, private_key)
    decrypted_message = int_to_message(decrypted_message_int)
    print(f"Decrypted message: {decrypted_message}")

    assert decrypted_message == message, "The decrypted message and original message do not match"


# Run Test
test_message = "123456789"
test(test_message)

test_message = "hello world!"
test(test_message)