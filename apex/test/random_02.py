import random
import string
import secrets

letters_set = string.ascii_lowercase + string.digits * 4

# print (letters_set)
random_list = random.sample(letters_set, 32)
# print (random_list)
result = ''.join(random_list)
print ('keyring_' + result)

# key = secrets.token_hex(16)
key = secrets.token_urlsafe(16)
print ('keyring_' + key)

