import hashlib

def HashPass(pwd):
    md5 = hashlib.md5()
    md5.update(pwd.encode())
    result = md5.hexdigest()
    return result