from secrets import choice
from hashlib import pbkdf2_hmac as pbkdf2
from encoding.sha256 import sha256


def get_words():
    with open("english.txt", "r") as words_file:
        words = [word.strip() for word in words_file.readlines()]
    return words

def get_bin_from_hex(hex_str: str):
    bin_str = ""
    for symb in hex_str:
        bin_str += bin(int(symb, 16))[2:].zfill(4)
    return bin_str

def get_mnemonic(words_count:int = 24):
    def get_entropy(entropy_bit_length: int):
        alphabet = "01"
        entropy = "".join([choice(alphabet) for _ in range(entropy_bit_length)])
        return entropy

    def get_checksum(entropy: bytes, entropy_length: int):
        checksum_bit_length = round(entropy_length / 32 + 0.5)
        print(f"Entropy hex: {hex(int(entropy, 2))}")
        entropy_hash = sha256(int(entropy, 2).to_bytes(length=(entropy_length + 7) // 8, byteorder="big"))
        hash_bin = get_bin_from_hex(entropy_hash)
        print(f"Entropy hash: {entropy_hash}")
        print(f"Hash bin: {hash_bin}")
        checksum = hash_bin[2:2 + checksum_bit_length]
        return checksum

    def entropy_to_mnemonic(entropy, entropy_length):
        checksum = get_checksum(entropy, entropy_length)
        print(checksum)
        complete_entropy = entropy + checksum

        words = get_words()
        mnemonic = list()
        for i in range(0, len(complete_entropy), 11):
            bits = complete_entropy[i:i + 11]
            word_n = int(bits, 2)
            mnemonic.append(words[word_n])
        return mnemonic
    
    assert words_count % 3 == 0
    bit_length = int(words_count * 32 * 11 / 33) # 12 15 18 21 24
    entropy = get_entropy(entropy_bit_length=bit_length)
    print(f"Entropy length = {len(entropy)}")
    print(f"Entropy bin: {entropy}")
    mnemonic = " ".join(entropy_to_mnemonic(entropy, bit_length))
    return mnemonic

def get_seed(mnemonic: str):
    password = bytes(mnemonic, encoding="utf-8")
    salt = bytes("", encoding="utf-8")
    iterations = 2048
    keylength = 32
    seed = pbkdf2(hash_name="sha512", salt=salt, password=password, iterations=iterations, dklen=keylength)
    return seed.hex()

def check_validness(mnemonic: str):
    words = get_words()

    mnemonic_words = mnemonic.split()
    mnemonic_bit = "".join([bin(words.index(word))[2:].zfill(11) for word in mnemonic_words])

    words_count = len(mnemonic_words)
    bit_length = words_count * 11
    checksum_length = bit_length // 32
    entropy_length = bit_length - checksum_length

    entropy, checksum = mnemonic_bit[:entropy_length], mnemonic_bit[entropy_length:]
    entropy_hash = sha256(int(entropy, 2).to_bytes(length=(entropy_length + 7) // 8, byteorder="big"))
    hash_bin = get_bin_from_hex(entropy_hash)

    return hash_bin.startswith(checksum)



mnemonic = get_mnemonic(12)
print(f"Mnemonic: {mnemonic}")
seed = get_seed(mnemonic)
print(f"Seed: {seed}")
print(f"Seed length = {len(seed)}")
print("Is valid") if check_validness(mnemonic) else print("Not valid")