from tkinter import *
import sys
import socket
import threading

# Server connection settings
ip = '127.0.0.1'
PORT = 5432
FORMAT = 'utf-8'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip, PORT))


class Interface():
    def __init__(self):
        # Window init
        self.window = Tk()
        self.window.withdraw()

        # Font
        self.font = ('Calibri', '11')

        # First screen Configuration
        self.loginScreen = Toplevel()
        self.loginScreen.title('Chat - login')
        self.loginScreen.bind('<Escape>', self.close)
        self.loginScreen.resizable(0, 0)
        self.loginScreen.config(bg='#303030', width=350, height=250)

        # Message
        self.message = Label(self.loginScreen, text='Welcome!', justify=CENTER,
                             font='Calibri 16 bold', bg='#303030', fg='#FFFFFF')
        self.message.place(relx=0.5, rely=0.5, y=-50, anchor='s')

        # UserName Label
        self.userlabel = Label(self.loginScreen, justify=CENTER, text='User: ',
                               font='Calibri 14 bold', bg='#303030', fg='#FFFFFF')
        self.userlabel.place(relx=0.5, rely=0.5, x=-100, anchor=CENTER)

        # UserName TextBox
        self.userBox = Entry(self.loginScreen, font=self.font, border=2)
        self.userBox.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.userBox.focus()

        # Join Button
        self.joinBtn = Button(self.loginScreen, width=20, border=3, text='JOIN', justify=CENTER,
                              font=self.font, command=lambda: self.goFoward(self.userBox.get()))
        self.joinBtn.place(relx=0.5, rely=0.5, y=50, anchor=CENTER)

        self.window.mainloop()

        # Destroy first screen and initialize the chat
    def goFoward(self, name):
        self.loginScreen.destroy()
        self.chatroom(name)

        receiveMsg = threading.Thread(target=self.receiveMsg)
        receiveMsg.start()

        # Chat window configuration
    def chatroom(self, name):
        self.font = ('SegoeUI', '11')
        self.name = name
        self.window.deiconify()
        self.window.title('Chat Room!')
        self.window.config(bg='#303030', width=450, height=550)

        # Top
        self.labelTop = Label(self.window, bg='#202020',
                              fg='#ffffff', text=self.name, font=self.font, pady=6)
        self.labelTop.place(relwidth=1)

        # Text messages view
        self.textContainer = Text(self.window, width=20, height=1,
                                  bg='#656565', fg='#ffffff', font=self.font, padx=5, pady=1)
        self.textContainer.place(relheight=1, relwidth=1, rely=0.05)

        # Bottom
        self.labelBottom = Label(self.window, bg='#202020', height=150)
        self.labelBottom.place(relwidth=1, rely=0.8)

        # Chat message box settings
        self.messageBox = Entry(
            self.labelBottom, width=200, bg='#505050', fg='#ffffff', font=self.font)
        self.messageBox.place(
            relheight=0.03, relwidth=0.75, relx=0.01, rely=0.01)
        self.messageBox.focus()

        # Chat message button settings
        self.messageBtn = Button(self.labelBottom, text='Send', font=self.font,
                                 width=20, bg='#909090', command=lambda: self.sendBtn(self.messageBox.get()))
        self.messageBtn.place(relx=0.77, rely=0.01,
                              relheight=0.03, relwidth=0.2)

        # Chat binds
        self.window.bind('<Escape>', self.close)
        self.window.bind(
            '<Return>', lambda x: self.sendBtn(self.messageBox.get()))

        # Chat main cursor
        self.textContainer.config(cursor='arrow')

        # Chat scroll settings
        scroll = Scrollbar(self.textContainer)
        scroll.place(relheight=1, relx=1)
        scroll.config(command=self.textContainer.yview)
        self.textContainer.config(state=DISABLED)

        # just a close/stop function
    def close(self, event):
        sys.exit(0)

        # Chat send button function
    def sendBtn(self, message):
        self.textContainer.config(state=DISABLED)
        self.message = message
        self.messageBox.delete(0, END)
        send = threading.Thread(target=self.sendMsg)
        send.start()

        # Chat messages receive
    def receiveMsg(self):
        # Running tests
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)
                if message == 'NAME':
                    client.send(self.name.encode(FORMAT))
                else:
                    self.textContainer.config(state=NORMAL)
                    self.textContainer.insert(END, message+'\n')
                    self.textContainer.config(state=DISABLED)
                    self.textContainer.see(END)
            except:
                print('ERROR!')
                client.close()
                break

        # Chat send message
    def sendMsg(self):
        self.textContainer.config(state=DISABLED)
        while True:
            message = (f'{self.name} >> {self.message}\n')
            client.send(message.encode(FORMAT))
            break


# Init class
main = Interface()
