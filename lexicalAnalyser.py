def generateTokenSet(address : str) -> list:
    with open(address, 'r') as inp:
        inpt = inp.read() + '\n@'
    from colorama import Fore, Style
    ts = wordBreaker(inpt)
    for x in ts:
        if x[1] == '_er':
            print(f'\n{Fore.RED}\n!!!LEXICAL ERROR {x[2]} AT line : {x[0]} !!!{Style.RESET_ALL}')
            return []
    print(f'\n{Fore.GREEN}Token set generated\n{Style.RESET_ALL}')
    return ts

def wordBreaker(st: str) -> list:
    
    words = []
    line = 1
    word = ''
    
    def addWord(word : str, words = words) -> list:
        if word != '' and word != '\n':
            words.append([line, tokenAssignment(word), word])
            if words[-1][1] == '_st':
                words[-1][2] = words[-1][2][1:-1]
    
    cr  = 0           
    while cr < len(st):
        
        #space
        if st[cr] == ' ':
            addWord(word)
            word = ''

        #new line
        elif st[cr] == '\n':
            addWord(word)
            word = ''
            line += 1

        #comment
        elif st[cr] == '#':
            addWord(word)
            word = ''
    
            if st[cr+1] == '#':
                cr += 2
            
                while str(st[cr] + st[cr+1]) != '##':
            
                    if st[cr+1] == '@':
                        addWord(st[cr+1])
                        break
            
                    if st[cr] == '\n':
                        line += 1
                    cr += 1
                cr += 2
            
            elif st[cr+1] != '#':
            
                while st[cr] != '\n':
            
                    if st[cr] == '@':
                        break
                    cr += 1
                line += 1

        #arithimatic, unary, relational with assignment
        elif st[cr] in ['+', '-', '*', '/', '%', '^', '~', '=', '>', '<', '!']:
            addWord(word)
            word = st[cr]
            if st[cr + 1] in ['+', '-', '*', '/', '%', '^', '~', '=', '>', '<', '!']:
                word += st[cr+1]
                addWord(word)
                word = ''
                cr+=1

        #string '
        elif st[cr] == "'":
            addWord(word)
            word = st[cr]
            cr += 1
            while st[cr] != "'":
                if st[cr] in ['\n'] :
                    addWord(word)
                    word = ''
                    break
                word += st[cr]
                cr += 1
            word += st[cr]
            addWord(word)
            word = ''

        #string ""
        elif st[cr] == '"':
            addWord(word)
            word = st[cr]
            cr += 1
            while st[cr] != '"':
                if st[cr] in ['\n'] :
                    addWord(word)
                    word = ''
                    break
                word += st[cr]
                cr += 1
            word += st[cr]
            addWord(word)
            word = ''
        
        #dot access
        elif st[cr] == '.':
            if word.isnumeric():
                word += st[cr]
            
            else:
                addWord(word)
                addWord(st[cr])
                word = ''
            
        #dict identifier
        elif st[cr] == ':':
            addWord(word)
            addWord(st[cr])
            word = ''

        #braces, comma, parantheses
        elif st[cr] in ['{', '}', '(', ')', ',']:
            addWord(word)
            addWord(st[cr])
            word = ''
      
        #list recheck
        elif st[cr] == '[':
            addWord(word)
            word = ''
            cr += 1
            while st[cr] != ']':
                cr += 1
                word += st[cr]
            word += st[cr]
            addWord(word)
            word = ''

        #adding char to word
        else:
            word += st[cr]

        cr+=1
    addWord(word)
    return words

def tokenAssignment(value : str) -> str:
    import re

    #tokens
    tokenSet = {
        #datatypes
        'str' : '_dt',
        'num' : '_dt',
        'bit' : '_dt',
        'list' : '_dt',

        #byte values
        'true' : '_bt',
        'false' : '_bt',

        #arithimatic operators
        '+' : '_sa',
        '-' : '_sa',
        '*' : '_md',
        '/' : '_md',
        '%' : '_md',

        #relational operators
        '<' : '_ro',
        '>' : '_ro',
        '<=' : '_ro',
        '>=' : '_ro',
        '!=' : '_ro',
        '==' : '_ro',

        #assignment operator
        '=' : '_eq',

        #unary operator
        '++' : '_uo',
        '--' : '_uo',
        'not' : '_uo',

        #binary
        'and' : '_ba',
        'or' : '_bo',

        #punctuators
        '.' : '_da',
        ',' : '_ca',
        ':' : '_ds',
        '{' : '_co',
        '}' : '_cc',
        '[' : '_so',
        ']' : '_sc',
        '(' : '_po',
        ')' : '_pc',
        '@' : '_tr',

        #blocks
        'for' : '_fr',
        'if' : '_if',
        'elif' : '_ef',
        'else' : '_es',
        'func' : '_fc',
        'class' : '_cs',

        #keywords
        'del' : '_dl',
        'in' : '_in',
        'abort' : '_at',
        'return' : '_rn',
        'this' : '_ts',

        #access modifier
        'global' : '_am'
    }

    #reserved
    if value in list(tokenSet.keys()):
        return tokenSet[value]

    #variable
    elif re.fullmatch('([_a-zA-Z]+[0-9]*|_[A-Za-z0-9]+)|(_)', value):
        return '_id'
    
    #string ""
    elif re.fullmatch('"{1}.*"{1}', value):
        return '_st' 

    #string ''
    elif re.fullmatch("'{1}.*'{1}", value):
        return '_st'
    
    #number
    elif re.fullmatch('[+-]?\d+[.\d]*', value):
        return '_nm'

    #list
    #elif re.fullmatch('', value):
    #    return '_lt'
    
    #error
    else:
        return '_er'