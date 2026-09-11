import os
import sys

def tokenize(line):
    tokens = []
    i = 0
    n = len(line)
    while i < n:
        ch = line[i]

        if ch.isspace():
            i += 1
            continue

        if ch.isdigit() or ch == ".":
            j = i
            dot_used = False
            while j < n and (line[j].isdigit() or (line[j] == "." and not dot_used)):
                if line[j] == ".":
                    dot_used = True
                j += 1
            num_text = line[i:j]
            if num_text == "." or num_text.endswith("."):
                raise ValueError("bad number")
            tokens.append(("NUM", num_text))
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

        raise ValueError("bad character: " + ch)

    tokens.append(("END", ""))
    return tokens

def tokens_to_string(tokens):
    out = []
    for t_type, t_val in tokens:
        if t_type == "END":
            out.append("[END]")
        else:
            out.append("[" + t_type + ":" + t_val + "]")
    return " ".join(out)

def current(state):
    return state[0][state[1]]

def next_token(state):
    tok = state[0][state[1]]
    state[1] += 1
    return tok

def parse_expr(state):
    node = parse_term(state)
    while current(state)[0] == "OP" and current(state)[1] in ("+", "-"):
        op = next_token(state)[1]
        right = parse_term(state)
        node = (op, node, right)
    return node

def parse_term(state):
    node = parse_unary(state)
    while True:
        t_type, t_val = current(state)
        if t_type == "OP" and t_val in ("*", "/", "%"):
            next_token(state)
            right = parse_unary(state)
            node = (t_val, node, right)
        elif t_type == "LPAREN":
            right = parse_unary(state)
            node = ("*", node, right)
        else:
            break
    return node

def parse_unary(state):
    t_type, t_val = current(state)
    if t_type == "OP" and t_val == "-":
        next_token(state)
        operand = parse_unary(state)
        return ("neg", operand)
    if t_type == "OP" and t_val == "+":
        raise ValueError("unary plus not allowed")
    return parse_power(state)

def parse_power(state):
    node = parse_primary(state)
    t_type, t_val = current(state)
    if t_type == "OP" and t_val == "^":
        next_token(state)
        right = parse_unary(state)
        node = ("^", node, right)
    return node

def parse_primary(state):
    t_type, t_val = current(state)
    if t_type == "NUM":
        next_token(state)
        return ("num", float(t_val))
    if t_type == "LPAREN":
        next_token(state)
        node = parse_expr(state)
        if current(state)[0] != "RPAREN":
            raise ValueError("missing closing bracket")
        next_token(state)
        return node
    raise ValueError("unexpected token")

def parse(tokens):
    state = [tokens, 0]
    node = parse_expr(state)
    if current(state)[0] != "END":
        raise ValueError("leftover tokens")
    return node

def evaluate(node):
    tag = node[0]
    if tag == "num":
        return node[1]
    if tag == "neg":
        return -evaluate(node[1])

    left = evaluate(node[1])
    right = evaluate(node[2])
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

def tree_to_string(node):
    tag = node[0]
    if tag == "num":
        return format_result(node[1])
    if tag == "neg":
        return "(neg " + tree_to_string(node[1]) + ")"
    return "(" + tag + " " + tree_to_string(node[1]) + " " + tree_to_string(node[2]) + ")"

def format_result(value):
    if value == int(value):
        return str(int(value))
    rounded = round(value, 4)
    text = ("%.4f" % rounded).rstrip("0").rstrip(".")
    return text

def evaluate_file(input_path):
    results = []

    f = open(input_path, "r", encoding="utf-8")
    lines = [line.rstrip("\n") for line in f]
    f.close()

    out_dir = os.path.dirname(os.path.abspath(input_path))
    out_path = os.path.join(out_dir, "output.txt")

    blocks = []
    for line in lines:
        if line.strip() == "":
            continue

        entry = {"input": line}

        try:
            tokens = tokenize(line)
            tokens_str = tokens_to_string(tokens)
        except ValueError:
            entry["tree"] = "ERROR"
            entry["tokens"] = "ERROR"
            entry["result"] = "ERROR"
            results.append(entry)
            blocks.append("Input: " + line + "\nTree: ERROR\nTokens: ERROR\nResult: ERROR")
            continue

        try:
            tree = parse(tokens)
            tree_str = tree_to_string(tree)
        except ValueError:
            entry["tree"] = "ERROR"
            entry["tokens"] = tokens_str
            entry["result"] = "ERROR"
            results.append(entry)
            blocks.append("Input: " + line + "\nTree: ERROR\nTokens: " + tokens_str + "\nResult: ERROR")
            continue

        entry["tree"] = tree_str
        entry["tokens"] = tokens_str

        try:
            value = evaluate(tree)
            result_str = format_result(value)
            entry["result"] = value
        except (ValueError, ZeroDivisionError):
            result_str = "ERROR"
            entry["result"] = "ERROR"

        results.append(entry)
        blocks.append("Input: " + line + "\nTree: " + tree_str + "\nTokens: " + tokens_str + "\nResult: " + result_str)

    out = open(out_path, "w", encoding="utf-8")
    out.write("\n\n".join(blocks))
    if blocks:
        out.write("\n")
    out.close()

    return results

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    results = evaluate_file(path)
    for r in results:
        print(r)

if __name__ == "__main__":
    main()
