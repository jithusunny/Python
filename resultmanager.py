#!/usr/bin/env python
#Filename: resultmanager.py
#Author: Jithu Sunny
#Date: 18:03:11
#Blog: http://jithusunny.blogspot.com/
#Email: jithusunnyk (at) gmail (dot) com

import re
from urllib import urlopen

def parse(string):
    '''Parses the HTML code and returns plain text'''
    string = re.sub(r'<.*?>|\n|[A-Z]+[0-9]+', '', string)
    string = re.sub(r'\t{1,6}', ' ', string)
    string = re.sub(r'.*Status|P : Passed.*', '', string)
    string = re.sub(r' {2,}', ' ', string)
    string = string.strip()
    return string

def failed(string):
    '''Returns true if student has failed in atleast one subject. False is returned otherwise.'''
    return re.search(r' F |F$', string)
 
def subject_string_match(string):
    '''Returns the first subject string in the input string.'''
    substr = re.search(r'([a-zA-Z-&] *)+([0-9-] *)+ [PF]', string)
    return substr

def stripA(string):
    '''Returns the string after deletion of 'A' from the end if presnt'''
    string = string.rstrip(' A ')
    string = string.rstrip(' A')
    string = string.strip()
    return string

def filter_subjects(string):
    '''Returns the dictionary - key: subject; value: 0.'''
    sub_dict = {}
    while string:
        string = string.strip()
        substring = subject_string_match(string).group()
        sub = re.search(r'([a-zA-Z-&] *)+', substring).group().strip()
        sub = stripA(sub)
        sub_dict[sub] = 0
        string = string[len(substring):]
    return sub_dict

def no_result(string):
    '''Returns true if the particular string contains label 'withheld'/'Withheld'''
    return re.search(r'withheld|Withheld|invalid|not registered', string)


def num_of_digits_roll(string):
    '''Return the number of digits in roll number.'''
    roll = re.search(r'(?<=regno=)[A-Za-z0-9]+', string).group()
    num = re.search(r'[0-9]+', roll).group()
    return len(num)

def subtotal(string):
    '''Returns the subject-total, ie the last number(before the symbol 'P') in input subject line.'''
    subtot = re.search(r'[0-9]+ P', string).group().split()[0]
    return int(subtot)

#Declarations of variables and data structures used.
failed_students = 0
flag = False
topper = [0] * 3
url = raw_input('Enter the url of result page of first(any) student from university website: ')
total = int(raw_input('Enter the total marks: '))
students = int(raw_input('Enter the total number of students: '))
individual_total = [0] * (students + 1)
effective_students = students
perc_above_80 = 0
perc_above_75 = 0
perc_60_to_75 = 0
perc_below_60 = 0

roll_prefix = re.search(r'(?<=regno=)[a-zA-Z]+', url).group()
url_prefix = re.search(r'.*?regno=', url).group()

#Populates the subject-dictionary.
page = urlopen(url).read()
result_string = parse(page)
subject_dict = filter_subjects(result_string)
zero_num = num_of_digits_roll(url) - 1

print '\nRoll number Total Percentage'
print '----------- ----- ----------'
#Does the calculation of pass-status, per-subject-pass-status & total of each student.
for i in range(1, students + 1):
    if i < 10:
        roll = roll_prefix + zero_num * '0' + str(i)
    elif i < 100:
        roll = roll_prefix + (zero_num - 1) * '0' + str(i)
    else:
        roll = roll_prefix + (zero_num - 2) * '0' + str(i)
    fail = False
    page = urlopen(url_prefix + roll + '&Submit=Submit').read()
    result_string = parse(page)

    if no_result(result_string):
        effective_students -= 1
    if failed(result_string):
        fail = True
        failed_students += 1

    sub = subject_string_match(result_string)
    while(sub):
        subject_line=sub.group()
        subject = re.search(r'([a-zA-Z-&] *)+', subject_line).group().strip()
        subject = stripA(subject)

        if failed(subject_line):
            subject_dict[subject] += 1
        if not fail:
            individual_total[i] += subtotal(subject_line)

        result_string = result_string[len(subject_line):].strip()
        sub = subject_string_match(result_string)
 
    if individual_total[i] > topper[1]:
        topper[0] = roll
        topper[1] = individual_total[i]
    if individual_total[i]:
        print roll, ' ', individual_total[i], ' - ', '%.2f' %(float(individual_total[i])/total*100)
        
        temp = float(individual_total[i])/total * 100
        if temp > 80:
            perc_above_80 += 1
        if temp > 75:
            perc_above_75 += 1
        if temp > 60 and temp < 75:
            perc_60_to_75 += 1
        if temp < 60:
            perc_below_60 += 1
        

print '\nTopper of the class is:', topper[0], '- Marks: ', topper[1], ' Percentage: %.2f' %(float(topper[1])/total * 100)

print '\nNo.of students with percentage above 80%: ', perc_above_80
print 'No.of students with percentage above 75%: ', perc_above_75
print 'No.of students with percentage in between 60% and 75%: ', perc_60_to_75
print 'No.of students with percentage below 60%: ', perc_below_60

print '\nClass Pass Percentage: %.4f(%d out of %d Students)\n' %(float(effective_students-failed_students)/effective_students*100, effective_students-failed_students, effective_students)

for subject in subject_dict:
    print 'Pass Percentage in', subject, "is: %.4f" %(float(effective_students-subject_dict[subject])/effective_students*100)
print
