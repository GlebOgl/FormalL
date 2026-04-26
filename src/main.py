import sys
import os
from .lexer import Lexer

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_file>")
        return

    input_path = sys.argv[1]
    
    if not os.path.exists(input_path):
        print(f"Error: File '{input_path}' not found.")
        return

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    lexer = Lexer(source_code)
    result = lexer.tokenize()

    output_path = input_path + ".out"
    
    if isinstance(result, str):
        print(result)
    else:
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for token in result:
                    f.write(f"{token.type:<12} | {token.value:<15} | Line: {token.line:<3} | Col: {token.column}\n")
            print(f"Success! Lexical analysis saved to {output_path}")
        except Exception as e:
            print(f"Error writing output: {e}")

if __name__ == "__main__":
    main()
