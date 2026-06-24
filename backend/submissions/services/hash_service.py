import json
import hashlib


def normalize_submission_data(data):
    """
    Converts submitted data into a stable JSON string.
    Sorting keys is important so the same data always generates the same hash.
    """
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def generate_submission_hash(data):
    """
    Generates a SHA-256 hash from normalized submitted data.
    Returns a blockchain-friendly 0x-prefixed hash.
    """
    normalized_data = normalize_submission_data(data)
    hash_value = hashlib.sha256(normalized_data.encode("utf-8")).hexdigest()
    return f"0x{hash_value}"