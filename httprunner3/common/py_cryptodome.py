import base64
from Cryptodome.Cipher import AES


class CryptoDome:

    def __init__(self):
        self.key = 'd8cg8gVakEq9Agup'

    def aes_encrypt(self, enc_data):
        """
        AES加密
        :param enc_data: 加密数据
        :return:
        """
        aes_ = AES.new(str.encode(self.key), AES.MODE_ECB)
        add_data = str.encode(enc_data)
        #   补足为16的倍数
        while len(add_data) % 16 != 0:
            add_data += b'\x00'
        encrypt_aes = aes_.encrypt(add_data)
        encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')
        return encrypted_text

    def aes_decrypt(self, dec_data):
        """
        AES解密
        :param dec_data: 解密数据
        :return:
        """
        aes_ = AES.new(str.encode(self.key), AES.MODE_ECB)
        base64_decrypted = base64.decodebytes(dec_data.encode(encoding='utf-8'))
        decrypted_text = str(aes_.decrypt(base64_decrypted), encoding='utf-8')
        return decrypted_text


if __name__ == '__main__':
    #   加解密
    aes = CryptoDome()
    secret_str = aes.aes_encrypt('zxy123456')
    decrypt_str = aes.aes_decrypt(secret_str)
    print(f'secret_str加密后为: {secret_str}decrypt_str解密后为: {decrypt_str}')
