######
# -*- coding: utf-8 -*-
# © 09/13/2020 by @zihaoDONG. ALL RIGHTS RESERVED
# File: utils.py
######

import json
import tkinter

known_face_encodings = []
known_face_names = []
encodings_path = "encodings.json"
names_path = "names.json"


def getDataFromFile():
    global known_face_encodings, known_face_names
    with open(encodings_path, 'r', encoding='utf-8') as fe, open(names_path, 'r', encoding='utf-8') as fn:
        # global known_face_encodings, known_face_names
        info = json.loads(fe.readline())
        known_face_encodings = info
        # with open(names_path, 'r', encoding = 'utf-8') as fn:
        # global known_face_encodings, known_face_names
        info = json.loads(fn.readline())
        known_face_names = info


def load_data():
    global known_face_encodings, known_face_names
    try:
        getDataFromFile()
        # return known_face_encodings, known_face_names
        # print(known_face_names, known_face_encodings)
    except FileNotFoundError:
        Dump()
    return known_face_encodings, known_face_names


def Dump():
    global known_face_encodings, known_face_names
    with open(encodings_path, 'w', encoding = 'utf-8') as fe:
        json.dump(known_face_encodings, fe)
    with open(names_path, 'w', encoding = 'utf-8') as fn:
        json.dump(known_face_names, fn)


def addNewPerson(name, encoding):
    global known_face_encodings, known_face_names
    known_face_encodings.append(encoding)
    known_face_names.append(name)
    Dump()
    load_data()


def getName():
    global name
    root = tkinter.Tk()
    root.title("Notice")
    root.geometry("400x150")
    e1 = tkinter.Label(root, text="Never Seen You Before, Please Enter Your Name Below.")
    e1.grid(row=0, column=0, padx=10, pady=10)
    txt = tkinter.Entry()
    txt.grid(row=1, column=0, padx=10, pady=10)

    def Name():
        global name
        name = txt.get()

    tkinter.Button(root, text='Save', command=Name)\
        .grid(row = 2, column = 0, padx = 10, pady = 10)
    root.mainloop()
    # print(name)
    return name