import pdb
from datetime import datetime as datum
import hashlib

def login(cur):

    username = input('What is username: ')
    password = input('What is password: ')
    allUsers = ''

    try:
        allUsers = cur.execute('SELECT * FROM users')
        allUsers = allUsers.fetchall()
    except:
        print('Something went wrong with us')


    singleUser = [user for user in allUsers if user[1]==username and user[2]==password]
    
    if len(singleUser)>0:
        singleUser = {'name':singleUser[0][1], 'id':singleUser[0][0],'role':singleUser[0][5]}
        return singleUser
    else:
        return {'msg':'No user with that name or password'}

def logout(cur,user):
    pass