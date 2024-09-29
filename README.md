# Password Manager

## Overview
This project is a **password manager** built using **Tkinter** and **CustomTkinter** for the GUI, along with **Cryptography** and **bcrypt** libraries for secure password encryption and storage. The goal of this application is to securely store and manage users' passwords.

## Features
- **Password encryption** using bcrypt for hashing and cryptography for asymmetric encryption.
- **User-friendly interface** built with Tkinter and CustomTkinter for a smooth experience.
- **Password generation** with customizable settings for length and complexity.
- **Secure password storage** in an encrypted format.
- **Master password** protection for accessing stored passwords.
- **Cross-platform support** for Windows, macOS, and Linux.

## How It Works
- **Master Password**: A master password is used to encrypt/decrypt stored passwords, ensuring that only the authorized user can access them.
  
- **Password Hashing**: The master password is hashed using bcrypt for secure storage.

- **Encryption**: Stored passwords are encrypted using cryptography and saved in an encrypted format within a database.

- **Secure Storage**: Passwords are stored in a secure database that can only be accessed via the application.

## Security Measures
- **Hashed passwords**: Passwords are hashed and salted using bcrypt, providing strong protection against brute-force attacks.
  
- **Encrypted data**: Passwords are encrypted with asymmetric encryption, adding an additional layer of security.

- **Master password protection**: Passwords can only be decrypted using the correct master password.

## Usage
- **Add a new password**: Enter credentials and securely store them.
- **Retrieve passwords**: Enter the master password to access stored passwords.
- **Update or delete passwords**: Manage your passwords easily with an intuitive interface.
