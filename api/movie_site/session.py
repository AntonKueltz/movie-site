from datetime import datetime, timedelta
from json import dumps, loads

from fastecdsa.curve import W25519
from fastecdsa.ecdsa import sign, verify
from fastecdsa.keys import gen_keypair

DELIMITER = "|"
secret_key, public_key = gen_keypair(W25519)


def generate_user_session_token(user_id: int) -> str:
    data = {"id": user_id, "ts": datetime.utcnow().timestamp()}
    data = dumps(data)
    r, s = sign(data, secret_key, W25519)
    return f"{r}{DELIMITER}{s}{DELIMITER}{data}"


def get_user_id_from_token(token: str) -> int | None:
    r, s, data = token.split(DELIMITER)
    r = int(r)
    s = int(s)

    if not verify((r, s), data, public_key, W25519):
        return None
    
    data = loads(data)

    if datetime.fromtimestamp(data["ts"]) + timedelta(days=1) < datetime.utcnow():
        return None
    
    return data.get("id")
