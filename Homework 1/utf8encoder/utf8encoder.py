import os
import binascii
import sys

def split(str, num):
    return [ str[start:start+num] for start in range(0, len(str), num) ]

def getIntValue(input):
    if input != '':
        binaryValue = bin(int(binascii.hexlify(input), 16))
        intValue = int(binaryValue,2)
        return intValue

def readFile(filePath):
    fileContent = []

    f = open(filePath, "rb")

    try:
        byte = f.read(2)
        fileContent.append(getIntValue(str(byte)))

        while byte != "":
            # Do stuff with byte.
            byte = f.read(2)
            # print str(byte) + '--' + str(getIntValue(str(byte)))
            if str(byte) != '':
                fileContent.append(getIntValue(str(byte)))
            #fileContent.append(str(byte))
    finally:
        f.close()

    return fileContent

def getUTF8(input):
    output = []
    for val in input:
        if val < int('10000000', 2):
            utf8 = bin(0b0000000 | val)[2:]
            padding = '0' * (7 - len(utf8))
            utf8 = '0' + padding + utf8

            output.append(utf8)
        elif val < int('100000000000' , 2):
            utf8_low = bin(0b111111 & val)[2:]
            padding = '0' * (6 - len(utf8_low))
            utf8_low = '10' + padding + utf8_low
            utf8_high = bin(val & 0b11111000000)[2:-6]
            padding = '0' * (5 - len(utf8_high))
            utf8_high = '110' + padding + utf8_high
            utf8 = utf8_high + utf8_low

            output.append(utf8)
        else:
            utf8_low = bin(0b111111 & val)[2:]
            padding = '0' * (6 - len(utf8_low))
            utf8_low = '10' + padding + bin(0b111111 & val)[2:]

            utf8_middle = bin(val & 0b111111000000)[2:-6]
            padding = '0' * (6 - len(utf8_middle))
            utf8_middle = '10' + padding + utf8_middle

            utf8_high = bin(val & 0b1111000000000000)[2:-12]
            padding = '0' * (4 - len(utf8_high))
            utf8_high = '1110' + padding + utf8_high
            utf8 = utf8_high + utf8_middle + utf8_low

            output.append(utf8)
    return output

def writeOutput(data):
    output = open('utf8encoder_out.txt', 'wb')

    for bin in utf8:
        # print bin
        if len(bin) == 1:
            output.write(chr(int(bin,2)))
        else:
            bytes = split(bin, 8)
            for byte in bytes:
                output.write(chr(int(byte,2)))

if len(sys.argv) != 2:
    print "Missing the input file as a parameter"
else:
    fileData = readFile(sys.argv[1])
    utf8 = getUTF8(fileData)
    print fileData[0:5]
    print utf8[0:5]
    writeOutput(utf8)
