import sys

from CYK import Parser


if __name__ == '__main__':
    while True:
        print('Enter a CNF grammar G followed by an input word w. The starting left-hand side should use the letter \'S\' for the nonterminal letter. Terminals should be lowercase and nonterminals uppercase. Whitespace does not matter.\n')

        print('Examples:')
        print('G = S -> AB|BC, A -> BA|a, B -> CC|b, C -> AB|a')
        print('w = babaa\n')

        print('G = S -> AB|BC, A -> SA|a, B -> BB|b')
        print('w = ababb\n')

        print('G = S -> AB, A -> a, B -> b')
        print('w = ba\n')

        print('-----------------------------------------------')

        grammar = input('G = ')
        word = input('w = ')

        print()
        parser = Parser.Parser(grammar)
        parser.parse(word)
        stop = input('\nQuit (Y/n)? ')
        print()
        if stop == 'Y':
            break
