import base64


def encode_list_to_base64(string_list) -> str:
    combined_str = '|'.join(string_list)
    byte_data = combined_str.encode('utf-8')
    base64_bytes = base64.b64encode(byte_data)
    base64_str = base64_bytes.decode('utf-8')
    return base64_str


def decode_base64_to_list(base64_str):
    base64_bytes = base64_str.encode('utf-8')
    byte_data = base64.b64decode(base64_bytes)
    combined_str = byte_data.decode('utf-8')
    string_list = combined_str.split('|')
    return string_list
