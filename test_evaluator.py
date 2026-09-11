

from evaluator import tokenize, parse, evaluate, tree_to_string, tokens_to_string, format_result


def run_case(expr, expect_error=False, expect_tree=None, expect_result=None):
    try:
        tokens = tokenize(expr)
        tree = parse(tokens)
        value = evaluate(tree)
    except (ValueError, ZeroDivisionError):
        if expect_error:
            print(f"PASS: {expr!r} -> ERROR (expected)")
        else:
            print(f"FAIL: {expr!r} -> unexpected ERROR")
        return

    if expect_error:
        print(f"FAIL: {expr!r} -> got {value}, expected ERROR")
        return

    tree_str = tree_to_string(tree)
    result_str = format_result(value)

    ok = True
    if expect_tree is not None and tree_str != expect_tree:
        ok = False
    if expect_result is not None and result_str != expect_result:
        ok = False

    status = "PASS" if ok else "FAIL"
    print(f"{status}: {expr!r} -> tree={tree_str} result={result_str}")


def main():
    # Basic operators
    run_case("3 + 5", expect_tree="(+ 3 5)", expect_result="8")
    run_case("10 % 3", expect_tree="(% 10 3)", expect_result="1")

    # Right-associative exponentiation: 2^3^2 = 2^(3^2) = 512
    run_case("2 ^ 3 ^ 2", expect_tree="(^ 2 (^ 3 2))", expect_result="512")

    # Unary negation binds tighter than * / %, looser than ^
    run_case("3 * -2", expect_tree="(* 3 (neg 2))", expect_result="-6")
    run_case("-2 ^ 2", expect_tree="(neg (^ 2 2))", expect_result="-4")
    run_case("--5", expect_tree="(neg (neg 5))", expect_result="5")

    # Unary + is not supported -> ERROR
    run_case("+5", expect_error=True)

    # Nested parentheses
    run_case("((2+3)*(4-1))", expect_tree="(* (+ 2 3) (- 4 1))", expect_result="15")

    # Implicit multiplication (number next to parenthesis)
    run_case("2(3+4)", expect_tree="(* 2 (+ 3 4))", expect_result="14")

    # Two adjacent numbers are NOT implicit multiplication -> ERROR
    run_case("2 3", expect_error=True)

    # Division / modulo by zero -> ERROR
    run_case("5 / 0", expect_error=True)
    run_case("5 % 0", expect_error=True)

    # Malformed number: leading dot is invalid (must start with a digit)
    run_case(".5", expect_error=True)

    # Malformed number: trailing dot is invalid
    run_case("5.", expect_error=True)

    # Invalid character
    run_case("3 @ 5", expect_error=True)

    # Mismatched parentheses
    run_case("(2 + 3", expect_error=True)

    # Token string sanity check
    tokens = tokenize("-5")
    print("Tokens for '-5':", tokens_to_string(tokens), "(expect [OP:-] [NUM:5] [END])")


if __name__ == "__main__":
    main()
