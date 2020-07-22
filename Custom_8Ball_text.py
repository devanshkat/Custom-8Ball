from tkinter import *
from PIL import Image, ImageTk, ImageFont, ImageDraw
from random import choice
import sqlite3


root = Tk()
root.title("Welcome to Customizable 8Ball!")
root.iconbitmap('c:/custom8ball/custom8ballimages/magicBallStart.ico')

connec = sqlite3.connect("custom_8Ball_text.db")
curso = connec.cursor()


# Only use code to create inital database table
curso.execute("""CREATE TABLE IF NOT EXISTS phrases (
        phrase text
        )""")

firstspaceLabel = Label(root, text="Welcome to Customizable 8Ball!", height=3, font=("freesansfont", 28))
firstspaceLabel.grid(row=0, column=0, columnspan=4)


def add_phrase():
    global enter_phrase
    global submit_btn
    global hide_add_btn
    global add_btn

    add_btn = Button(root, text="Add a phrase to the 8Ball", height=2, width=78, relief=RAISED, command=add_phrase)
    add_btn.grid_forget()
    hide_add_btn = Button(root, text="Add a phrase to the 8Ball", height=2, width=78, relief=RAISED, command=hide_add_phrase)
    hide_add_btn.grid(row=3, column=0, columnspan=4)
    enter_phrase = Entry(root, width=79, borderwidth=5)
    enter_phrase.grid(row=4, column=0, sticky=E, columnspan=3, pady=(15, 0), ipady=6)
    submit_btn = Button(root, text="Add Phrase", height=2, relief=RAISED, command=submit_phrase)
    submit_btn.grid(row=4, column=3, sticky=W, columnspan=1, pady=(10, 0))


def hide_add_phrase():
    global enter_phrase
    global submit_btn
    global hide_add_btn
    global add_btn

    hide_add_btn = Button(root, text="Add a phrase to the 8Ball", height=2, width=78, relief=RAISED, command=hide_add_phrase)
    hide_add_btn.grid_forget()
    enter_phrase.grid_forget()
    submit_btn.grid_forget()
    add_btn = Button(root, text="Add a phrase to the 8Ball", height=2, width=78, relief=RAISED, command=add_phrase)
    add_btn.grid(row=3, column=0, columnspan=4)


def submit_phrase():
    global enter_phrase

    try:
        connec = sqlite3.connect("custom_8Ball_text.db")
        curso = connec.cursor()

        curso.execute("INSERT INTO phrases VALUES(:phrase)", 
                {
                    "phrase": enter_phrase.get()
                })

        connec.commit()
        connec.close()
        enter_phrase.delete(0, END)

    except sqlite3.Error:
        enter_phrase.insert(0, "Phrase failed to submit. Please try again.")

def show_record():
    global records
    global show_phrases
    global show_phrases_label
    global show_oid_label
    global phrases_label
    global oid_label

    try:
        show_phrases.grid_forget()

        connec = sqlite3.connect("custom_8Ball_text.db")
        curso = connec.cursor()

        curso.execute("SELECT *, oid FROM phrases")
        records = curso.fetchall()

        print_phrases = ''
        print_oid = ''
        for record in records:
            print_phrases += str(record[0]) + "\n"
            print_oid += str(record[1]) + "\n"
        

        phrases_label = Label(root, text="Label")
        phrases_label.grid(row=8, column=0, columnspan=2)

        oid_label = Label(root, text="ID Number")
        oid_label.grid(row=8, column=2, columnspan=2)

        show_phrases_label = Label(root, text=print_phrases)
        show_phrases_label.grid(row=9, column=0, columnspan=2)

        show_oid_label = Label(root, text=print_oid)
        show_oid_label.grid(row=9, column=2, columnspan=2)

        hide_phrases_btn = Button(root, text="Hide Custom 8Ball Phrases",  width=78, height=2, command=hide_phrases)
        hide_phrases_btn.grid(row=7, column=0, columnspan=4)

        connec.commit()
        connec.close()
    
    except sqlite3.Error:
        error_label = Label(root, text="Failed to retrieve phrases. Please restart the application.", font=(("OpenSans-Regular.ttf"), 16))
        error_label.grid(row=8, column=0, columnspan=4)

def hide_phrases():
    global show_phrases
    global show_phrases_label
    global show_oid_label
    global hide_phrases_btn
    global phrases_label
    global oid_label

    hide_phrases_btn = Button(root, text="Hide Custom 8Ball Phrases", command=hide_phrases)

    phrases_label.grid_forget()
    oid_label.grid_forget()
    hide_phrases_btn.grid_forget()
    show_phrases_label.grid_forget()
    show_oid_label.grid_forget()

    show_phrases = Button(root, text="Show Custom 8Ball Phrases", width=78, height=2, command=show_record)
    show_phrases.grid(row=7, column=0, columnspan=4)


def play_game():
    global ask
    global play_window
    global question_box

    play_window = Toplevel()
    play_window.title("Play Customizable 8Ball!")
    play_window.iconbitmap('magicBallStart.ico')    
    
    question_box = Entry(play_window, width=50, borderwidth=7)
    question_box.grid(row=0, column=0, pady=(0,15), ipady=6)

    ask = Button(play_window, text="Ask 8Ball", height=2, command=ask_question)
    ask.grid(row=0, column=1, pady=(0,15))


def ask_question():
    global records
    global ask
    global play_window
    global a_phrase_label
    global ask_anot
 

    ask = Button(play_window, text="Ask 8Ball", height=2, command=ask_question, state=DISABLED)
    ask.grid(row=0, column=1, pady=(0,15))

    ask_anot = Button(play_window, text="Ask Again", height=2, command=reset_play_window)
    ask_anot.grid(row=2, column=0, columnspan=2)

    connec = sqlite3.connect("custom_8Ball_text.db")
    curso = connec.cursor()

    curso.execute("SELECT * FROM phrases")
    records = curso.fetchall()

    str_a_phrase = ''
    for record in records:
        a_phrase = choice(records)
        str_a_phrase = str(a_phrase[0])

    a_phrase_label = Label(play_window, text=str_a_phrase, font=("OpenSans-Regular.ttf", 16))
    a_phrase_label.grid(row=1, column=0, columnspan=2)

    connec.commit()
    connec.close()


def reset_play_window():
    global play_window
    global a_phrase_label
    global ask_anot
    global question_box


    ask_anot.grid_forget()
    a_phrase_label.grid_forget()

    question_box = Entry(play_window, width=50, borderwidth=7)
    question_box.grid(row=0, column=0, pady=(0,15), ipady=6)

    ask = Button(play_window, text="Ask 8Ball", height=2, command=ask_question)
    ask.grid(row=0, column=1, pady=(0,15))


def show_delete_btn():
    global delete_box
    global show_btns_frame
    global delete_btn
    global show_del_btn
    global hide_del_btn

    show_del_btn = Button(root, text="Delete a phrase in your 8Ball", height=2, width=78, relief=RAISED, command=show_delete_btn)
    show_del_btn.grid_forget()

    hide_del_btn = Button(root, text="Delete a phrase in your 8Ball", height=2, width=78, relief=RAISED, command=hide_delete_btn)
    hide_del_btn.grid(row=11, column=0, columnspan=4)

    show_btns_frame = LabelFrame(root, bd=0)
    show_btns_frame.grid(row=12, column=0, columnspan=4)
    
    delete_btn = Button(show_btns_frame, text="Delete Phrase with ID Number", height=2, command=delete_phrase)
    delete_btn.grid(row=0, column=2, sticky=E, ipadx=19, padx=1, columnspan=2)
    
    delete_box = Entry(show_btns_frame, width=56, borderwidth=5)
    delete_box.grid(row=0, column=0, ipady=6, columnspan=2, sticky=W)


def delete_phrase():
    global delete_box

    connec = sqlite3.connect("custom_8Ball_text.db")
    curso = connec.cursor()

    curso.execute("DELETE from phrases WHERE oid =" + delete_box.get())
    delete_box.delete(0, END)

    connec.commit()
    connec.close()


def hide_delete_btn():
    global delete_box
    global show_btns_frame
    global delete_btn
    global show_del_btn
    global hide_del_btn

    hide_del_btn = Button(root, text="Delete a phrase in your 8Ball", height=2, width=78, relief=RAISED, command=hide_delete_btn)
    hide_del_btn.grid_forget()

    show_del_btn = Button(root, text="Delete a phrase in your 8Ball", height=2, width=78, relief=RAISED, command=show_delete_btn)
    show_del_btn.grid(row=11, column=0, columnspan=4)

    delete_btn.grid_forget()
    delete_box.grid_forget()
    show_btns_frame.grid_forget()



play_btn = Button(root, text="Play", height=2, width=78, relief=RAISED, command=play_game)
play_btn.grid(row=1, column=0, columnspan=4)

space_label = Label(root, text="", width=15, height=2)
space_label.grid(row=2, column=0, columnspan=4)

add_btn = Button(root, text="Add a phrase to the 8Ball", height=2, width=78, relief=RAISED, command=add_phrase)
add_btn.grid(row=3, column=0, columnspan=4)

spaceLabel = Label(root, text="", width=15, height=2)
spaceLabel.grid(row=6, column=0, columnspan=4)

show_phrases = Button(root, text="Show Custom 8Ball Phrases", width=78, height=2, command=show_record)
show_phrases.grid(row=7, column=0, columnspan=4)

spacedLabel = Label(root, text="", width=15, height=2)
spacedLabel.grid(row=10, column=0, columnspan=4)

show_del_btn = Button(root, text="Delete a phrase in your 8Ball", height=2, width=78, relief=RAISED, command=show_delete_btn)
show_del_btn.grid(row=11, column=0, columnspan=4)


connec.commit()
curso.close()
connec.close()

root.mainloop()