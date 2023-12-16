from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
def demo_signature_RSA():
    message = b"Test message 1234567890"
    key = RSA.generate(2048)

    # Private key is used for creating the signature and public key is used for verification
    private_key = key
    public_key = key.public_key()

    # Create a hash from the document
    hash = SHA256.new(message)

    # Create signature using hash and private_key
    signature = pkcs1_15.new(private_key).sign(hash)

    print("Signature for message ", message, " is: ", signature.hex())
    try:
        pkcs1_15.new(public_key).verify(hash, signature)
        print("The signature is valid")
    except (ValueError, TypeError):
        print("The signature is not valid")

    # Attempt to verify signature if message and hash are slightly altered
    message2 = b"Test message 12345678900"
    hash2 = SHA256.new(message2)
    print("Trying with a new message")
    try:
        pkcs1_15.new(public_key).verify(hash2, signature)
        print("The signature is valid")
    except (ValueError, TypeError):
        print("The signature is not valid")

    newHash = SHA256.new(message)
    print("Signature for message ", message, " is: ", signature.hex())
    try:
        pkcs1_15.new(public_key).verify(newHash, signature)
        print("The signature is valid")
    except (ValueError, TypeError):
        print("The signature is not valid")

demo_signature_RSA()