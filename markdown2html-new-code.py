#!/usr/bin/python3
"""
a script markdown2html.py that takes an argument 2 strings:
First argument is the name of the Markdown file
Second argument is the output file name
"""
import hashlib
import os
import sys


def check_arguments():
    """ checks if arguments exit """
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)
    elif not os.path.exists(sys.argv[1]):
        error = "Missing " + sys.argv[1] + '\n'
        sys.stderr.write(error)
        exit(1)


def check_line(line):
    """ checks if a line contains bold or em or [[]] or (()) syntax """
    line = line_syntax(line, '**', '**', '<br>', '</br>', True)
    line = line_syntax(line, '__', '__', '<em>', '</em>', True)
    md5 = line_syntax(line, '[[', ']]', '', '', False)
    if md5[0] is True:
        index1 = md5[1]
        index2 = md5[2]
        line = line[:index1]\
            + hashlib.md5(line[index1 + 2:index2].encode()).hexdigest()\
            + line[index2+2:]
    C = line_syntax(line, '((', '))', '', '', False)
    if C[0] is True:
        index1 = C[1]
        index2 = C[2]
        token = line[index1 + 2:index2].replace("c", '')
        token = token.replace('C', '')
        line = line[:index1] + token + line[index2+2:]
    return line


def line_syntax(line, m_start, m_end, h_start, h_end, convert):
    """ checks if line contains a tag inside it and converts it """
    found1 = False
    found2 = False
    for i in range(len(line) - 2):
        if line[i] + line[i + 1] == m_start:
            index1 = i
            found1 = True
            break
    if found1:
        for j in range(i + 2, len(line) - 1):
            if line[j] + line[j + 1] == m_end:
                index2 = j
                found2 = True
                break
    if convert is True:
        if found2:
            return line[:index1] + h_start\
                    + line[index1 + 2:index2] + h_end + line[index2+2:]
        else:
            return line
    else:
        if found2:
            return [True, index1, index2]
        else:
            return [False, ]


def handle_heading(line, words, size, f2):
    """ A function that handles headings """
    if words[0] == '#' * size and size in range(1, 7):
        open_tag = '<h' + str(size) + '>'
        close_tag = '</h' + str(size) + '>'
        html_line = open_tag + check_line(line[size + 1:]) + close_tag + '\n'
        f2.write(html_line)


def handle_list(data, line, f2):
    """ writes list items + opening and closing list tags """
    if line[0:2] == "- ":
        list_type = 'ul'
    elif line[0:2] == "* ":
        list_type = 'ol'
    if (line + '\n' == data[0] or len(data[data.index(line + '\n') - 1]) < 2 or
            data[data.index(line + '\n') - 1][:2] != line[:2]):
        f2.write("<{}>\n".format(list_type))
    html_line = "<li>" + check_line(line[2:]) + "</li>\n"
    f2.write(html_line)
    if (line + '\n' == data[-1] or
            len(data[data.index(line + '\n') + 1]) < 2 or
            data[data.index(line + '\n') + 1][:2] != line[:2]):
        f2.write("</{}>\n".format(list_type))


def handle_paragraph(data, line, f2):
    """ writes paragraths """
    if (line + '\n' == data[0] or
            data[data.index(line + '\n') - 1][:2] in ('- ', '* ', '# ')):
        f2.write("<p>\n")
    elif data[data.index(line + '\n') - 1] == '\n':
        f2.write("<p>\n")
    else:
        f2.write("<br/>\n")
    f2.write("{}\n".format(check_line(line)))
    if line + '\n' == data[-1] or data[data.index(line + '\n') + 1] == '\n':
        f2.write("</p>\n")
    elif data[data.index(line + '\n') + 1][:2] in ('- ', '* ', '# ', '##'):
        f2.write("</p>\n")


if __name__ == "__main__":
    check_arguments()
    with open(sys.argv[1]) as f1, open(sys.argv[2], 'w') as f2:
        data = f1.readlines()
        for line in data:
            line = line.split('\n')[0]
            words = line.split(' ')
            size = len(words[0])
            if size > 0 and words[0][0] == '#':
                handle_heading(line, words, size, f2)
            elif line[0:2] == "- " or line[0:2] == "* ":
                handle_list(data, line, f2)
            elif line == '':
                pass
            else:
                handle_paragraph(data, line, f2)
    exit(0)
