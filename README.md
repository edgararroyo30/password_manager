**Overview**
This project is a password manager built using Tkinter and CustomTkinter for the GUI, with Cryptography and bcrypt libraries used for secure password encryption and storage. The goal of this application is to securely store and manage users' passwords.

**Features**
Password encryption using bcrypt for hashing and cryptography for symmetric encryption.
User-friendly interface with Tkinter and CustomTkinter for a smooth and responsive experience.
Password generation with customizable settings for length and complexity.
Secure password storage in an encrypted format.
Master password protection for accessing stored passwords.
Cross-platform support (Windows, MacOS, Linux).

**How It Works**
**Master Password:** A master password is used to encrypt/decrypt the stored passwords, ensuring that only the owner can access them.
**Password Hashing: **The master password is hashed using bcrypt for secure storage.
**Encryption:** Stored passwords are encrypted using cryptography and saved in an encrypted format within a database.
**Secure Storage: **Passwords are stored in a secure database that is only accessible through the application.
**Security Measures**
Passwords are hashed and salted with bcrypt, ensuring high resistance to brute-force attacks.
Encrypted passwords can only be decrypted with the correct master password.
Symmetric encryption is applied to stored passwords, adding an extra layer of security.
**Usage**
**Add a new password:** Enter the required credentials and store them securely.
**Retrieve passwords:** Access stored passwords by entering the master password.
**Update or delete passwords:** Manage your stored passwords easily with the intuitive interface.
