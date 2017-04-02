import ed25519
import os

SIG_ABS_PATH = os.path.dirname(os.path.realpath('__file__'))

def generate_pub_private_key():
    signing_key, verifying_key = ed25519.create_keypair(entropy=os.urandom)
    open("pns", "wb").write(signing_key.to_seed())
    open("pns.pub", "wb").write(verifying_key.to_ascii(encoding="hex"))


def compute_signature(page_path, page_id):
    path = os.path.join(page_path, page_id)
    page_data = open(path, 'r').read()
    priv_key_path = os.path.join(SIG_ABS_PATH, "..", "pns")
    seed = open(priv_key_path, "rb").read()
    signing_key = ed25519.SigningKey(seed)
    signature = signing_key.sign(str.encode(page_data), encoding="base64")
    return signature


def verify_signature(signature, page_path, page_id):
    path = os.path.join(page_path, page_id)
    page_data = open(path, 'r').read()
    pub_key_path = os.path.join(SIG_ABS_PATH, "..", "pns.pub")
    vkey_hex = open(pub_key_path, "rb").read()
    verifying_key = ed25519.VerifyingKey(vkey_hex, encoding="hex")
    try:
        verifying_key.verify(signature, str.encode(page_data), encoding="base64")
        return "Success"
    except ed25519.BadSignatureError:
        return "Failed"
