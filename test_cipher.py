from cipher import AESCipher

aes = AESCipher(b'helloworld')


def test_all():
    assert aes.decrypt(aes.encrypt('hello world'.encode())) == b'hello world'


def test_file():
    with open('gui.py', 'rb') as f:
        data = f.read()

        assert data == aes.decrypt(aes.encrypt(data))
