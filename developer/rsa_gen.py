#!/usr/bin/env python3

# Script to generate initial asymmetric keys
# Public key <rsa.pub> can be given out
# KEEP private key <rsa> to yourself! Necessary to decrypt!
# Usage: python3 rsa_gen.py

from Crypto.PublicKey import RSA

def generate_keys():
	# Generate public key
	keyPair = RSA.generate(4096)
	pubKey = keyPair.publickey()
	# Create pem files
	pubKeyPEM = pubKey.exportKey()
	privKeyPEM = keyPair.exportKey()
	# Make it readable
	privateKey = privKeyPEM.decode('ascii')
	publicKey = pubKeyPEM.decode('ascii')
	# Write to files
	with open('rsa.pub', 'w') as f: f.write(publicKey)
	with open('rsa', 'w') as f: f.write(privateKey)

generate_keys()