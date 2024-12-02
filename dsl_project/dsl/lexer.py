import re

# dictionary of token types and their corresponding regex patterns
TOKENS = {
    'KEYWORD_SET': r'\bset\b',  # Matches the keyword "set"
    'KEYWORD_TO': r'\bto\b',    # Matches the keyword "to"
    'KEYWORD_SHOW': r'\bshow\b', # Matches the keyword "show"
    'IDENTIFIER': r'\b[A-Z][a-zA-Z0-9]*\b',  # Matches identifiers starting with an uppercase letter
    'NUMBER': r'\d+(\.\d+)?',  # Matches integers or decimal numbers
    'OPERATOR': r'(\*\*|[\+\-\*/])',  # Matches operators like +, -, *, /, and ** (exponentiation)
    'FUNCTION': r'\b(sin|cos|tan|sqrt|log|exp|asin|acos|atan|ceil|floor|fabs|factorial|pow)\b',  # Matches function names
    'LPAREN': r'\(',  # Matches left parenthesis '('
    'RPAREN': r'\)',  # Matches right parenthesis ')'
    'SEMICOLON': r';',  # Matches semicolon ';'
    'COMMENT': r'\$\$.*',  # Matches comments starting with '$$'
    'COMMA': r','  # Matches comma ','
}

def lexer(code):
    """
    Tokenizes the input code based on predefined token patterns.

    Args:
        code (str): The input code as a string.

    Returns:
        list of tuples: A list of (token_type, token_value) pairs.

    Raises:
        ValueError: If an illegal character is encountered in the input code.
    """
    tokens = []  # List to store the matched tokens
    pos = 0  # Current position in the input code

    while pos < len(code):  # Loop through the entire code
        match = None  # To store the regex match

        # Skip whitespace characters
        if code[pos].isspace():
            pos += 1
            continue

        # Attempt to match each token type
        for token_type, pattern in TOKENS.items():
            regex = re.compile(pattern)  # Compile the regex pattern
            match = regex.match(code, pos)  # Check if the pattern matches at the current position

            if match:
                if token_type != 'COMMENT':  # Ignore tokens of type 'COMMENT'
                    # Add the token type and matched value to the token list
                    tokens.append((token_type, match.group()))
                # Move the position to the end of the matched token
                pos = match.end()
                break

        # If no token matches, raise an error for the illegal character
        if not match:
            raise ValueError(f"Illegal character at position {pos}: '{code[pos]}'")

    return tokens  # Return the list of tokens
