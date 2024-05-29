#!/usr/bin/env python3
"""
Main file
"""

hash_password = __import__('encrypt_password').hash_password
is_valid = __import__('encrypt_password').is_valid

password = "MyAmazingPasswrd"
false_pwd = 'djvdjfdj'
encrypted_password = hash_password(password)
print(encrypted_password)
print(is_valid(encrypted_password, false_pwd))