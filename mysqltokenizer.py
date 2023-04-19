#!/usr/bin/env python3

import sys
import getopt
from antlr4 import *
from MySqlLexer import MySqlLexer
from MySqlParser import MySqlParser

def main(argv):
    try:
        opts, args = getopt.getopt(sys.argv[1:], "il", ['identifiers', 'literals'])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(1)
    oIdentifiers = False
    oLiterals = False
    for opt, arg in opts:
        match opt:
            case ('-i'|'--identifiers'):
                oIdentifiers = True
            case ('-l'|'--literals'):
                oLiterals = True
            case other:
                assert False, "unknown option {other}"

    line = ''
    lastIter = False
    while True:
        try:
            newLines = sys.stdin.readline()
        except KeyboardInterrupt:
            break
        if not newLines:
            lastIter = True
        newLinesSplitted = newLines.split('\0')
        line += newLinesSplitted[0]
        if len(newLinesSplitted) <= 1 and lastIter == False:
            continue
        inputStream = InputStream(line)
        lexer = MySqlLexer(inputStream)
        tokensStream = CommonTokenStream(lexer)
        parser = MySqlParser(tokensStream)

        tokens = lexer.getAllTokens()
        tokensNoSpaces(parser, tokens, oIdentifiers, oLiterals)

#        tree = parser.root()

        if lastIter == True:
            break
        line = newLinesSplitted[1].lstrip()

def tokensNoSpaces(parser, tokens, identifiers, literals):
    output = ""
    for token in tokens:
        tokenSymbolicType = parser.symbolicNames[token.type]
        match tokenSymbolicType:
            case ('SPACE'):
                output += printToString(' ', end='')
            case 'ID':
                output += printToString(token.text if identifiers == True else '{:'+tokenSymbolicType+':}', end='')
            case 'REVERSE_QUOTE_ID':
                output += printToString(token.text if identifiers == True else '{:'+tokenSymbolicType+':}', end='')
            case 'DOT_ID':
                output += printToString(token.text if identifiers == True else '{:'+tokenSymbolicType+':}', end='')
            case ('NULL_LITERAL'|'FILESIZE_LITERAL'|'START_NATIONAL_STRING_LITERAL'|
                  'STRING_LITERAL'|'DECIMAL_LITERAL'|'HEXADECIMAL_LITERAL'|
                  'REAL_LITERAL'|'NULL_SPEC_LITERAL'):
                output += printToString(token.text if literals == True else '{:'+tokenSymbolicType+':}', end='')
            case other:
                output += printToString(token.text.upper(), end='')
    import re
    output = re.sub(r'(?<=OR)(.+?OR)\1+', r' {:OR_LOOP:} OR', output)
    output = re.sub(r'(?<=AND)(.+?AND)\1+', r' {:AND_LOOP:} AND', output)
    output = re.sub(r'(?<=,)(.+?,)\1+', r' {:COMMA_LOOP:},', output)
    output = output.rstrip()
    print(output)

def printToString(*args, **kwargs):
    import io
    output = io.StringIO()
    print(*args, file=output, **kwargs)
    contents = output.getvalue()
    output.close()
    return contents

if __name__ == '__main__':
    main(sys.argv)
