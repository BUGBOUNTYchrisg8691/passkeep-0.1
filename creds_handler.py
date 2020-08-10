#!/usr/bin/env python3

import bcrypt
import time
from password_creation import create_password
from encryption import *
from getpass import getpass

class Credentials:
    def __init__(self, service='', username='', password='', salt=None):
        self.service = service
        self.username = username
        self.password = password

        if salt == None:
            self.__salt = bcrypt.gensalt()
        else:
            self.__salt = salt


    def __str__(self):
        return 'Credentials({0}, {1}, {2})'.format(
            self.service, self.username, self.password
        )


    def __repr__(self):
        return 'Credentials(servcice: {0}, username: {1},' \
            ' password: {2}, salt: {3})'.format(
            self.service, self.username, self.password, self.__salt
            )

    
    def get_service(self):
        return self.service


    def get_username(self):
        return self.username


    def get_password(self):
        return self.password


    def get_salt(self):
        return self.__salt


    def set_service(self):
        self.service = str(input('Enter service: '))


    def set_username(self):
        self.username = str(input('Enter username: '))


    def set_password(self):
        action = str(input('Would you like to (g)enerate a password to your sp'
                           'ecs or (e)nter your own password: '))

        if (action.lower() == 'g'):
            length = input('Enter length: ')
            if (length == ''):
                length = 10
            else:
                length = int(length)
            spec_chars = str(input('Enter allowed special characters: '))
            self.password = create_password(length, spec_chars)

        elif (action.lower() == 'e'):
            password = str(getpass('Enter password: '))
            confirm = str(getpass( 'Confirm password: '))

            if (password == confirm):
                self.password = password
            else:
                print('An error occurred... ')
                time.sleep(3)
                self.set_password()

        else:
            print('An error occurred...')
            time.sleep(3)
            self.set_password()


    def hash_entry(self, mast_pass=None):
        if mast_pass == None:
            mast_pass = str(getpass('Enter master password: '))
            confirm = str(getpass('Confirm master password: '))

            if (mast_pass == confirm):
                pass

            else:
                print('An error occurred...')
                time.sleep(3)
                self.hash_entry()
            
        self.service = encrypt(self.service, mast_pass, self.__salt)
        self.username = encrypt(self.username, mast_pass, self.__salt)
        self.password = encrypt(self.password, mast_pass, self.__salt)
   

    def unhash_entry(self, mast_pass=None):
        if mast_pass == None:
            mast_pass = str(getpass('Enter master password: '))
            confirm = str(getpass('Confirm master password: '))

            if (mast_pass == confirm):
                pass

            else:
                print('An error occurred...')
                time.sleep(3)
                self.unhash_entry()
            
        self.service = decrypt(self.service, mast_pass, self.__salt)
        self.username = decrypt(self.username, mast_pass, self.__salt)
        self.password = decrypt(self.password, mast_pass, self.__salt)

#  def unhash_entry(self):
        #  mast_pass = str(getpass('Enter master password: '))
        #  confirm = str(getpass('Confirm master password: '))
#
        #  if (mast_pass == confirm):
            #  self.service = decrypt(self.service, mast_pass, self.__salt)
            #  self.username = decrypt(self.username, mast_pass, self.__salt)
            #  self.password = decrypt(self.password, mast_pass, self.__salt)
#
        #  else:
            #  print('An error occurred...')
            #  time.sleep(3)
            #  self.unhash_entry()

