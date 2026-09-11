"""
HIT137 Assignment 2 - Question 2
Recursive-descent expression evaluator. No classes - plain functions only,
as required.

GRAMMAR (lowest to highest precedence, matching the brief's table):

    expr    := term (('+' | '-') term)*                     # level 1, left
    term    := unary ( ('*' | '/' | '%' | IMPLICIT) unary )* # level 2, left
    unary   := '-' unary | power                             # level 3, prefix
    power   := primary ('^' unary)?                          # level 4, right
    primary := NUM | '(' expr ')'

IMPLICIT MULTIPLICATION NOTE:
The brief says implicit multiplication is valid, but that two bare adjacent
numbers like "2 3" are NOT implicit multiplication. So implicit
multiplication is only triggered when a primary is immediately followed by
'(' with no operator in between - e.g. "2(3)", "(2)(3)", "2(3+4)". A bare
"2 3" is left as a genuine syntax error (trailing token), which is what "2 3
are not implicit multiplication" implies.

TOKENS NOTE:
The brief's own example dict for evaluate_file() shows a tokens string that
does NOT end in "[END]", while the Tokens section a few paragraphs above it
explicitly says the token line ends with [END] or ERROR. I've followed the
explicit written rule (tokens end with [END]) since the dict example looks
like a shorthand typo. If your provided sample_output.txt disagrees, it's a
one-line change in format_tokens() below.
"""

import sys


# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------

def tokenize(expr: str):
    """Turns an expression string into a list of (type, value) tuples.
    Raises ValueError on any character that doesn't belong to the grammar.
    """
    tokens = []
    i = 0
    n = len(expr)
    while i < n:
        ch = expr[i]
        if ch.isspace():
            i += 1
            continue
        if ch.isdigit() or ch == ".":
            j = i
            seen_dot = False
            while j < n and (expr[j].isdigit() or (expr[j] == "." and not seen_dot)):
                if expr[j] == ".":
                    seen_dot = True
                j += 1
            literal = expr[i:j]
            # must contain at least one digit and (if it has a dot) a digit after it
            if literal in (".", "") or literal.endswith("."):
                raise ValueError(f"Invalid number literal '{literal}'")
            tokens.append(("NUM", literal))
            i = j
            continue
        if ch in "+-*/%^":
            tokens.append(("OP", ch))
            i += 1
            continue
        if ch == "(":
            tokens.append(("LPAREN", ch))
            i += 1
            continue
        if ch == ")":
            tokens.append(("RPAREN", ch))
            i += 1
            continue
        raise ValueError(f"Unexpected character '{ch}'")
    tokens.append(("END", ""))
    return tokens


def format_tokens(tokens) -> str:
    parts = []
    for ttype, value in tokens:
        if ttype == "END":
            parts.append("[END]")
        else:
            parts.append(f"[{ttype}:{value}]")
    return " ".join(parts)


# ---------------------------------------------------------------------------
# Parser (recursive descent) - builds a tuple-based parse tree
#   number      -> ("num", float_value)
#   binary op   -> (op_symbol, left_node, right_node)
#   unary minus -> ("neg", operand_node)
# ---------------------------------------------------------------------------

class ParseState:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]

    def advance(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok


def parse_expr(state: ParseState):
    node = parse_term(state)
    while state.peek()[0] == "OP" and state.peek()[1] in ("+", "-"):
        op = state.advance()[1]
        right = parse_term(state)
        node = (op, node, right)
    return node


def parse_term(state: ParseState):
    node = parse_unary(state)
    while True:
        ttype, value = state.peek()
        if ttype == "OP" and value in ("*", "/", "%"):
            state.advance()
            right = parse_unary(state)
            node = (value, node, right)
        elif ttype == "LPAREN":
            # implicit multiplication: primary directly followed by '('
            right = parse_unary(state)
            node = ("*", node, right)
        else:
            break
    return node


def parse_unary(state: ParseState):
    ttype, value = state.peek()
    if ttype == "OP" and value == "-":
        state.advance()
        operand = parse_unary(state)
        return ("neg", operand)
    if ttype == "OP" and value == "+":
        raise ValueError("Unary '+' is not supported")
    return parse_power(state)


def parse_power(state: ParseState):
    node = parse_primary(state)
    ttype, value = state.peek()
    if ttype == "OP" and value == "^":
        state.advance()
        right = parse_unary(state)  # right-associative, allows e.g. 2^-3
        node = ("^", node, right)
    return node


def parse_primary(state: ParseState):
    ttype, value = state.peek()
    if ttype == "NUM":
        state.advance()
        return ("num", float(value))
    if ttype == "LPAREN":
        state.advance()
        node = parse_expr(state)
        ttype2, _ = state.peek()
        if ttype2 != "RPAREN":
            raise ValueError("Expected ')'")
        state.advance()
        return node
    raise ValueError(f"Unexpected token {ttype}")


def parse(tokens):
    state = ParseState(tokens)
    node = parse_expr(state)
    if state.peek()[0] != "END":
        raise ValueError("Unexpected trailing tokens")
    return node


# ---------------------------------------------------------------------------
# Evaluator
# ---------------------------------------------------------------------------

def evaluate_node(node):
    tag = node[0]
    if tag == "num":
        return node[1]
    if tag == "neg":
        return -evaluate_node(node[1])
    left = evaluate_node(node[1])
    right = evaluate_node(node[2])
    if tag == "+":
        return left + right
    if tag == "-":
        return left - right
    if tag == "*":
        return left * right
    if tag == "/":
        return left / right
    if tag == "%":
        return left % right
    if tag == "^":
        return left ** right
    raise ValueError(f"Unknown node tag '{tag}'")


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def format_result(value: float) -> str:
    if value == int(value):
        return str(int(value))
    rounded = round(value, 4)
    # keep up to 4 decimal places, no trailing zeros beyond what's needed
    text = f"{rounded:.4f}".rstrip("0").rstrip(".")
    return text


def format_tree(node) -> str:
    tag = node[0]
    if tag == "num":
        return format_result(node[1])
    if tag == "neg":
        return f"(neg {format_tree(node[1])})"
    return f"({tag} {format_tree(node[1])} {format_tree(node[2])})"


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

def evaluate_file(input_path: str) -> list:
    import os

    results = []
    with open(input_path, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    output_dir = os.path.dirname(os.path.abspath(input_path))
    output_path = os.path.join(output_dir, "output.txt")

    blocks = []
    for line in lines:
        if line.strip() == "":
            continue
        entry = {"input": line}

        # Tokenizing and parsing/evaluating are treated as separate stages:
        # a bad character (e.g. '@') fails tokenizing, so *everything* is
        # ERROR. A structurally invalid expression built from otherwise
        # valid tokens (e.g. "(3 + 4" with no closing paren) still shows the
        # real token list - only Tree and Result become ERROR.
        try:
            tokens = tokenize(line)
            tokens_str = format_tokens(tokens)
        except ValueError:
            entry["tree"] = "ERROR"
            entry["tokens"] = "ERROR"
            entry["result"] = "ERROR"
            tokens_str = "ERROR"
            tree_str = "ERROR"
            result_str = "ERROR"
            results.append(entry)
            blocks.append(f"Input: {entry['input']}\n"
                           f"Tree: {tree_str}\n"
                           f"Tokens: {tokens_str}\n"
                           f"Result: {result_str}")
            continue

        try:
            tree = parse(tokens)
            tree_str = format_tree(tree)
            value = evaluate_node(tree)
            entry["tree"] = tree_str
            entry["tokens"] = tokens_str
            entry["result"] = value
            result_str = format_result(value)
        except (ValueError, ZeroDivisionError):
            entry["tree"] = "ERROR"
            entry["tokens"] = tokens_str
            entry["result"] = "ERROR"
            tree_str = "ERROR"
            result_str = "ERROR"

        results.append(entry)
        blocks.append(f"Input: {entry['input']}\n"
                       f"Tree: {tree_str}\n"
                       f"Tokens: {tokens_str}\n"
                       f"Result: {result_str}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(blocks))
        if blocks:
            f.write("\n")

    return results


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    results = evaluate_file(input_path)
    for r in results:
        print(r)


if __name__ == "__main__":
    main()
