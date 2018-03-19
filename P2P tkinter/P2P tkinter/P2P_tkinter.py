import time
import socket
import threading
import os
from tkinter import *

UDP_PORT = 5005
users = []
LogIp = ""
open_ch = ""
events = threading.Event() #???? ??? ?????????? ?????? ?????????
events.set() #event = True
cl_ch = 0 #close chat
number=0
#def setting(event):
def nothing():
    return(0)

def notification(event):  
    global LogIp
    LogIp = IPaddr + "@#" + str(login.get())
    users.append(LogIp)
    chat = open("chat" + str(login.get()) + ".txt", "a")
    chat.close()                           
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    i=1
    while i<256:
        addr='192.168.0.'+str(i)
        sock.sendto(LogIp.encode(), (addr, UDP_PORT))
        i=i+1
    btn.place_forget()
    ent.place_forget()
    label2.place_forget()
    users_list.place(y=27,width=68,relheight=1.0)
    chat_btn.place(x=0)


def Receiving():                                #Получение UDP пакетов, пополнение списка участников,
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.bind(('', UDP_PORT))
    while True:
        events.wait()  #если True продолжает работу, иначе ждет
        data, addr = sock.recvfrom(1024)
        if data.decode().find("@#") != -1:
            writeback = data.decode().split("@#")
            existing_user = 0
            for item in users:
                if item == data.decode():
                    existing_user = 1
            if existing_user != 1:
                users.append(data.decode())
                users_list.insert(0,writeback[1])
                chat = open("chat" + writeback[1] + ".txt", "a")
                chat.close()
                if data.decode() != LogIp:
                    sock.sendto(LogIp.encode(), (writeback[0], UDP_PORT)) #Пакет новому пользователю содержащий логин и IP
        elif data.decode().find("|") != -1:
            writeback = data.decode().split("|")
            with open("chat" + writeback[0] + ".txt", "a") as chat:
                chat.write("\n" + data.decode())


def Sending(event):
    message = str(ent_mes.get())
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    i = 0
    while i < len(users):
        IP = users[i].split("@#")
        if users_list.get(number) == IP[1]:
            events.clear()    #event=False останавливает Receiving
            a = (str(login.get()) + "|" + message).encode()
            sock.sendto(a, (IP[0], UDP_PORT))
            with open("chat" + IP[1] + ".txt", "a") as chat:
                chat.write("\n" + a.decode())
            events.set()    #event=True позволяет Receiving продолжить работу
        i += 1


def updating_ch(num):
    while True:
        if cl_ch==1:
            break
        else:
            with open("chat" + users_list.get(num) + ".txt", "r") as file:
                tx.delete("1.0", "end")
                tx.insert(1.0,file.read())
            time.sleep(1)
 

def open_chat_btn(event):
    try:
        global cl_ch
        cl_ch = 0
        global number
        selection = users_list.curselection()
        number=selection[0]
        tx.place(x=68,height=250) 
        k = threading.Thread(target=updating_ch, args=(number,))
        k.start()
        sent_btn.place(x=265,y=250)
        ent_mes.place(y=255,x=135)
        back_btn.place(y=255, x=70)
    except:
        nothing()


def Back(event):
    global cl_ch
    cl_ch = 1
    tx.place_forget()
    sent_btn.place_forget()
    ent_mes.place_forget()
    back_btn.place_forget()


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
IPaddr = s.getsockname()[0]  #????????????? ????????? IP ??????
s.close()

c = threading.Thread(target=Receiving)
c.start()

root = Tk()
root.geometry("300x280")
login=StringVar()

ent = Entry(root,textvariable = login ,width=10,bd=3)
ent.place(relx=.5,rely=0.5)

btn= Button(root, text="connect")
btn.bind("<Button-1>", notification)
btn.place(relx=.5, rely=.6)

label2 = Label(text="Введите логин", justify=LEFT)
label2.place(relx=.5, rely=.4)

sent_btn=Button(root, text="sent")
sent_btn.bind("<Button-1>",Sending)

MES=StringVar()
ent_mes = Entry(root,textvariable = MES ,width=20,bd=3)

back_btn=Button(root, text="back")
back_btn.bind("<Button-1>",Back)

users_list=Listbox()

chat_btn=Button(root, text="open chat")
chat_btn.bind("<Button-1>",open_chat_btn)

tx = Text(font=('times',12),width=28,height=10,wrap=WORD)
tx.pack(side=RIGHT) 
tx.pack_forget()

root.mainloop()