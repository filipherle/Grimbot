import sqlite3 as sql
import random
import ConfigParser
import calendar
import sys
import os
import datetime
import platform
import socket
# Config stuff
configParser = ConfigParser.RawConfigParser()   
configFilePath = 'config.txt'
configParser.read(configFilePath)
name = configParser.get('basic-config', 'name')
name_of_bot = configParser.get('basic-config', 'name_of_bot')
# Variables
now = datetime.datetime.now()
yy = now.year
mm = now.month
teach_me = {"question":['Teach me how to answer this!', 'Please teach me how to respond to this, ' + name + '!', 'How do I respond to this ' + name + '? Train me!', 'I have no clue how to respond to this! Teach me!']}
print "Welcome, " + name + "! My name is " + name_of_bot + "! How may I help you?"
class Robot(object):
        def __init__(self):
                global teach_me
                self.teach_me = teach_me
        
        def memory(self, user_voice):
                global conn
                conn = sql.connect('memory.db')
                global c
                c = conn.cursor()
                c.execute ('CREATE TABLE IF NOT EXISTS response_memory (user_voice, response)')
                conn.commit()
                response_memory = c.execute('SELECT user_voice, response FROM response_memory WHERE user_voice=?', (user_voice,)).fetchall()
                return response_memory

        def listen(self):
                while True:
                        try:
                                user_voice = raw_input("> ")
                                if user_voice == "@exit":
                                        print "Bye!"
                                        sys.exit()
                                elif user_voice == "@time":
                                        print datetime.datetime.now()
                                elif user_voice == "@calendar":
                                        print "\n" + (calendar.month(yy, mm))
                                elif user_voice == "@computer info":
                                        print "Name: " + (socket.gethostname())
                                        print "OS: " + platform.platform()
                                        print "CPU: " + platform.processor()
                                elif user_voice == "@help":
                                        print """
@exit - exits program
@time - shows date & time
@calendar - shows calendar of current month and year
@computer info - shows computer information
@help - shows this
                                              """

                                else:
                                        self.process(user_voice)
                        except:
                                sys.exit()
                else:
                        sys.exit()

        def process(self, user_voice):
                
                def remember(user_voice):
                        thoughts = self.memory(user_voice)
                        #print thoughts
                        if thoughts:
                                for u, r in thoughts:
                                        user_data = u
                                        response_data = r
                        else:
                                user_data = None
                                response_data = None

                        return user_data, response_data

                def learn(user_voice):
                        if user_voice != None:
                                learned_response = raw_input("[" + name_of_bot + "] " + random.choice(teach_me['question']) + "\n")
                                c.execute('INSERT INTO response_memory(user_voice, response) VALUES(?,?)', (user_voice, learned_response))
                                conn.commit()
                                self.listen()
                        else:
                                self.speak(response_data)

                user_data, response_data = remember(user_voice)
                if user_voice == user_data:
                        self.speak(response_data)
                else:
                        learn(user_voice)

        def speak(self, response_data):
                goodbye = ['bye', 'see you later', 'bubye', 'goodbye' ]
                print "[" + name_of_bot + "] %s" %response_data
                if response_data in goodbye:
                        exit()
                else:
                        self.listen()

bot = Robot()
bot.listen()
