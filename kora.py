__author__ = 'Wojto'
import socket
import random
import pymysql
from settings import *
import re
#settings located in settings file

if debug == True:
    channel = '#sram'
    host = "irc.freenode.net"
else:
    channel = '#kx'
    host = "irc.quakenet.org"

#guwner
random.seed()
podmiot = open('podmiot.txt', 'r')
okolicznik = open('okolicznik.txt', 'r')
orzeczenie = open('orzeczenie.txt', 'r')
dopelnienie = open('dopelnienie.txt', 'r')
przydawka = open('przydawka.txt', 'r')
def cytat(): #fetching quote from db
    connection = pymysql.connect(**connection_settings)
    kursor = connection.cursor()
    kursor.execute('SELECT * FROM Quote ORDER BY RAND() LIMIT 1')
    for row in kursor.fetchall():
                 print("PRIVMSG " + channel + " : " + "Quote nr:" + str(row[0]) + "  " + str(row[1]), file=soclog)
    kursor.close()
    connection.close()
def dodaj(): #adding quote to db
    connection = pymysql.connect(**connection_settings)
    kursor = connection.cursor()
    qwithline = 'INSERT INTO Quote (Quote) VALUES ("%s")' % quotemsg
    kursor.execute(qwithline)
    kursor.close()
    connection.close()
    print (qwithline)
def zguwnij():
    linep = random.choice(open('podmiot.txt').readlines())
    lineok = random.choice(open('okolicznik.txt').readlines())
    lineorz = random.choice(open('orzeczenie.txt').readlines())
    linedop = random.choice(open('dopelnienie.txt').readlines())
    lineprz = random.choice(open('przydawka.txt').readlines())

    zz1 = linep.rstrip()
    zz5 = lineok.rstrip()
    zz2 = lineorz.rstrip()
    zz3 = lineprz.rstrip()
    zz4 = linedop.rstrip()
    #print("PRIVMSG " + channel + " : " + zz1 + " " + zz2 + " " + zz3  + " " + zz4  + " " + zz5, file=soclog)
    msg = 'PRIVMSG {} : {}'.format(channel, ' '.join([zz1, zz2, zz3, zz4, zz5]))
    print(msg, file=soclog)
#Connect
soc = socket.socket()
soc.connect((host, port))

print ("Connecting to %s" % (host))

soclog = soc.makefile(mode='rw', buffering=1, encoding='utf-8', newline='\r\n')
def logIn(): #log in function
    print("NICK", bnick, file=soclog)
    print("USER", bnick, bnick, bnick, ':'+bnick, file=soclog)
logIn() #calling the log in function
FirstPing = False

for line in soclog:
    line = line.strip()
    print(line)
    if 'PRIVMSG' in line:
        msg = ":".join(line.split (':')[2:])
        nick = line.split('!')[ 0 ].replace(':','')
    if 'PING' in line:
        print("PONG :" + line.split(":")[1], file=soclog)
        if not FirstPing:
            print("JOIN :" +channel, file=soclog)
            FirstPing = True;
    if 'zguwnij' in line:
        zguwnij()
    if 'join' in line:
        print("JOIN :" + channel, file=soclog)
    if '!cyt' in line:
        cytat()
    if '!test' in line:
        quotemsg = msg.replace("!test ","",1)
        dodaj()




