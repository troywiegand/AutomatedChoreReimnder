#!/usr/bin/python2.7
import sqlite3
import sys
import os

from twilio.rest import Client


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

db = sqlite3.connect('./house.db')
db.row_factory = dict_factory



account_sid=os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

people=db.execute("SELECT * FROM People").fetchall()
chores=db.execute("SELECT * FROM Chores").fetchall()

print(people)
print(chores)
orderchores=["","","","","",""]
orderchores[1]=db.execute("SELECT Name FROM Chores WHERE `Order`='1' ").fetchall()[0]['Name']
orderchores[2]=db.execute("SELECT Name FROM Chores WHERE `Order`='2' ").fetchall()[0]['Name']
orderchores[3]=db.execute("SELECT Name FROM Chores WHERE `Order`='3' ").fetchall()[0]['Name']
orderchores[4]=db.execute("SELECT Name FROM Chores WHERE `Order`='4' ").fetchall()[0]['Name']
orderchores[5]=db.execute("SELECT Name FROM Chores WHERE `Order`='5' ").fetchall()[0]['Name']

for person in people:

    # Chore Rotation
    if person['name']!='Rowan':
        if person['chore']==orderchores[5]:
            person['chore']=orderchores[1]
            db.execute('UPDATE People SET chore = "'+orderchores[1]+'" WHERE name = "'+person['name']+'"')
        else:
            for x in range(1,5):
                if person['chore']==orderchores[x]:
                    person['chore']=orderchores[x+1]
                    db.execute('UPDATE People SET chore = "'+orderchores[x+1]+'" WHERE name = "'+person['name']+'"')
                    break
        
    ##Text Sending
    text="Hello "+person['name']+"! \n This week your chore is "+person['chore']

    message = client.messages.create(body=text,from_='+19014662863',to=person['number'])

    print(message.sid)


db.commit()
people=db.execute("SELECT * FROM People WHERE name='Troy' ").fetchall()

print(people)
