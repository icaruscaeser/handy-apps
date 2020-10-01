#Author : Icarus Caeser
#File created on 29 Sep 2020 8:16 AM

import os
import hashlib
from cryptography.hazmat.primitives.ciphers import algorithms, modes, Cipher
from cryptography.hazmat.primitives import padding
import argparse


def encrypt_file(path_of_file, password=None, key=None):

    """This method is used to encrypt a file
        params: path_of_file --> path of file to be encrypted,
                password --> password with which the key has to be generated, If the password is none, name of the file including the extension will be used as password
                key --> key with which the file has to be encrypted, if the key string is empty, password will be used to generate the key
        returns: path of encrypted file
    """

    file_name = os.path.basename(path_of_file)
    dir_path = os.path.dirname(path_of_file)

    # if the key is none, use the name of file(not path of file) as key
    if key is None:
        if password is None:
            password = file_name
        hash_obj = hashlib.sha256()
        hash_obj.update(bytes(password, 'utf-8'))
        key = hash_obj.digest()
        print(' The password is {0} The key is '.format( password) + str(key))

    cipher = Cipher(algorithms.AES(key), modes.ECB())
    encryptor = cipher.encryptor()

    with open(path_of_file, 'rb') as file:
        data = file.read()
        #pad the data
        print(data)
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()
        print(padded_data)
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        print(encrypted_data)

    encrpyted_file_path = os.path.join(dir_path, file_name+'.enc')

    with open(encrpyted_file_path, 'wb+') as encrypted_file:
        encrypted_file.write(encrypted_data)

    return encrpyted_file_path

def decrypt_file(path_of_file, password=None, key=None):

    """This method is used to decrypt a file that was encrypted using the above method
        params: path_of_file --> path of file to be encrypted,
                password --> password with which the key has to be generated, If the password is none, name of the file including the extension will be used as password
                key --> key with which the file has to be decrypted, if the key string is empty, password will be used to generate the key
        returns: path of decrypted file
    """

    file_name = os.path.basename(path_of_file).replace('.enc', '')
    dir_path = os.path.dirname(path_of_file)
    print(file_name)

    # if the key is none, use the name of file(not path of file) as key
    if key is None:
        if password is None:
            password = file_name
        hash_obj = hashlib.sha256()
        hash_obj.update(bytes(password, 'utf-8'))
        key = hash_obj.digest()
        print(' The password is {0} The key is '.format( password) + str(key))

    cipher = Cipher(algorithms.AES(key), modes.ECB())
    decryptor = cipher.decryptor()


    with open(path_of_file, 'rb') as file:
        data = file.read()
        print(data)

        #decrypt the data
        decrypted_data = decryptor.update(data) + decryptor.finalize()
        #unpad the data
        unpadder = padding.PKCS7(128).unpadder()
        decrypted_data = unpadder.update(decrypted_data) + unpadder.finalize()

    decrypted_file_path = os.path.join(dir_path, file_name + '.dec')
    print(decrypted_data)

    with open(decrypted_file_path, 'wb+') as decrypted_file:
        decrypted_file.write(decrypted_data)

    return decrypted_file_path



if __name__ ==  '__main__':

    arg_parser = argparse.ArgumentParser(description='Encrypt/Decrypt the given file')

    arg_parser.add_argument('operation', type=str, help='cryptographic operation that has to be performed.', choices=['encrypt', 'decrypt'])
    arg_parser.add_argument('file', type=str, help='path of file on which cryptography has to be performed')

    arg_parser.add_argument('--nodecextension', action='store_true')
    args = arg_parser.parse_args()

    file_path = args.file
    if not os.path.exists(file_path):
        print("file path does not exist")
        exit(1)

    if not os.path.isfile(file_path):
        print("Path specified is not that of a file")
        exit(1)

    if args.operation == 'encrypt':
        encrypt_file(file_path)

    elif args.operation == 'decrypt':
        decrypted_file = decrypt_file(file_path)
        if args.nodecextension:
            print('removing dec extension')
            os.rename(decrypted_file, decrypted_file[:-4])