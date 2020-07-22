from tkinter import *
from PIL import ImageTk, Image
from random import choice

root = Tk()
root.title("Ask 8Ball")
root.iconbitmap('c:/custom8ball/custom8ballimages/magicBallStart.ico')

# When you click the "Ask Again" button, this function is called, which resets the program to as it was when you first opened it.
def restart():
    global my_Label
    global ask_anot
    global ask
    global Question_Box
    global random_choice
    my_Label.grid_forget()
    ask_anot.grid_forget()    
    Question_Box = Entry(root, width=50, borderwidth=7)
    Question_Box.insert(0, "")
    Question_Box.grid(row=0, column=0, pady=(0,15))
    ask = Button(root, text="Ask 8Ball", command=random_choice)
    ask.grid(row=0, column=1, pady=(0,15))

"""
When you click the "Ask 8Ball" button, this function is called, which picks a random image and displays it on the screen,
along with the "Ask Again" button. Another key feature in this function is disabling the "Ask 8Ball" button so you
can't keep on clicking it multiple times to change the answer to what you want.
"""
def random_choice():
    a = ImageTk.PhotoImage(Image.open("c:/custom8ball/custom8ballimages/yes.jpg"))
    b = ImageTk.PhotoImage(Image.open("c:/custom8ball/custom8ballimages/No.jpg"))
    c = ImageTk.PhotoImage(Image.open("c:/custom8ball/custom8ballimages/perhaps.jpg"))
    global a_pic
    global ask_anot
    global ask
    global my_Label
    global restart
    a_pic = choice([a, b, c])
    my_Label = Label(root, image=a_pic)
    my_Label.grid(row=1, column=0, columnspan=2)
    ask = Button(root, text="Ask 8Ball", state=DISABLED)
    ask.grid(row=0, column=1, pady=(0,15))
    ask_anot = Button(root, text="Ask Again", command=restart)
    ask_anot.grid(row=2, column=0)

Question_Box = Entry(root, width=50, borderwidth=7)
Question_Box.grid(row=0, column=0, pady=(0,15))
ask = Button(root, text="Ask 8Ball", command=random_choice)
ask.grid(row=0, column=1, pady=(0,15))

root.mainloop()