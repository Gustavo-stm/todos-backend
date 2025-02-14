import sqlite3
from datetime import datetime 
import random
import pdb

from login import login, logout


connexion = sqlite3.connect('to_do_list.db', autocommit = True)
cur = connexion.cursor()


def readTodos(user):
    if user['role']=='admin':
        res = cur.execute('SELECT * FROM mytodos')
        [print(i) for i in res]
    else:
        res = cur.execute('SELECT todo_id FROM userstodos WHERE user_id = ? ',(int(user['id']),))
        res = res.fetchall()
        todos_ids = [x for x in res]
        [print(todo[0]) for todo in todos_ids]

# -Ta bort to-dos från dbn i programmet

def deleteTodos():
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
            # readTodos()
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
                readTodos()
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
    # readTodos()

def createUser():
    id = random.randint(0,10000000)
    username = input('Enter username: ')
    password = input('What is password: ')

    if len(username) < 8 or len(password) <8:
        print('Username or password needs to be 8 chars long')
        createUser()

    try:
        role = int(input('Role: 1. Admin, 2. User'))

    except:
        print('Only numbers please')
        createUser()

    if role == 1:
        role = 'admin'
    elif role == 2:
        role='user'

    newUser={'id':id, 'username':username, 'password':password,'role':role}
    try:
        res = cur.execute('INSERT INTO users (id,name,password,role) VALUES (?,?,?,?)', (newUser['id'], newUser['username'], newUser['password'],newUser['role'],))
        res = res.fetchall()
        print(res)
    except:
        print('Something wrong with us')

def getUsers():

    allUsers = ""
    try:
        allUsers = cur.execute('SELECT * FROM users')
        allUsers = allUsers.fetchall()
    except:
        print('Something went wrong with us')

    return allUsers


def deleteUser():
    allUsers = getUsers()
    [print(user) for user in allUsers]

    id = int(input('What is the id of the user to delete?: '))

    userToDelete = [user for user in allUsers if user[0]==id]
    
    if len(userToDelete)>0:
        res = cur.execute('DELETE FROM users WHERE id = ?',(int(userToDelete[0][0]),))
        res.fetchall()
        print(f'User {userToDelete} successfully deleted')
    else:
        print('No such user')
        deleteUser()


user = login(cur)

if 'msg' in user.keys():
    print(user['msg'])
else:
    if user['role']=='admin':
        print("""1. Create user, 2. Delete user
              3. Read todos, 4. Delete todos  """)
        action = int(input('Vad vill du göra?: '))

        if action==1:
            createUser()
        elif action == 2:
            deleteUser()
        elif action == 3:
            readTodos(user)
        elif action == 4:
            deleteTodos()
        
    elif user['role']=='user':
        print("""1. Read todos""")
        action = int(input('Vad vill du göra?: '))

        if action==1:
            readTodos(user)
        
