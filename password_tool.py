# ============================================================
#       HASHED PASSWORD CRACKER & SECURE AUTH TOOL
#              Written By Thamizh Selvan
#         Cybersecurity & Ethical Hacking — BIA
# ============================================================

import hashlib
import os
import json
import itertools
import string
import random

# ============================================================
# GLOBAL VARIABLES — AI Auto Hash Flow
# ============================================================
last_generated_hash = ""
last_used_algorithm = ""
failed_attempts = {}
MAX_ATTEMPTS = 5

# ============================================================
# BUILT-IN WORDLIST — 100 Common Passwords
# ============================================================
BUILTIN_WORDLIST = [
    "password", "123456", "12345678", "123456789",
    "1234567890", "password1", "password123",
    "admin", "admin123", "admin@123",
    "hello", "welcome", "letmein", "monkey",
    "dragon", "master", "sunshine", "princess",
    "qwerty", "football", "shadow", "superman",
    "michael", "login", "iloveyou", "test",
    "pass", "root", "user", "guest", "secret",
    "111111", "222222", "333333", "444444",
    "555555", "666666", "777777", "888888",
    "999999", "000000", "112233", "121212",
    "696969", "654321", "987654321",
    "abc123", "abc@123", "abcd1234", "abcdef",
    "qwerty123", "qwerty@123", "azerty",
    "zxcvbn", "asdfgh", "qazwsx",
    "jessica", "charlie", "donald",
    "thomas", "jordan", "harley", "ranger",
    "daniel", "andrew", "george", "joshua",
    "hunter", "robert", "buster", "soccer",
    "kali", "toor", "kali123", "root123",
    "hacker", "hacking", "hack", "pentest",
    "metasploit", "nmap", "linux", "ubuntu",
    "india123", "india@123", "indian",
    "krishna", "ganesh", "shiva", "allah",
    "welcome1", "welcome@1", "welcome123",
    "pass@123", "pass@1234", "password@1",
    "admin@1234", "admin1234", "system",
    "1q2w3e4r", "1qaz2wsx", "q1w2e3r4",
    "qwertyuiop", "asdfghjkl", "zxcvbnm",
    "1234qwer", "qwer1234", "pass1234",
    "letmein1", "trustno1", "starwars",
    "batman", "superman1", "spiderman",
    "pokemon", "naruto", "onepiece",
    "changeme", "change123", "temp123",
    "default", "test123", "demo123",
]

# ============================================================
# PART 2 — HASH FUNCTION
# ============================================================
def hash_password(password, algorithm="sha256"):
    if algorithm == "md5":
        return hashlib.md5(password.encode()).hexdigest()
    elif algorithm == "sha1":
        return hashlib.sha1(password.encode()).hexdigest()
    elif algorithm == "sha256":
        return hashlib.sha256(password.encode()).hexdigest()
    elif algorithm == "sha512":
        return hashlib.sha512(password.encode()).hexdigest()
    else:
        return "Invalid algorithm!"

# ============================================================
# PART 3 — DICTIONARY ATTACK (with rockyou.txt support)
# ============================================================
def dictionary_attack(target_hash, algorithm="sha256"):
    print("\n[*] DICTIONARY ATTACK")
    print("-" * 50)
    print("Choose wordlist:")
    print("1. Built-in wordlist (100 common passwords)")
    print("2. rockyou.txt    (14 million real passwords)")
    print("3. Custom wordlist (your own file)")
    wordlist_choice = input("\nEnter choice (1-3): ")

    if wordlist_choice == "1":
        wordlist = BUILTIN_WORDLIST
        print(f"\n[*] Using built-in wordlist ({len(wordlist)} passwords)")
        print(f"[*] Starting Dictionary Attack...\n")

        for word in wordlist:
            attempt = hash_password(word, algorithm)
            print(f"    Trying: {word}")
            if attempt == target_hash:
                print(f"\n[+] PASSWORD CRACKED!")
                print(f"[+] Password is: {word}")
                return word

        print("\n[-] Password not found in built-in wordlist!")
        return None

    elif wordlist_choice == "2":
        rockyou_paths = [
            "/usr/share/wordlists/rockyou.txt",
            "rockyou.txt",
            "C:\\rockyou.txt",
        ]
        rockyou_path = None
        for path in rockyou_paths:
            if os.path.exists(path):
                rockyou_path = path
                break

        if not rockyou_path:
            print("\n[-] rockyou.txt not found!")
            print("[*] In Kali Linux run:")
            print("    sudo gunzip /usr/share/wordlists/rockyou.txt.gz")
            print("[*] Or copy rockyou.txt to this tool's folder.")
            return None

        print(f"\n[*] Found rockyou.txt at: {rockyou_path}")
        print(f"[*] Starting attack — Press Ctrl+C to stop\n")

        tried = 0
        try:
            with open(rockyou_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    word = line.strip()
                    if not word:
                        continue
                    tried += 1
                    attempt = hash_password(word, algorithm)
                    if tried % 100000 == 0:
                        print(f"    [*] Tried {tried:,} passwords...")
                    if attempt == target_hash:
                        print(f"\n[+] PASSWORD CRACKED!")
                        print(f"[+] Password is: {word}")
                        print(f"[+] Found after {tried:,} attempts!")
                        return word
        except KeyboardInterrupt:
            print(f"\n[!] Stopped after {tried:,} attempts!")
            return None

        print(f"\n[-] Not found in rockyou.txt! Tried {tried:,} passwords.")
        return None

    elif wordlist_choice == "3":
        custom_path = input("\nEnter full path to your wordlist file: ")
        if not os.path.exists(custom_path):
            print(f"\n[-] File not found: {custom_path}")
            return None

        print(f"\n[*] Using custom wordlist: {custom_path}")
        tried = 0
        try:
            with open(custom_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    word = line.strip()
                    if not word:
                        continue
                    tried += 1
                    attempt = hash_password(word, algorithm)
                    if tried % 10000 == 0:
                        print(f"    [*] Tried {tried:,} passwords...")
                    if attempt == target_hash:
                        print(f"\n[+] PASSWORD CRACKED!")
                        print(f"[+] Password is: {word}")
                        print(f"[+] Found after {tried:,} attempts!")
                        return word
        except KeyboardInterrupt:
            print(f"\n[!] Stopped after {tried:,} attempts!")
            return None

        print(f"\n[-] Not found! Tried {tried:,} passwords.")
        return None

    else:
        print("\n[-] Invalid choice!")
        return None

# ============================================================
# PART 4 — BRUTE FORCE ATTACK
# ============================================================
def brute_force_attack(target_hash, algorithm="sha256", max_length=4):
    chars = string.ascii_lowercase + string.digits
    print(f"\n[*] Starting Brute Force Attack...")
    print(f"[*] Trying all combinations up to {max_length} characters...")
    print(f"[*] Using: a-z and 0-9\n")

    for length in range(1, max_length + 1):
        print(f"[*] Trying length {length}...")
        for combo in itertools.product(chars, repeat=length):
            attempt = "".join(combo)
            hashed = hash_password(attempt, algorithm)
            if hashed == target_hash:
                print(f"\n[+] PASSWORD CRACKED!")
                print(f"[+] Password is: {attempt}")
                return attempt

    print("\n[-] Password not found by brute force!")
    return None

# ============================================================
# PART 5 — RAINBOW TABLE (with rockyou.txt support)
# ============================================================
def rainbow_table_attack(target_hash, algorithm="sha256"):
    print("\n[*] RAINBOW TABLE ATTACK")
    print("-" * 50)
    print("Choose wordlist to build table from:")
    print("1. Built-in wordlist (100 passwords — instant)")
    print("2. rockyou.txt    (14 million — takes time)")
    print("3. Custom wordlist")
    wordlist_choice = input("\nEnter choice (1-3): ")

    rainbow_table = {}

    if wordlist_choice == "1":
        print(f"\n[*] Building Rainbow Table from built-in wordlist...")
        for word in BUILTIN_WORDLIST:
            hashed = hash_password(word, algorithm)
            rainbow_table[hashed] = word
        print(f"[*] Table built with {len(rainbow_table)} entries!")

    elif wordlist_choice == "2":
        rockyou_paths = [
            "/usr/share/wordlists/rockyou.txt",
            "rockyou.txt",
            "C:\\rockyou.txt",
        ]
        rockyou_path = None
        for path in rockyou_paths:
            if os.path.exists(path):
                rockyou_path = path
                break

        if not rockyou_path:
            print("\n[-] rockyou.txt not found!")
            print("[*] In Kali: sudo gunzip /usr/share/wordlists/rockyou.txt.gz")
            return None

        print(f"\n[*] Building Rainbow Table from rockyou.txt...")
        print(f"[*] This may take a few minutes — Press Ctrl+C to stop\n")
        count = 0
        try:
            with open(rockyou_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    word = line.strip()
                    if not word:
                        continue
                    hashed = hash_password(word, algorithm)
                    rainbow_table[hashed] = word
                    count += 1
                    if count % 100000 == 0:
                        print(f"    [*] Built {count:,} entries...")
        except KeyboardInterrupt:
            print(f"\n[!] Stopped at {count:,} entries!")

        print(f"\n[*] Rainbow Table built with {count:,} entries!")

    elif wordlist_choice == "3":
        custom_path = input("\nEnter full path to your wordlist: ")
        if not os.path.exists(custom_path):
            print(f"\n[-] File not found!")
            return None
        count = 0
        with open(custom_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                word = line.strip()
                if not word:
                    continue
                hashed = hash_password(word, algorithm)
                rainbow_table[hashed] = word
                count += 1
        print(f"[*] Table built with {count:,} entries!")
    else:
        print("\n[-] Invalid choice!")
        return None

    print(f"\n[*] Looking up target hash...")
    if target_hash in rainbow_table:
        print(f"\n[+] PASSWORD FOUND IN RAINBOW TABLE!")
        print(f"[+] Password is: {rainbow_table[target_hash]}")
        return rainbow_table[target_hash]
    else:
        print(f"\n[-] Hash not found in rainbow table!")
        return None

# ============================================================
# PART 6 — SECURE STORAGE
# ============================================================
def store_user(username, password, algorithm="sha256"):
    salt = os.urandom(16).hex()
    salted_password = salt + password
    hashed = hash_password(salted_password, algorithm)
    user_data = {
        "username": username,
        "salt": salt,
        "hash": hashed,
        "algorithm": algorithm
    }
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = []

    for user in users:
        if user["username"] == username:
            print(f"\n[-] Username '{username}' already exists!")
            return False

    users.append(user_data)
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

    print(f"\n[+] User '{username}' stored successfully!")
    print(f"[+] Salt     : {salt}")
    print(f"[+] Hash     : {hashed}")
    print(f"[+] Plaintext password is NEVER saved!")
    return True

# ============================================================
# PART 7 — AUTHENTICATION
# ============================================================
def authenticate(username, password):
    print(f"\n[*] Authenticating user '{username}'...")
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        print("\n[-] No users found! Please store a user first.")
        return False

    for user in users:
        if user["username"] == username:
            salt = user["salt"]
            stored_hash = user["hash"]
            algorithm = user["algorithm"]
            salted_attempt = salt + password
            attempt_hash = hash_password(salted_attempt, algorithm)
            if attempt_hash == stored_hash:
                print(f"\n[+] LOGIN SUCCESSFUL!")
                print(f"[+] Welcome, {username}!")
                return True
            else:
                print(f"\n[-] LOGIN FAILED!")
                print(f"[-] Incorrect password for '{username}'!")
                return False

    print(f"\n[-] User '{username}' not found!")
    return False

# ============================================================
# PART 9 — SHOW ALL USERS
# ============================================================
def show_all_users():
    print("\n[*] Fetching all stored users...")
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        print("\n[-] No users found!")
        return

    if len(users) == 0:
        print("\n[-] No users stored yet!")
        return

    print(f"\n[+] Total users stored: {len(users)}")
    print("-" * 60)
    for i, user in enumerate(users, 1):
        print(f"\n  User {i}:")
        print(f"  Username  : {user['username']}")
        print(f"  Algorithm : {user['algorithm'].upper()}")
        print(f"  Hash      : {user['hash'][:20]}...")
        print(f"  Salt      : {user['salt'][:10]}...")
    print("\n" + "-" * 60)
    print("[+] Plaintext passwords are never stored!")

# ============================================================
# PART 10 — DELETE USER
# ============================================================
def delete_user(username):
    print(f"\n[*] Looking for user '{username}'...")
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        print("\n[-] No users found!")
        return False

    user_found = False
    updated_users = []
    for user in users:
        if user["username"] == username:
            user_found = True
            print(f"\n[+] User '{username}' found!")
        else:
            updated_users.append(user)

    if not user_found:
        print(f"\n[-] User '{username}' not found!")
        return False

    confirm = input(f"\n[!] Are you sure you want to delete '{username}'? (yes/no): ")
    if confirm.lower() != "yes":
        print("\n[*] Deletion cancelled!")
        return False

    with open("users.json", "w") as f:
        json.dump(updated_users, f, indent=4)

    print(f"\n[+] User '{username}' deleted successfully!")
    print(f"[+] Remaining users: {len(updated_users)}")
    return True

# ============================================================
# PART 11 — CHANGE PASSWORD
# ============================================================
def change_password(username):
    print(f"\n[*] Looking for user '{username}'...")
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        print("\n[-] No users found!")
        return False

    for i, user in enumerate(users):
        if user["username"] == username:
            old_password = input("\nEnter your CURRENT password: ")
            old_salt = user["salt"]
            old_hash = hash_password(old_salt + old_password, user["algorithm"])

            if old_hash != user["hash"]:
                print("\n[-] Current password is WRONG! Change cancelled.")
                return False

            print("\n[+] Current password verified!")
            new_password = input("Enter your NEW password: ")
            confirm_password = input("Confirm your NEW password: ")

            if new_password != confirm_password:
                print("\n[-] Passwords do not match! Change cancelled.")
                return False

            if new_password == old_password:
                print("\n[-] New password same as old! Change cancelled.")
                return False

            new_salt = os.urandom(16).hex()
            new_hash = hash_password(new_salt + new_password, user["algorithm"])
            users[i]["salt"] = new_salt
            users[i]["hash"] = new_hash

            with open("users.json", "w") as f:
                json.dump(users, f, indent=4)

            print(f"\n[+] Password changed successfully for '{username}'!")
            return True

    print(f"\n[-] User '{username}' not found!")
    return False

# ============================================================
# PART 12 — EXPORT HASH REPORT
# ============================================================
def export_hash_report():
    print("\n[*] Generating hash report...")
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        print("\n[-] No users found!")
        return False

    if len(users) == 0:
        print("\n[-] No users to export!")
        return False

    report = []
    report.append("=" * 60)
    report.append("    HASHED PASSWORD CRACKER & SECURE AUTH TOOL")
    report.append("         Written By Thamizh Selvan")
    report.append("              HASH REPORT")
    report.append("=" * 60)
    report.append(f"\nTotal Users: {len(users)}")
    report.append("\n" + "-" * 60)

    for i, user in enumerate(users, 1):
        report.append(f"\nUser {i}:")
        report.append(f"  Username   : {user['username']}")
        report.append(f"  Algorithm  : {user['algorithm'].upper()}")
        report.append(f"  Hash       : {user['hash']}")
        report.append(f"  Salt       : {user['salt']}")
        report.append(f"  Note       : Plaintext password never stored")
        report.append("-" * 60)

    report.append("\n[!] This report is confidential!")
    report.append("[!] For educational purposes only!")
    report.append("=" * 60)

    filename = input("\nEnter report filename (e.g. report.txt): ")
    if not filename.endswith(".txt"):
        filename = filename + ".txt"

    with open(filename, "w") as f:
        f.write("\n".join(report))

    print(f"\n[+] Report exported to: {filename}")
    print(f"[+] Total users: {len(users)}")
    return True

# ============================================================
# PART 13 — HASH A FILE
# ============================================================
def hash_file(filepath, algorithm="sha256"):
    print(f"\n[*] Hashing file: {filepath}")
    if not os.path.exists(filepath):
        print(f"\n[-] File not found: {filepath}")
        return None

    file_size = os.path.getsize(filepath)
    print(f"[*] File size: {file_size} bytes")

    try:
        if algorithm == "md5":
            hasher = hashlib.md5()
        elif algorithm == "sha1":
            hasher = hashlib.sha1()
        elif algorithm == "sha256":
            hasher = hashlib.sha256()
        elif algorithm == "sha512":
            hasher = hashlib.sha512()
        else:
            print("\n[-] Invalid algorithm!")
            return None

        with open(filepath, "rb") as f:
            chunk = f.read(4096)
            while chunk:
                hasher.update(chunk)
                chunk = f.read(4096)

        file_hash = hasher.hexdigest()
        print(f"\n[+] File hashed successfully!")
        print(f"[+] File      : {filepath}")
        print(f"[+] Algorithm : {algorithm.upper()}")
        print(f"[+] Hash      : {file_hash}")
        print(f"\n[*] Use this hash to verify file integrity!")

        save = input("\nSave hash to a file? (yes/no): ")
        if save.lower() == "yes":
            hash_filename = os.path.basename(filepath) + "_hash.txt"
            with open(hash_filename, "w") as f:
                f.write(f"File      : {filepath}\n")
                f.write(f"Algorithm : {algorithm.upper()}\n")
                f.write(f"Hash      : {file_hash}\n")
                f.write(f"Size      : {file_size} bytes\n")
                f.write(f"Author    : Thamizh Selvan\n")
            print(f"\n[+] Hash saved to: {hash_filename}")

        return file_hash

    except PermissionError:
        print(f"\n[-] Permission denied: {filepath}")
        return None
    except Exception as e:
        print(f"\n[-] Error: {e}")
        return None

# ============================================================
# PART 14 — LOGIN WITH LOCKOUT
# ============================================================
def authenticate_with_lockout(username, password):
    if username in failed_attempts:
        if failed_attempts[username]["locked"]:
            print(f"\n[!] ACCOUNT LOCKED!")
            print(f"[!] User '{username}' locked after {MAX_ATTEMPTS} failed attempts!")
            print(f"[!] Contact admin to unlock.")
            return False

    print(f"\n[*] Authenticating '{username}'...")
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        print("\n[-] No users found!")
        return False

    for user in users:
        if user["username"] == username:
            salt = user["salt"]
            stored_hash = user["hash"]
            algorithm = user["algorithm"]
            attempt_hash = hash_password(salt + password, algorithm)

            if attempt_hash == stored_hash:
                if username in failed_attempts:
                    del failed_attempts[username]
                print(f"\n[+] LOGIN SUCCESSFUL!")
                print(f"[+] Welcome, {username}!")
                return True
            else:
                if username not in failed_attempts:
                    failed_attempts[username] = {"attempts": 0, "locked": False}
                failed_attempts[username]["attempts"] += 1
                attempts_left = MAX_ATTEMPTS - failed_attempts[username]["attempts"]
                print(f"\n[-] LOGIN FAILED!")
                print(f"[!] Attempts remaining: {attempts_left}")
                if failed_attempts[username]["attempts"] >= MAX_ATTEMPTS:
                    failed_attempts[username]["locked"] = True
                    print(f"\n[!] ACCOUNT LOCKED!")
                    print(f"[!] Too many failed attempts!")
                return False

    print(f"\n[-] User '{username}' not found!")
    return False

def unlock_account(username):
    if username in failed_attempts and failed_attempts[username]["locked"]:
        del failed_attempts[username]
        print(f"\n[+] Account '{username}' unlocked successfully!")
        return True
    else:
        print(f"\n[-] Account '{username}' is not locked!")
        return False

# ============================================================
# AI PART 15 — AI HASH TYPE DETECTOR
# ============================================================
def ai_detect_hash(hash_input):
    hash_input = hash_input.strip()
    hash_length = len(hash_input)

    print("\n" + "=" * 55)
    print("        AI HASH TYPE DETECTOR")
    print("=" * 55)
    print(f"\n[AI] Analysing hash...")
    print(f"[AI] Hash length: {hash_length} characters")

    valid_chars = set("0123456789abcdefABCDEF")
    is_hex = all(c in valid_chars for c in hash_input)

    if not is_hex:
        print("\n[AI] This does not look like a valid hash!")
        print("[AI] A hash should only contain 0-9 and a-f characters.")
        return None

    print("\n[AI] Running detection algorithm...")

    if hash_length == 32:
        algo, confidence, bits = "MD5", "99%", "128 bits"
        security = "WEAK"
        note = "MD5 is outdated — cracked easily using rainbow tables!"
        rec = "Do NOT use MD5 for password storage. Use SHA-256 instead."
    elif hash_length == 40:
        algo, confidence, bits = "SHA-1", "99%", "160 bits"
        security = "WEAK"
        note = "SHA-1 is deprecated since 2017!"
        rec = "Do NOT use SHA-1. Use SHA-256 or bcrypt instead."
    elif hash_length == 56:
        algo, confidence, bits = "SHA-224", "95%", "224 bits"
        security = "MODERATE"
        note = "SHA-224 is rarely used."
        rec = "Use SHA-256 or SHA-512 instead."
    elif hash_length == 64:
        algo, confidence, bits = "SHA-256", "99%", "256 bits"
        security = "STRONG"
        note = "SHA-256 is the current industry standard!"
        rec = "Good choice! SHA-256 is secure for most use cases."
    elif hash_length == 96:
        algo, confidence, bits = "SHA-384", "95%", "384 bits"
        security = "VERY STRONG"
        note = "SHA-384 is used in high security applications."
        rec = "Excellent for high security environments."
    elif hash_length == 128:
        algo, confidence, bits = "SHA-512", "99%", "512 bits"
        security = "VERY STRONG"
        note = "SHA-512 is extremely secure!"
        rec = "Excellent! SHA-512 is the strongest standard algorithm."
    else:
        print(f"\n[AI] Unknown hash type! Length {hash_length} not recognized.")
        return None

    print("\n" + "-" * 55)
    print(f"[AI] DETECTION COMPLETE!")
    print("-" * 55)
    print(f"[AI] Algorithm    : {algo}")
    print(f"[AI] Confidence   : {confidence}")
    print(f"[AI] Hash Length  : {hash_length} characters")
    print(f"[AI] Bit Strength : {bits}")
    print(f"[AI] Security     : {security}")
    print(f"\n[AI] Analysis     : {note}")
    print(f"[AI] Suggestion   : {rec}")
    print("-" * 55)

    crack = input(f"\n[AI] Do you want to crack this hash now? (yes/no): ")
    if crack.lower() == "yes":
        print("\n[AI] Choose attack method:")
        print("     1. Dictionary Attack")
        print("     2. Brute Force")
        print("     3. Rainbow Table")
        method = input("     Enter choice (1-3): ")
        algo_map = {"MD5": "md5", "SHA-1": "sha1", "SHA-256": "sha256", "SHA-512": "sha512"}
        algo_key = algo_map.get(algo, "sha256")
        if method == "1":
            dictionary_attack(hash_input, algo_key)
        elif method == "2":
            max_len = input("     Max password length (recommended 4): ")
            brute_force_attack(hash_input, algo_key, int(max_len))
        elif method == "3":
            rainbow_table_attack(hash_input, algo_key)
    return algo

# ============================================================
# AI PART 16 — AI PASSWORD STRENGTH CHECKER
# ============================================================
def ai_password_strength(password):
    print("\n" + "=" * 55)
    print("      AI PASSWORD STRENGTH CHECKER")
    print("=" * 55)

    score = 0
    tips = []

    # Length check
    if len(password) >= 16:
        score += 3
        print("[AI] Length 16+         : +3 points")
    elif len(password) >= 12:
        score += 2
        print("[AI] Length 12-15       : +2 points")
    elif len(password) >= 8:
        score += 1
        print("[AI] Length 8-11        : +1 point")
    else:
        tips.append("Use at least 12 characters")
        print("[AI] Length < 8         :  0 points (too short!)")

    # Uppercase
    if any(c.isupper() for c in password):
        score += 1
        print("[AI] Has uppercase       : +1 point")
    else:
        tips.append("Add uppercase letters (A-Z)")

    # Lowercase
    if any(c.islower() for c in password):
        score += 1
        print("[AI] Has lowercase       : +1 point")
    else:
        tips.append("Add lowercase letters (a-z)")

    # Numbers
    if any(c.isdigit() for c in password):
        score += 1
        print("[AI] Has numbers         : +1 point")
    else:
        tips.append("Add numbers (0-9)")

    # Special characters
    special = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
    if any(c in special for c in password):
        score += 2
        print("[AI] Has special chars   : +2 points")
    else:
        tips.append("Add special characters (!@#$%)")

    # Common password check
    if password.lower() in BUILTIN_WORDLIST:
        score -= 3
        tips.append("This is a very common password — change it immediately!")
        print("[AI] Common password     : -3 points (DANGEROUS!)")

    # Final rating
    print("\n" + "-" * 55)
    print(f"[AI] Total Score: {score}/8")

    if score <= 2:
        rating = "VERY WEAK"
        color_msg = "Change immediately! Anyone can crack this!"
    elif score <= 4:
        rating = "WEAK"
        color_msg = "Not safe. Improve your password!"
    elif score <= 6:
        rating = "MODERATE"
        color_msg = "Decent but can be stronger."
    elif score == 7:
        rating = "STRONG"
        color_msg = "Good password! Almost perfect."
    else:
        rating = "VERY STRONG"
        color_msg = "Excellent password! Very hard to crack!"

    print(f"[AI] Strength   : {rating}")
    print(f"[AI] Verdict    : {color_msg}")

    if tips:
        print(f"\n[AI] Tips to improve:")
        for tip in tips:
            print(f"     - {tip}")
    print("-" * 55)

# ============================================================
# AI PART 17 — AI PASSWORD GENERATOR
# ============================================================
def ai_generate_password():
    print("\n" + "=" * 55)
    print("         AI PASSWORD GENERATOR")
    print("=" * 55)

    try:
        length = int(input("\n[AI] Enter password length (recommended 16): "))
    except ValueError:
        length = 16

    print("\n[AI] Include:")
    use_upper = input("     Uppercase letters? (yes/no): ").lower() == "yes"
    use_lower = input("     Lowercase letters? (yes/no): ").lower() == "yes"
    use_digits = input("     Numbers?           (yes/no): ").lower() == "yes"
    use_special = input("     Special chars?     (yes/no): ").lower() == "yes"

    char_pool = ""
    if use_upper:
        char_pool += string.ascii_uppercase
    if use_lower:
        char_pool += string.ascii_lowercase
    if use_digits:
        char_pool += string.digits
    if use_special:
        char_pool += "!@#$%^&*()_+-=[]{}|;:,.<>?"

    if not char_pool:
        char_pool = string.ascii_letters + string.digits
        print("\n[AI] No options selected — using default (letters + numbers)")

    password = "".join(random.choice(char_pool) for _ in range(length))

    print(f"\n[AI] Generated Password : {password}")
    print(f"[AI] Length             : {length} characters")

    # Auto check strength
    print(f"\n[AI] Checking strength of generated password...")
    ai_password_strength(password)

    # Auto hash it
    hash_now = input("\n[AI] Hash this password now? (yes/no): ")
    if hash_now.lower() == "yes":
        print("\n[AI] Choose algorithm:")
        print("     1. MD5   2. SHA-1   3. SHA-256   4. SHA-512")
        algo_choice = input("     Enter choice (1-4): ")
        algo_map = {"1": "md5", "2": "sha1", "3": "sha256", "4": "sha512"}
        algorithm = algo_map.get(algo_choice, "sha256")
        result = hash_password(password, algorithm)
        global last_generated_hash, last_used_algorithm
        last_generated_hash = result
        last_used_algorithm = algorithm
        print(f"\n[AI] Algorithm : {algorithm.upper()}")
        print(f"[AI] Hash      : {result}")
        print(f"[AI] Hash stored for direct use in cracking options!")

    return password

# ============================================================
# AI PART 18 — AI CRACK TIME ESTIMATOR
# ============================================================
def ai_crack_time_estimator():
    print("\n" + "=" * 55)
    print("       AI CRACK TIME ESTIMATOR")
    print("=" * 55)

    password = input("\n[AI] Enter password to estimate crack time: ")
    length = len(password)

    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digits = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

    charset_size = 0
    charset_desc = []
    if has_lower:
        charset_size += 26
        charset_desc.append("lowercase (26)")
    if has_upper:
        charset_size += 26
        charset_desc.append("uppercase (26)")
    if has_digits:
        charset_size += 10
        charset_desc.append("digits (10)")
    if has_special:
        charset_size += 32
        charset_desc.append("special (32)")

    if charset_size == 0:
        charset_size = 26

    total_combinations = charset_size ** length

    # Speed estimates (attempts per second)
    speeds = {
        "Normal PC (CPU)":      1_000_000,
        "Gaming PC (GPU)":    100_000_000,
        "Hacker Rig (multi)": 1_000_000_000,
    }

    print(f"\n[AI] Password length  : {length} characters")
    print(f"[AI] Character set    : {', '.join(charset_desc) if charset_desc else 'lowercase only'}")
    print(f"[AI] Charset size     : {charset_size} characters")
    print(f"[AI] Total combos     : {total_combinations:,}")
    print("\n" + "-" * 55)
    print(f"[AI] CRACK TIME ESTIMATES:")
    print("-" * 55)

    for machine, speed in speeds.items():
        seconds = total_combinations / speed

        if seconds < 60:
            time_str = f"{seconds:.2f} seconds"
        elif seconds < 3600:
            time_str = f"{seconds/60:.2f} minutes"
        elif seconds < 86400:
            time_str = f"{seconds/3600:.2f} hours"
        elif seconds < 31536000:
            time_str = f"{seconds/86400:.2f} days"
        elif seconds < 31536000000:
            time_str = f"{seconds/31536000:.2f} years"
        else:
            time_str = f"{seconds/31536000:.2e} years (practically uncrackable!)"

        print(f"[AI] {machine:<25}: {time_str}")

    print("-" * 55)

    if total_combinations < 1_000_000:
        print("\n[AI] Verdict: VERY WEAK — cracked in seconds!")
    elif total_combinations < 1_000_000_000:
        print("\n[AI] Verdict: WEAK — cracked in minutes to hours!")
    elif total_combinations < 1_000_000_000_000:
        print("\n[AI] Verdict: MODERATE — could take days!")
    else:
        print("\n[AI] Verdict: STRONG — very difficult to crack!")

# ============================================================
# AI PART 19 — AI SECURITY TIPS
# ============================================================
def ai_security_tip():
    tips = [
        "Always use salted hashing — never store plain MD5 or SHA-1!",
        "Use bcrypt or SHA-256 for password storage — not MD5!",
        "Enable 2-Factor Authentication (2FA) on all your accounts!",
        "Never reuse the same password on multiple websites!",
        "Use a password manager like Bitwarden or KeePass!",
        "A 16+ character password is 100x harder to crack than 8 characters!",
        "rockyou.txt has 14 million real leaked passwords — avoid all of them!",
        "Rainbow table attacks fail against properly salted hashes!",
        "SHA-256 produces a 64-character hash — always check hash length!",
        "Brute force takes exponentially longer with each extra character!",
        "Change your passwords every 6 months for important accounts!",
        "Never save passwords in plain text files — always hash them!",
        "A password with special chars is 32x harder to brute force!",
        "Always implement account lockout after 5 failed attempts!",
        "Ethical hacking requires written permission — always get it first!",
    ]
    print("\n" + "=" * 55)
    print("          AI SECURITY TIP OF THE DAY")
    print("=" * 55)
    print(f"\n[AI] Tip: {random.choice(tips)}")
    print("=" * 55)

# ============================================================
# PART 8 — MAIN MENU
# ============================================================
def main():
    global last_generated_hash, last_used_algorithm

    print("=" * 55)
    print("  HASHED PASSWORD CRACKER & SECURE AUTH TOOL")
    print("       Written By Thamizh Selvan — BIA")
    print("=" * 55)

    # Show a tip on startup
    ai_security_tip()

    while True:
        print("\n---------- MAIN MENU ----------")
        print("--- HASHING ---")
        print("1.  Hash a password")
        print("2.  Hash a file")
        print("")
        print("--- CRACKING ---")
        print("3.  Dictionary Attack")
        print("4.  Brute Force Attack")
        print("5.  Rainbow Table Attack")
        print("")
        print("--- SECURE STORAGE ---")
        print("6.  Store a user securely")
        print("7.  Login / Authenticate")
        print("8.  Login with lockout protection")
        print("9.  Unlock a locked account")
        print("10. Show all stored users")
        print("11. Delete a user")
        print("12. Change password")
        print("13. Export hash report")
        print("")
        print("--- AI FEATURES ---")
        print("14. AI Hash Type Detector")
        print("15. AI Password Strength Checker")
        print("16. AI Password Generator")
        print("17. AI Crack Time Estimator")
        print("18. AI Security Tip")
        print("")
        print("19. Exit")
        print("--------------------------------")

        choice = input("Enter your choice (1-19): ")

        # ── Option 1 — Hash a password ──
        if choice == "1":
            password = input("\nEnter password to hash: ")
            print("\nChoose algorithm:")
            print("1. MD5  2. SHA-1  3. SHA-256  4. SHA-512")
            algo_choice = input("Enter choice (1-4): ")
            algo_map = {"1": "md5", "2": "sha1", "3": "sha256", "4": "sha512"}
            algorithm = algo_map.get(algo_choice, "sha256")
            result = hash_password(password, algorithm)
            last_generated_hash = result
            last_used_algorithm = algorithm
            print(f"\n[+] Algorithm : {algorithm.upper()}")
            print(f"[+] Hash      : {result}")
            print(f"\n[AI] Hash stored! Use options 3,4,5 directly without copy-paste!")

        # ── Option 2 — Hash a file ──
        elif choice == "2":
            filepath = input("\nEnter full file path: ")
            print("\nChoose algorithm:")
            print("1. MD5  2. SHA-1  3. SHA-256  4. SHA-512")
            algo_choice = input("Enter choice (1-4): ")
            algo_map = {"1": "md5", "2": "sha1", "3": "sha256", "4": "sha512"}
            algorithm = algo_map.get(algo_choice, "sha256")
            hash_file(filepath, algorithm)

        # ── Option 3 — Dictionary Attack ──
        elif choice == "3":
            if last_generated_hash:
                print(f"\n[AI] Last hash detected: {last_generated_hash[:20]}...")
                use_last = input("[AI] Use this hash directly? (yes/no): ")
                if use_last.lower() == "yes":
                    target = last_generated_hash
                    algorithm = last_used_algorithm
                    print(f"[AI] Using algorithm: {algorithm.upper()}")
                else:
                    target = input("\nEnter hash to crack: ")
                    print("\n1. MD5  2. SHA-1  3. SHA-256")
                    algo_choice = input("Enter choice: ")
                    algo_map = {"1": "md5", "2": "sha1", "3": "sha256"}
                    algorithm = algo_map.get(algo_choice, "sha256")
            else:
                target = input("\nEnter hash to crack: ")
                print("\n1. MD5  2. SHA-1  3. SHA-256")
                algo_choice = input("Enter choice: ")
                algo_map = {"1": "md5", "2": "sha1", "3": "sha256"}
                algorithm = algo_map.get(algo_choice, "sha256")
            dictionary_attack(target, algorithm)

        # ── Option 4 — Brute Force ──
        elif choice == "4":
            if last_generated_hash:
                print(f"\n[AI] Last hash detected: {last_generated_hash[:20]}...")
                use_last = input("[AI] Use this hash directly? (yes/no): ")
                if use_last.lower() == "yes":
                    target = last_generated_hash
                    algorithm = last_used_algorithm
                else:
                    target = input("\nEnter hash to crack: ")
                    print("\n1. MD5  2. SHA-1  3. SHA-256")
                    algo_choice = input("Enter choice: ")
                    algo_map = {"1": "md5", "2": "sha1", "3": "sha256"}
                    algorithm = algo_map.get(algo_choice, "sha256")
            else:
                target = input("\nEnter hash to crack: ")
                print("\n1. MD5  2. SHA-1  3. SHA-256")
                algo_choice = input("Enter choice: ")
                algo_map = {"1": "md5", "2": "sha1", "3": "sha256"}
                algorithm = algo_map.get(algo_choice, "sha256")
            length = input("Max password length (recommended 4): ")
            brute_force_attack(target, algorithm, int(length))

        # ── Option 5 — Rainbow Table ──
        elif choice == "5":
            if last_generated_hash:
                print(f"\n[AI] Last hash detected: {last_generated_hash[:20]}...")
                use_last = input("[AI] Use this hash directly? (yes/no): ")
                if use_last.lower() == "yes":
                    target = last_generated_hash
                    algorithm = last_used_algorithm
                else:
                    target = input("\nEnter hash to crack: ")
                    print("\n1. MD5  2. SHA-1  3. SHA-256")
                    algo_choice = input("Enter choice: ")
                    algo_map = {"1": "md5", "2": "sha1", "3": "sha256"}
                    algorithm = algo_map.get(algo_choice, "sha256")
            else:
                target = input("\nEnter hash to crack: ")
                print("\n1. MD5  2. SHA-1  3. SHA-256")
                algo_choice = input("Enter choice: ")
                algo_map = {"1": "md5", "2": "sha1", "3": "sha256"}
                algorithm = algo_map.get(algo_choice, "sha256")
            rainbow_table_attack(target, algorithm)

        # ── Option 6 — Store User ──
        elif choice == "6":
            username = input("\nEnter username: ")
            password = input("Enter password: ")
            print("\n1. MD5  2. SHA-1  3. SHA-256  4. SHA-512")
            algo_choice = input("Enter choice (1-4): ")
            algo_map = {"1": "md5", "2": "sha1", "3": "sha256", "4": "sha512"}
            algorithm = algo_map.get(algo_choice, "sha256")
            store_user(username, password, algorithm)

        # ── Option 7 — Authenticate ──
        elif choice == "7":
            username = input("\nEnter username: ")
            password = input("Enter password: ")
            authenticate(username, password)

        # ── Option 8 — Login with Lockout ──
        elif choice == "8":
            username = input("\nEnter username: ")
            password = input("Enter password: ")
            authenticate_with_lockout(username, password)

        # ── Option 9 — Unlock Account ──
        elif choice == "9":
            username = input("\nEnter username to unlock: ")
            unlock_account(username)

        # ── Option 10 — Show All Users ──
        elif choice == "10":
            show_all_users()

        # ── Option 11 — Delete User ──
        elif choice == "11":
            username = input("\nEnter username to delete: ")
            delete_user(username)

        # ── Option 12 — Change Password ──
        elif choice == "12":
            username = input("\nEnter username: ")
            change_password(username)

        # ── Option 13 — Export Report ──
        elif choice == "13":
            export_hash_report()

        # ── Option 14 — AI Hash Detector ──
        elif choice == "14":
            print("\n[AI] Welcome to AI Hash Type Detector!")
            if last_generated_hash:
                print(f"[AI] Last hash: {last_generated_hash[:20]}...")
                use_last = input("[AI] Use last generated hash? (yes/no): ")
                if use_last.lower() == "yes":
                    ai_detect_hash(last_generated_hash)
                else:
                    hash_val = input("[AI] Paste your hash: ")
                    ai_detect_hash(hash_val)
            else:
                hash_val = input("[AI] Paste your hash: ")
                ai_detect_hash(hash_val)

        # ── Option 15 — AI Strength Checker ──
        elif choice == "15":
            password = input("\n[AI] Enter password to check strength: ")
            ai_password_strength(password)

        # ── Option 16 — AI Password Generator ──
        elif choice == "16":
            ai_generate_password()

        # ── Option 17 — AI Crack Time Estimator ──
        elif choice == "17":
            ai_crack_time_estimator()

        # ── Option 18 — AI Security Tip ──
        elif choice == "18":
            ai_security_tip()

        # ── Option 19 — Exit ──
        elif choice == "19":
            print("\n[+] Thank you for using the tool!")
            print("[+] Written By Thamizh Selvan — BIA")
            print("[+] Goodbye!")
            break

        else:
            print("\n[-] Invalid choice! Please enter 1-19.")

if __name__ == "__main__":
    main()