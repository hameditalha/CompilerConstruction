from lexicalAnalyser import generateTokenSet
from syntaxAnalyser import parseTokenSet

def main():
    tokenSet = generateTokenSet('input.txt')
    print (*tokenSet, sep='\n')
    
    print(parseTokenSet([tokenSet[:-2][1]]))

if __name__ == "__main__":
    main()