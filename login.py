import pdb
from datetime import datetime as datum
import hashlib

def login(cur):
    username = input('vad är ditt användarnamn?: ')
    password = input('Vad är ditt lösenord?: ')

    password = password.encode('utf-8')
    password= hashlib.md5(password).hexdigest()

    user ={'id':'','name':'','role':''}

    try:
        existingUsers = cur.execute('SELECT * FROM users')
        existingUsers = existingUsers.fetchall()
        
        try:
            if len(existingUsers)>0:
                for exUser in existingUsers:
                    if username and password in exUser:
                        print('User exists')
                        user['id'] = int(exUser[0])
                        user['name'] = exUser[1]
                        user['role'] = exUser[5]
                        break
                else:
                    raise ValueError
        except ValueError:
            print('No such user or wrong password') 
        
    except SystemError:
        print('Not working at the moment. It´s us')
        
    return user

def logout(cur,user):
    return {'loggedOut':True, 'msg':f'{user["name"]} has logged out'}