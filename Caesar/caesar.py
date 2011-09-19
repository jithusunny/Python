#!/usr/bin/python

#Date: Sept 19, 2011
#Filename: caesar.py
#Code for deciphering Caesar-Cipher

#Author: Jithu Sunny
#Blog: http://jithusunnyk.blogspot.com/
#Email: jithusunnyk@gmail.com

def shift(str, n):
    '''Forms the new string by shifting all characters in str by n places'''
    new = ''
    for c in str:
        if c.isalpha():
            num = ord(c) + n
            if c.islower():
                if num < 123:
                    new += chr(num)
                else:
                    new += chr(num - 26)
            elif c.isupper():
                if num < 91:
                    new += chr(num)
                else:
                    new += chr(num - 26)
        else:
            new += c
    return new

def combi(str):
    '''Prints all 25 possible plain-messages'''
    for i in range(1, 26):
        print shift(str, i)

str = raw_input('Enter the cipher: ')
combi(str)
