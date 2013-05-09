#!/usr/bin/python

""" process xps data for maomao """

import re
import sys
import glob

AllBuf = []

def is_one(line):
    """ is this line a "1" ?"""
    if re.search('^\s*1\s*$',line):
        return True
    return False


def process(lines, filename):
    """ process the buff of one single file
        The buff may contain one or mutiple block(s)
        format each buff into the following structure:
            [ "filename", elem_num, label(atom), [first column], [second column] ]
        and add it to AllBuf
    """
    length = len(lines)
    label = ""    # atom label
    elem_num = 0  # number of data in one block
    i = 0
    res = []      # a structure for one block
    #filename = '-'.join(filename.strip().split('-')[0:-1])
    filenamefrac = filename.strip().split('-')
    if filenamefrac[-1][0] == 'n':
        filename = '-'.join(filename.strip().split('-')[0:-1])


    while i < length:
        if is_one(lines[i]):
            res = []
            label = lines[i-1].strip()
            i += 1
            start_val = float(lines[i])
            i += 1
            inteval = float(lines[i])
            i += 1
            elem_num = int(lines[i])
            res.append(filename)
            res.append(elem_num)
            res.append(label)

            first_row = []
            second_row = []

            while elem_num > 0:
                first_row.append(start_val)
                start_val += inteval
                elem_num -= 1
                i += 1
                second_row.append(float(lines[i]))

            res.append(first_row)
            res.append(second_row)
            AllBuf.append(res)

        i += 1

def SortBuf():
    """ sort AllBuf according to the label (atom) """
    length = len(AllBuf)

    i = 0
    while (i < length):
        j = i
        while j < length:
            if AllBuf[i][2] > AllBuf[j][2]:
                AllBuf[i], AllBuf[j] = AllBuf[j], AllBuf[i]
            j += 1
        i += 1

def FindMaxLen(head,tail):
    """ find the max elem_num between AllBuf[head] and AllBuf[tail] """
    maxlen = 0
    ibuf = head
    while ibuf < tail:
        if maxlen < AllBuf[ibuf][1]:
            maxlen = AllBuf[ibuf][1]
        ibuf += 1

    return maxlen

def OutPut():
    """ output buffer """
    length = len(AllBuf)
    head = tail = 0
    while True:
        head = tail
        while AllBuf[tail][2] == AllBuf[head][2]:
            tail += 1
            if tail >= length:
                break

        ofilename = AllBuf[head][2] + ".csv"
        f = open(ofilename, 'w')
        print "Output to %s..." % ofilename,

        bufi = head
        while bufi < tail:
            f.write("%s,%s" % (AllBuf[bufi][0],AllBuf[bufi][0]))
            if bufi+1 < tail:
                f.write(",")
            bufi += 1
        f.write('\n')

        elemi = 0
        elem_num = FindMaxLen(head, tail)
        while elemi < elem_num:
            bufi = head
            while bufi < tail:
                if elemi < AllBuf[bufi][1]:
                    f.write( "%7.4f,%8.4f" % (AllBuf[bufi][3][elemi], AllBuf[bufi][4][elemi]) )
                else:
                    f.write(" , ")
                if bufi+1 < tail:
                    f.write(",")
                bufi += 1
            elemi += 1
            f.write('\n')

        print "OK"

        if tail >= length:
            return
        
def testoutput():
    for buf in AllBuf:
        print buf[0], buf[1], buf[2], buf[3][0]


filelist = glob.glob("*.asc")
if not filelist:
    sys.stderr.write("NO .asc file found")
    exit(1)


for f in filelist:
    print "processing %s..." % f ,
    buf = open(f,'r').readlines()
    process(buf, f.replace('.asc',''))
    print 'Done'


SortBuf()
OutPut()

