# gui
import tkinter as tk
from tkinter import scrolledtext, font, messagebox

# necessary includes for internet
import socket
import threading

# encryption algorithm
import rsa
publicKey, prviateKey = rsa.newkeys(1024)

# get ipv4 address saved in .env file and set port
import os
from dotenv import load_dotenv
load_dotenv()
ipAddress = os.getenv('ipv4')
port = 9999
publicPartner = None

def startGui(clientSocket):
    global publicPartner

    def sendMsg(event = None):
        message = entry.get()
        if(message):
            chatWindow.config(state = tk.NORMAL)
            chatWindow.insert(tk.END, "You: " + message + "\n")
            chatWindow.config(state = tk.DISABLED)
            entry.delete(0, tk.END)
            clientSocket.send(rsa.encrypt(message.encode(), publicPartner))

    def recMsg():
        while True:
            try:
                messagePartner =  rsa.decrypt(clientSocket.recv(1024), prviateKey).decode()
                chatWindow.config(state = tk.NORMAL)
                chatWindow.insert(tk.END, "Partner: " + messagePartner + "\n")
                chatWindow.config(state = tk.DISABLED)
            except Exception as e:
                break

    root = tk.Tk()
    root.title("Dylan's Secure Chat")
    root.geometry("1100x800")  
    root.config(bg = "#2B2B2B")  

    customFont = font.Font(family = "Courier New", size = 12)
    buttonFont = font.Font(family = "Courier New", size = 10, weight = "bold")

    chatWindow = scrolledtext.ScrolledText(root, wrap = tk.WORD, state = tk.DISABLED, font = customFont, borderwidth = 0, relief = tk.FLAT)
    chatWindow.pack(padx = 10, pady = 10, fill = tk.BOTH, expand = True)
    chatWindow.config(bg = "#1C1C1C", fg = "#D3D3D3")

    scrollBar = chatWindow.pack_slaves()[0]  
    scrollBar.config(bg = "#3D3D3D", activebackground = "#5C5C5C", width = 0) 
    scrollBar.pack(side = tk.RIGHT, fill = tk.Y)

    inputFrame = tk.Frame(root, bg = "#2B2B2B")
    inputFrame.pack(padx = 10, pady = 10, fill = tk.X)

    entry = tk.Entry(inputFrame, font = customFont, bg = "#D3D3D3", fg = "#2B2B2B", relief = tk.FLAT)
    entry.pack(side = tk.LEFT, fill = tk.X, expand = True, padx = (0, 10))

    entry.bind("<Return>", sendMsg)

    def onEnter(e):
        sendButton.config(bg="#3CB371")

    def onLeave(e):
        sendButton.config(bg="#2E8B57")

    sendButton = tk.Button(inputFrame, text = "Send", command = sendMsg, font = buttonFont, bg = "#2E8B57", fg = "white", relief = tk.FLAT)
    sendButton.pack(side = tk.RIGHT)
    sendButton.bind("<Enter>", onEnter)
    sendButton.bind("<Leave>", onLeave)

    threading.Thread(target = recMsg, daemon = True).start()

    root.mainloop()

def networkGUI():
    def connect():
        global publicPartner
        ipAddress = ipEntry.get()
        port = portEntry.get()
        try:
            port = int(port)
            if hostVar.get():
                
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.bind((ipAddress, port))
                server.listen()

                client, _ = server.accept()
                client.send(publicKey.save_pkcs1("PEM"))

                publicPartner = rsa.PublicKey.load_pkcs1(client.recv(1024))

                setupWindow.destroy()
                startGui(client)
            else:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((ipAddress, port))

                publicPartner = rsa.PublicKey.load_pkcs1(client.recv(1024))

                client.send(publicKey.save_pkcs1("PEM"))
                setupWindow.destroy()
                startGui(client)
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))    

    setupWindow = tk.Tk()
    setupWindow.title("Network Setup")
    setupWindow.geometry("200x250")
    setupWindow.config(bg = "#2B2B2B")
    
    hostVar = tk.BooleanVar(value = True)
    tk.Radiobutton(setupWindow, text = "Host", variable = hostVar, value = True, bg = "#2B2B2B", fg = "white").pack(anchor = tk.W)
    tk.Radiobutton(setupWindow, text = "Connect", variable = hostVar, value = False, bg = "#2B2B2B", fg = "white").pack(anchor = tk.W)

    tk.Label(setupWindow, text = "IP Address:", bg = "#2B2B2B", fg = "white").pack(pady = 5)
    ipEntry = tk.Entry(setupWindow)
    ipEntry.insert(0, ipAddress)
    ipEntry.pack(pady=5)

    tk.Label(setupWindow, text = "Port:", bg = "#2B2B2B", fg = "white").pack(pady = 5)
    portEntry = tk.Entry(setupWindow)
    portEntry.insert(0, str(port))  
    portEntry.pack(pady = 5)

    connectButton = tk.Button(setupWindow, text = "Connect", command = connect, bg = "#2E8B57", fg = "white")
    connectButton.pack(pady = 10)
    
    setupWindow.mainloop()
    
networkGUI()