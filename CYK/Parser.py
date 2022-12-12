import sys


class Parser:

    def __init__(self, grammar: str, verbose: bool = True):
        self.grammar = self.remove_space(grammar)
        self.verbose = verbose
        try:
            self.productions = self.get_productions(grammar)
        except Exception as e:
            print('Error: Your grammar is invalid.')
            sys.exit(1)

        if not self.is_cnf_form(self.productions):
            print('Error: Your grammar is not in CNF form.')
            sys.exit(1)
        self.alphabet = self.get_alphabet(self.productions)

        self.print_grammar()
        self.print_alphabet()

    def remove_space(self, s : str) -> str:
        return ''.join(s.split())

    def is_cnf_form(self, productions: dict) -> bool:
        for lhs, rhs_list in productions.items():
            for rhs in rhs_list:
                if len(rhs) == 1 and rhs.islower():
                    pass
                elif len(rhs) == 2 and rhs.isupper():
                    pass
                else:
                    return False
        return True

    def get_alphabet(self, productions: dict) -> set:
        alphabet = set()
        for lhs, rhs_list in productions.items():
            for rhs in rhs_list:
                if len(rhs) == 1 and rhs.islower():
                    alphabet.add(rhs)
        return alphabet

    def get_productions(self, grammar: str) -> dict:
        productions = {}
        for production in self.remove_space(grammar).split(','):
            lhs = production.split('->')[0]
            rhs = production.split('->')[1].split('|')
            productions[lhs] = rhs
        return productions

    def parse(self, word: str) -> bool:
        word = self.remove_space(word)
        table = self.build_table(word)

        self.print_msg('Word:')
        self.print_msg(word)
        self.print_table(table, word)

        self.print_msg('Results:')
        if 'S' in len(table[0][len(word) - 1]):
            self.print_msg(f'w ∈ L(G) for the given w and G')
            self.print_msg('The word is in the language generated by the grammar.')
            return True
        else:
            self.print_msg(f'w ∉ L(G) for the given w and G')
            self.print_msg('The word is *not* in the language generated by the grammar.')
            return False

    def build_table(self, word: str) -> list:
        table = [[set([]) for _ in range(len(word))] for _ in range(len(word))]
        for i, char in enumerate(word):
            if char not in self.alphabet:
                print(f'Error: The letter {char} is in w but not in the alphabet.')
                sys.exit(1)
            for lhs, rhs_list in self.productions.items():
                for rhs in rhs_list:
                    if len(rhs) == 1 and rhs == char:
                        table[i][i].add(lhs)

            self.solve_table(table, i)

        return table

    def solve_table(self, table: list, i: int) -> None:
        for j in range(i, -1, -1):
            for k in range(j, i + 1):
                for lhs, rhs_list in self.productions.items():
                    for rhs in rhs_list:
                        if k + 1 < len(table) and len(rhs) == 2 and rhs[0] in table[j][k] and rhs[1] in table[k + 1][i]:
                            table[j][i].add(lhs)

    def print_msg(self, msg) -> None:
        if self.verbose:
            print(msg)

    def print_table(self, table: list, word: str) -> None:
        print('Parse Table:')
        if self.verbose:
            print(''.ljust(5), end=' ')
            for char in word:
                print(char.ljust(18), end=' ')
            print()
            for i, row in enumerate(table):
                print(word[i].ljust(5), end=' ')
                for j, col in enumerate(row):
                    if col:
                        print(str(col).ljust(18), end=' ')
                print()

    def print_alphabet(self) -> None:
        self.print_msg('Alphabet:')
        self.print_msg(f'{self.alphabet}')

    def print_grammar(self) -> None:
        print('Grammar:')
        for lhs, rhs_list in self.productions.items():
            rhs = '|'.join(rhs_list)
            self.print_msg(f'{lhs} -> {rhs}')

