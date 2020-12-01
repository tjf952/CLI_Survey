#!/usr/bin/env python3

# Script to decrypt data for developer
# Usage: python3 <file-to-decrypt>

import sys
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA

filename = sys.argv[1]

def decrypt_file(filename):
	# Get information from bin file
	nonce, tag, rsa_key, ciphertext = None, None, None, None
	with open(filename, 'rb') as f:
		nonce = f.read(16)
		tag = f.read(16)
		aes_key = f.read(512)
		ciphertext = f.read()
	# Decrypt rsa encrypted aes key
	rsa_key = RSA.importKey(open('rsa').read())
	rsa_cipher = PKCS1_OAEP.new(rsa_key)
	aes_key = rsa_cipher.decrypt(aes_key)
	# Decrypt message
	aes_cipher = AES.new(aes_key, AES.MODE_EAX, nonce)
	data = aes_cipher.decrypt_and_verify(ciphertext, tag)
	return data

data = decrypt_file(filename).decode()
print(data)