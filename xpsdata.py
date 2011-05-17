#!/usr/bin/python

""" process xps data for maomao """

import re
import sys

AllBuf = []

def is_one(line):
    """ is this line a "1" ?"""
    if re.search('^\s*1\s*$',line):
        return True
    return False


def process(lines):
    """ process data and generate new form of table """
    length = len(lines)
    label = ""
    i = 0
    res = []
    max_line_num = 0

    while i < length:
        if is_one(lines[i]):
            label = lines[i-1].strip()
            i += 1
            start_val = float(lines[i])
            i += 1
            inteval = float(lines[i])
            i += 1
            line_num = int(lines[i])

            if line_num > max_line_num:
                max_line_num = line_num

            first_row = []
            second_row = []
            sub_res = []
            while line_num > 0:
                first_row.append(start_val)
                start_val += inteval
                line_num -= 1

                i += 1
                second_row.append(float(lines[i]))
            sub_res.append(label)
            sub_res.append(first_row)
            sub_res.append(second_row)
            res.append(sub_res)

        i += 1

    return res, max_line_num

def output(result, maxn, outfile):
    """ output buffer """
    ofile.write("%s\n" % outfile.name)
    for subres in result:
        ofile.write("%s," % subres[0])
        ofile.write("%s," % subres[0])

    ofile.write("\n")
    ofile.write("\n")
    ofile.write("\n")
    i = 0
    while i < maxn:
        for subres in result:
            if i < len(subres[1]):
                outfile.write( "%7.4f," % (subres[1][i]))
            else:
                outfile.write( "%8s," % ""),

            if i < len(subres[2]):
                outfile.write( "%8.4f," % (subres[2][i]))
            else:
                outfile.write( "%9s," % ""),
        outfile.write("\n")
        i += 1

for f in sys.argv[1:]:

    print "processing %s..." % f,
    buf = open(f,'r').readlines()
    ofilename = f.replace('.asc','_result.csv')
    ofile = open(ofilename,'w')
    result,maxn = process(buf)
    output(result,maxn,ofile)
    print 'Done'
#for subres in result:
#    for i in subres:
#        print i
