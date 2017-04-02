import ed25519
import os


def generate_pub_private_key():
    signing_key, verifying_key = ed25519.create_keypair(entropy=os.urandom)
    open("pns", "wb").write(signing_key.to_seed())
    open("pns.pub", "wb").write(verifying_key.to_ascii(encoding="hex"))


def compute_signature(page_path, page_id):
    path = os.path.join(page_path, page_id)
    page_data = open(path, 'r').read()
    seed = open("pns", "rb").read()
    signing_key = ed25519.SigningKey(seed)
    signature = signing_key.sign(str.encode(page_data), encoding="base64")
    return signature


def verify_signature(signature, page_path, page_id):
    path = os.path.join(page_path, page_id)
    page_data = open(path, 'r').read()
    vkey_hex = open("pns.pub", "rb").read()
    print(vkey_hex)
    verifying_key = ed25519.VerifyingKey(vkey_hex, encoding="hex")
    try:
        verifying_key.verify(signature, str.encode(page_data), encoding="base64")
        return "Success"
    except ed25519.BadSignatureError:
        return "Failed"

