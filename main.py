import sqlite3
from datetime import datetime as datum 
import random
import pdb

from login import login, logout


connexion = sqlite3.connect('to_do_list.db', autocommit = True)
cur = connexion.cursor()


def read():
    res = cur.execute('SELECT * FROM mytodos')
    [print(i) for i in res]

# -Ta bort to-dos från dbn i programmet

def delete():
    id = int(input('Vad är id:n du tar bort?: '))

    existingTodo = False
    try: 
        res = cur.execute('SELECT * FROM mytodos WHERE id = ?',(id,))
        res = res.fetchone()
        if res:
            existingTodo = True
    except:
        print('No such to do / Server error')

    if existingTodo:
        try:
            res = cur.execute('DELETE FROM mytodos WHERE id = ?',(id,))
            read()
        except:
            print('Server error deleting to do')


# -Uppdatera en befintlig to-do

def update():
    id = int(input('Vad är id:n du uppdatera?: '))

    existingTodo = False
    todoToUpdate = []
    try: 
        res = cur.execute('SELECT * FROM mytodos WHERE id = ?',(id,))
        res = res.fetchone()
        if res:
            existingTodo = True
            todoToUpdate.append(res)
    except:
        print('No such to do / Server error')

    if len(todoToUpdate)==1:        
        try:
            option = int(input('Vad vill du uppdatera? 1. Task, 2. Status, 3.Prioritet:' ))
            val = input('Ange ett värde till ditt fält: ')

            # if option == 3:
            #     val = int(val)

            field = ""

            if option==1:
                field = 'task'
            elif option == 2:
                field = 'status'
            elif option == 3:
                val = int(val)
                field = 'priority'

            try:
                query = f'UPDATE mytodos SET {field} = ? WHERE id = ?'
                cur.execute(query,(val,id,))
                read()
            except:
                print('Something went wrong')
        except:
            print('Something went wrong')
        


# -Skapa en ny to do

def create():
    task = input('Give the task name')
    due_date = str(datetime.datetime.now())
    status = 'undone'
    id = random.randint(0,1000000)
    priority = int(input('Vad är prioritet?: '))
    social = 1

    new_todo = (task,status,id,due_date,priority,social)

    res = cur.execute('INSERT INTO mytodos VALUES(?,?,?,?,?,?)',new_todo)
    read()

def createUser():
    pass

def deleteUser():
    pass

user = login(cur)


# while user['name'] != '':
#     action = int(input('Vad vill du göra?: '))
#     if user['role']=='admin':
#         print('Du är admin')
#         break
#     elif user['role']=='user':
#         print('Du är user')
#         break
