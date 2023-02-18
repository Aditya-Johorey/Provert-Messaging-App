from tkinter import *
from PIL import Image,ImageTk
import socket
import threading

PORT=11111
# PORT=13950
SERVER="127.0.0.1"
# SERVER="3.142.167.4"

ADDRESS=(SERVER,PORT)
FORMAT="utf-8"
separator_token="<SEP>"
name=""
def forward(event=0):
    global name
    if person.get("1.0",END)!="\n" and len(person.get("1.0",END))>0:
        name = person.get("1.0", END).strip("\n").strip()+" "
        login.destroy()
    else:
        print("Invalid name!! please try again")

login=Tk()
login.config(bg="#FFDDCE")
login.geometry("350x200")
login.resizable(0,0)
display=Label(login,text="Please enter your name: ",bg="#FFDDCE",font=("Comic Sans MS", 15, "normal"))
person=Text(login,width=25,height=1,font=("Comic Sans MS", 15, "normal"))
go=Button(login,text="Start",width=13,height=1,bg="#9900B3",fg="white",activebackground="#FFDDCE",
          activeforeground="#9900B3",font=("Comic Sans MS", 15, "normal"),bd=1,command=forward)
login.bind("<Return>",forward)
display.place(relx=0.18,rely=0.1)
person.place(relx=0.06,rely=0.3)
go.place(relx=0.27,rely=0.6)
login.mainloop()


client=socket.socket()
# talking_to="
client.connect(ADDRESS)

client.send(name.encode(FORMAT))

def sending(event=0):
    to_send=entry.get("1.0",END).strip("\r")
    to_send=to_send.strip()
    if to_send!="\n":
        client.send(to_send.encode())
        # chat_frame.insert(END, "You: " + to_send)
        entry.delete("1.0",END)

def click(event):
    entry.delete("1.0",END)

def leave(event):
    if len(entry.get("1.0",END).strip("\n"))<=0:
        entry.delete("1.0", 'end')
        entry.insert("1.0", "Type a message..")
        window.focus()

window=Tk()
window.geometry("500x558")
window.title("PROVERT")
user=StringVar()
user.set(name)
window.resizable(0,0)
frame1=Frame(window,width=500,height=50,bg="black")
frame1.grid(row=0,column=0)
frame1.pack_propagate(False)
name=Label(frame1,textvariable=user,fg="White",bg="black",font=("Comic Sans MS", 15, "normal"))
name.pack(side=LEFT)
frame2=Frame(window,width=500,height=450,bg="#FFDDCE")
frame2.grid(row=1,column=0)
frame2.pack_propagate(False)
scroll=Scrollbar(frame2)
scroll.pack(side=RIGHT,fill=Y)
chat_frame=Text(frame2,insertbackground="#FFDDCE",wrap=WORD,yscrollcommand=scroll.set,width=40,height=16,font=("Comic Sans MS", 15, "normal"),bg="#FFDDCE",bd=0)
chat_frame.place(relx=0.0,rely=0.0)
chat_frame.bind("<Key>", lambda a: "break")
chat_frame.bindtags((str(chat_frame), str(window), "all"))


# chat_frame.bind("<1>", lambda event: event.widget.focus_set())
scroll.config(command=chat_frame.yview)
# chat_frame.config(state='disabled')
window.bind("<Return>",sending)
frame3=Frame(window,width=500,height=80,bg="#9900B3")
frame3.grid(row=2,column=0)
entry=Text(frame3,width=36,height=2,wrap=WORD,font=("Comic Sans MS", 15, "normal"),bg="#9900B3",fg="#FFDDCE",bd=0)
entry.place(relx=0.0,rely=0.0)
entry.insert("1.0","Type a message..")
entry.bind("<Button-1>", click)
entry.bind("<Leave>", leave)
entry.bind("<Super_L+>")
# entry.bind("<Shift-Return>",add_nl)
send_image=Image.open("Send_button.png")
send_image=send_image.resize((57,57))
send_image=ImageTk.PhotoImage(send_image)

send=Button(frame3,image=send_image,bd=0,bg="#FF9AE9",activebackground="#FF9AE9",command=sending)
send.place(relx=0.886,rely=0.0)

def message_formatting(message):
    pass

def listen_for_messages():
    # global talking_to
    # talking_to=client.recv(1024).decode()
    # window.update()

    chat_frame.insert('end',client.recv(1024).decode())
    # chat_frame.tag_configure("tag_name", justify='center')
    chat_frame.insert('end',client.recv(1024).decode())
    # chat_frame.tag_add('tag_name',"1.0","end")
    while True:
        message_recived=client.recv(1024).decode()
        if message_recived:
            chat_frame.insert('end',"\n"+message_recived)
            chat_frame.see("end")
            window.update()
t=threading.Thread(target=listen_for_messages)

t.start()

window.mainloop()