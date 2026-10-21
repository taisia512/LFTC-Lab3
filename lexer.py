
import re

from tokens import KEYWORDS
from symbol_table import SymbolTable

# regular expressions for identifiers and constants
IDENTIFIER_PATTERN = r"[a-zA-Z][a-zA-Z0-9_]*"
INTEGER_PATTERN = r"0|[1-9][0-9]*"
REAL_PATTERN = r"(?:0|[1-9][0-9]*)\.[0-9]+"
STRING_PATTERN = r'"[^"\n]*"'


# recognize tokens from the source program
def tokenize(source_code):
    tokens = []
    errors = []

    token_pattern = re.compile(
        r'(?P<INVALID_STRING>"[^"\n]*(?=\n|$))'
        rf'|(?P<STRING>{STRING_PATTERN})'
        r'|(?P<NUMBER>[0-9][a-zA-Z0-9_.]*)'
        r'|(?P<INVALID_IDENTIFIER>_[a-zA-Z0-9_]*)'
        rf'|(?P<IDENTIFIER>{IDENTIFIER_PATTERN})'
        r'|(?P<OPERATOR>:=|==|!=|>=|<=|[+\-*/%><])'
        r'|(?P<SEPARATOR>[\[\](),])'
        r'|(?P<WHITESPACE>\s+)'
        r'|(?P<INVALID>.)'
    )

    for match in token_pattern.finditer(source_code):
        token_type = match.lastgroup
        token_value = match.group()

        if token_type == "WHITESPACE":
            continue

        # check if the number is valid
        if token_type == "NUMBER":
            if re.fullmatch(INTEGER_PATTERN, token_value):
                token_type = "INTEGER"
            elif re.fullmatch(REAL_PATTERN, token_value):
                token_type = "REAL"
            else:
                token_type = "INVALID_NUMBER"

        # check if the identifier is a keyword
        if token_type == "IDENTIFIER" and token_value in KEYWORDS:
            token_type = "KEYWORD"

        # collect lexical errors
        if token_type in (
            "INVALID",
            "INVALID_NUMBER",
            "INVALID_STRING",
            "INVALID_IDENTIFIER"
        ):
            line = source_code.count("\n", 0, match.start()) + 1

            errors.append(
                f"Invalid token '{token_value}' at line {line}"
            )
        else:
            tokens.append((token_type, token_value))

    return tokens, errors


# read the source program and display the results
if __name__ == "__main__":
    with open("program.txt", "r", encoding="utf-8") as file:
        source_code = file.read()

    tokens, errors = tokenize(source_code)

    print("TOKENS:")
    for token_type, token_value in tokens:
        print(f"{token_type}: {token_value}")

    print("\nLEXICAL ERRORS:")
    if errors:
        for error in errors:
            print(error)
    else:
        print("No lexical errors found.")

    # create and populate the symbol table
    st = SymbolTable()

    for token_type, token_value in tokens:
        if token_type in ("IDENTIFIER", "INTEGER", "REAL", "STRING"):
            st.add(token_value)

    print("\nSYMBOL TABLE:")
    st.display()

    # generate the program internal form
    pif = []

    for token_type, token_value in tokens:
        if token_type in ("IDENTIFIER", "INTEGER", "REAL", "STRING"):
            position = st.search(token_value)

            if token_type == "IDENTIFIER":
                pif_token = "IDENTIFIER"
            else:
                pif_token = "CONSTANT"

            pif.append((pif_token, position))
        else:
            pif.append((token_value, (-1, -1)))

    print("\nPROGRAM INTERNAL FORM:")
    for token, position in pif:
        print(f"{token} -> {position}")

    # save the program internal form
    with open("PIF.txt", "w", encoding="utf-8") as file:
        for token, position in pif:
            file.write(f"{token} -> {position}\n")

    # save the symbol table
    with open("ST.txt", "w", encoding="utf-8") as file:
        for position, bucket in enumerate(st.table):
            for index, value in enumerate(bucket):
                file.write(f"{value} -> ({position}, {index})\n")

    # save lexical errors
    with open("lexical_errors.txt", "w", encoding="utf-8") as file:
        if errors:
            for error in errors:
                file.write(error + "\n")
        else:
            file.write("No lexical errors found.\n")

    print("\nResults saved to files.")
