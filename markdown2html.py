#!/usr/bin/python3
"""
a script markdown2html.py that takes an argument 2 strings:

First argument is the name of the Markdown file
Second argument is the output file name
"""
import hashlib
import os
import sys

def check_line(line):
    """ checks if a line contains bold syntax and write it """
    foundb1 = False
    foundb2 = False
    founde1 = False
    founde2 = False
    foundm1 = False
    foundm2 = False
    foundc1 = False
    foundc2 = False
    for i in range(len(line) - 2):
        if line[i] + line[i + 1] == '**':
            index1 = i
            foundb1 = True
            break
    if foundb1:
        for j in range(i + 2, len(line) - 1):
            if line[j] + line[j + 1] == '**':
                index2 = j
                foundb2 = True
                break
    if foundb2:
        line = line[:index1] + "<b>" + line[index1 + 2:index2] + "</b>" + line[index2+2:]
    for i in range(len(line) - 2):
        if line[i] + line[i + 1] == '__':
            index1 = i
            founde1 = True
            break
    if founde1:
        for j in range(i + 2, len(line) - 1):
            if line[j] + line[j + 1] == '__':
                index2 = j
                founde2 = True
                break
    if founde2:
        line = line[:index1] + "<em>" + line[index1 + 2:index2] + "</em>" + line[index2+2:]
    for i in range(len(line) - 2):
        if line[i] + line[i + 1] == '[[':
            index1 = i
            foundm1 = True
            break
    if foundm1:
        for j in range(i + 2, len(line) - 1):
            if line[j] + line[j + 1] == ']]':
                index2 = j
                foundm2 = True
                break
    if foundm2:
        line = line[:index1] + hashlib.md5(line[index1 + 2:index2].encode()).hexdigest() + line[index2+2:]
    for i in range(len(line) - 2):
        if line[i] + line[i + 1] == '((':
            index1 = i
            foundc1 = True
            break
    if foundc1:
        for j in range(i + 2, len(line) - 1):
            if line[j] + line[j + 1] == '))':
                index2 = j
                foundc2 = True
                break
    if foundc2:
        token = line[index1 + 2:index2].replace("c", '')
        token = token.replace('C', '')
        line = line[:index1] + token + line[index2+2:]
    return line

def handle_heading(line, words, size, f2):
    """ A function that handles headings """
    if words[0] == '#' * size and size in range(1, 7):
        open_tag = '<h' + str(size) + '>'
        close_tag = '</h' + str(size) + '>'
        html_line = open_tag + check_line(line[size + 1:]) + close_tag + '\n'
        f2.write(html_line)

def open_list(list_type, list_started, f2):
    """ write the opening list tag if needed"""
    if not list_started:
        f2.write("<{}>\n".format(list_type))
    return True

def close_list(list_type, list_started, f2):
    """ write the closing list tag if needed"""
    if list_started:
        f2.write("</{}>\n".format(list_type))
    return False


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)
    elif not os.path.exists(sys.argv[1]):
        error = "Missing " + sys.argv[1] + '\n'
        sys.stderr.write(error)
        exit(1)
    with open(sys.argv[1]) as f1, open(sys.argv[2], 'w') as f2:
        data = f1.readlines()
        list_started = False
        list_type = ''
        for line in data:
            line = line.split('\n')[0]
            words = line.split(' ')
            size = len(words[0])
            if size > 0 and words[0][0] == '#':
                list_started = close_list(list_type, list_started, f2)
                list_type = ''
                handle_heading(line, words, size, f2)
            elif line[0:2] == "- " or line[0:2] == "* ":
                if line[0:2] == "- ":
                    if list_type == 'ol':
                        list_started = close_list(list_type, list_started, f2)
                    list_type = 'ul'
                else:
                    if list_type == 'ul':
                        list_started = close_list(list_type, list_started, f2)
                    list_type = 'ol'
                list_started = open_list(list_type, list_started, f2)
                html_line = "<li>" + check_line(line[2:]) + "</li>\n"
                f2.write(html_line)
                if line + '\n' == data[-1]:
                    list_started = close_list(list_type, list_started, f2)
            else:
                list_started = close_list(list_type, list_started, f2)
                list_type = ''
                if line == '':
                    pass
                else:
                    if line + '\n' == data[0] or data[data.index(line + '\n') - 1] == '\n':
                        f2.write("<p>\n")
                    elif data[data.index(line + '\n') - 1][:2] in ('- ', '* ', '# ') and line != '':
                        f2.write("<p>\n")
                    else:
                        f2.write("<br/>\n")
                    f2.write("{}\n".format(check_line(line)))
                    if line + '\n' == data[-1] or data[data.index(line + '\n') + 1] == '\n':
                        f2.write("</p>\n")
                    elif data[data.index(line + '\n') + 1][:2] in ('- ', '* ', '# '):
                        f2.write("</p>\n")
    exit(0)
