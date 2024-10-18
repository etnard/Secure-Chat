# SIMPLE END-TO-END ENCRYPTED MESSENGER

This is a simple console encrypted messenger. It useses asynchronous key exchange. The RSA encryption library is used to generate the keys as well as encrypt and decrypt the messages.

## Run

To run the program just run the executable `./dist/SecureChat.exe`.

## Packages:
import tkinter: Used for GUI.

import socket: Used to connect.

import threading: Used to add threads to the program.

import rsa: Used for RSA algorithm.

import os: Used to access .env file data.

## Capturing Data

Wireshark was used to capture the data.

Examples of unencrypted messages:

![Alt text](images/Unencrypted1.png?raw=true "Unencrypted Message 1:")
![Alt text](images/Unencrypted2.png?raw=true "Unencrypted Message 2:")

Exampel of an encrypted message:

![Alt text](images/Encrypted1.png?raw=true "Encrypted Message:")
