from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()


password = "Admin@123456"

hashed = password_hash.hash(password)


print()
print("======================================")
print("ADMIN PASSWORD")
print("======================================")
print(password)

print()
print("ARGON2 HASH")
print("======================================")
print(hashed)
print()