import MySQLdb
from Crypto.Cipher import AES
import os

# Database connection information
HOST = "localhost"
USER = "root"
PASSWORD = "root"
DATABASE = "mini_project"

# Database tables and columns
TABLES = {"Individuals": ["first_name", "last_name", "address_id"],
          "Addresses": ["street_address", "city", "state_id", "zip_code"],
          "Financial_Accounts": ["account_number", "routing_number"]}

# Generate a secure DEK
dek = os.urandom(32)

# Connect to the database
db = MySQLdb.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
cursor = db.cursor()

# Encrypt each table and its columns
for table_name, columns in TABLES.items():
    for column in columns:
        encrypt_query = f"UPDATE {table_name} SET {column} = AES_ENCRYPT({column}, %s)"
        cursor.execute(encrypt_query, (dek,))

# Store the DEK securely (replace with your secure storage method)
with open("dek.bin", "wb") as f:
    f.write(dek)

# Commit changes and close the connection
db.commit()
db.close()

print("All tables and columns encrypted successfully.")
print("DEK stored in 'dek.bin'. Please keep it safe.")
