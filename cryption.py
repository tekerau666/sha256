import hashlib


def hash_data_sha256(data):
    sha256 = hashlib.sha256()
    sha256.update(data.encode('utf-8'))
    if data == 'ошибочный':
        data = 'пришел ошибочный текст'
    return sha256.hexdigest(), data


def check_data_sha256(data_recv, data):
    sha256 = hashlib.sha256()
    sha256.update(data.encode('utf-8'))
    hash_text = sha256.hexdigest()
    if hash_text == data_recv:
        return data
    else:
        return 'Сообщение подверглось изменению'
