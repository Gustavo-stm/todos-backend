import sqlite3
import datetime
import random
import pdb

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

            if option == 3:
                val = int(val)

            field = ""

            if option==1:
                field = 'task'
            elif option == 2:
                field = 'status'
            elif option == 3:
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


while True:
    print('Välkommen. 1. Läsa to dos, 2. Lägg till, 3. Uppdatera, 4. Ta bort')
    action = int(input('Vad vill du göra?: '))
    if action == 1:
        read()
    elif action == 2:
        create()
    elif action == 3:
        update()
    elif action == 4:
        delete()
    elif action == "q":
        break
    else:
        print('No such action, try again')





