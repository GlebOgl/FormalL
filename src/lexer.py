import re
from .models import Token

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        
        # Описываем правила нашего метаязыка
        self.rules = [
            ('COMMENT',    r'#.*'),
            ('ARROW',      r'->'),
            ('PIPE',       r'\|'),
            ('SEMICOLON',  r';'),
            ('NON_TERM',   r'[A-Z][a-zA-Z0-9]*'),
            ('TERM',       r"'.*?'|\".*?\""),
            ('EPSILON',    r'eps'),
            ('NEWLINE',    r'\n'),
            ('SKIP',       r'[ \t]+'), 
            ('MISMATCH',   r'.'),
        ]
        self.regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.rules)

    def tokenize(self):
        line_num = 1
        line_start = 0
        
        for mo in re.finditer(self.regex, self.source_code):
            kind = mo.lastgroup
            value = mo.group()
            column = mo.start() - line_start + 1
            
            if kind == 'NEWLINE':
                line_start = mo.end()
                line_num += 1
                continue
            elif kind == 'SKIP' or kind == 'COMMENT':
                continue
            elif kind == 'MISMATCH':
                return f"Lexical error: Unexpected character '{value}' at {line_num}:{column}"
            
            self.tokens.append(Token(kind, value, line_num, column))
        
        return self.tokens
