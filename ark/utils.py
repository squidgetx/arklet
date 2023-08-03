from typing import Tuple

import secrets

BETANUMERIC = "0123456789bcdfghjkmnpqrstvwxz"


def noid_check_digit(noid: str) -> str:
    """Calculate the check digit for an ARK.

    See: https://metacpan.org/dist/Noid/view/noid#NOID-CHECK-DIGIT-ALGORITHM
    """
    total = 0
    for pos, char in enumerate(noid, start=1):
        score = BETANUMERIC.find(char)
        if score > 0:
            total += pos * score
    remainder = total % 29  # 29 == len(BETANUMERIC)
    return BETANUMERIC[remainder]  # IndexError may be long ARK


def generate_noid(length: int) -> str:
    return "".join(secrets.choice(BETANUMERIC) for _ in range(length))


def parse_ark(ark: str) -> Tuple[str, int, str]:
    parts = ark.split("ark:")
    if len(parts) != 2:
        raise ValueError("Not a valid ARK")
    nma, ark = parts
    ark = ark.lstrip("/")
    parts = ark.split("/")
    if len(parts) < 2:
        raise ValueError("Not a valid ARK")
    naan = parts[0]
    identifier = '/'.join(parts[1:])
    try:
        naan_int = int(naan)
    except ValueError:
        raise ValueError("ARK NAAN must be an integer")

    return nma, naan_int, identifier

def parse_ark_lookup(ark: str) -> str:

    _, naan_int, identifier = parse_ark(ark)
    return f"{naan_int}/{identifier}"


def gen_prefixes(ark: str):
    parts = ark.split('/')
    for i in range(1, len(parts)):
        yield '/'.join(parts[:-i])
