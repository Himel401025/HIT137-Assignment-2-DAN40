# evaluator.py

def tokenize(expr):
    tokens = []
    i = 0

    while i < len(expr):
        ch = expr[i]

        if ch.isspace():
            i += 1
            continue

        if ch.isdigit() or ch == '.':
            start = i
            dot_count = 0

            while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                if expr[i] == '.':
                    dot_count += 1
                i += 1

            num_str = expr[start:i]

            if dot_count > 1 or num_str == '.':
                raise ValueError("Invalid number")

            tokens.append(("NUM", float(num_str)))
            continue

        if ch in "+-*/":
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

        raise ValueError("Invalid character")

    tokens.append(("END", ""))
    return tokens


def current_token(tokens, pos):
    return tokens[pos]


def is_factor_start(token):
    return token[0] in ("NUM", "LPAREN") or (token[0] == "OP" and token[1] == "-")


def parse_expression(tokens, pos):
    left, pos = parse_term(tokens, pos)

    while True:
        token = current_token(tokens, pos)
        if token[0] == "OP" and token[1] in "+-":
            op = token[1]
            pos += 1
            right, pos = parse_term(tokens, pos)
            left = (op, left, right)
        else:
            break

    return left, pos


def parse_term(tokens, pos):
    left, pos = parse_factor(tokens, pos)

    while True:
        token = current_token(tokens, pos)

        if token[0] == "OP" and token[1] in "*/":
            op = token[1]
            pos += 1
            right, pos = parse_factor(tokens, pos)
            left = (op, left, right)

        elif is_factor_start(token):
            right, pos = parse_factor(tokens, pos)
            left = ("*", left, right)

        else:
            break

    return left, pos


def parse_factor(tokens, pos):
    token = current_token(tokens, pos)

    if token[0] == "OP" and token[1] == "-":
        pos += 1
        operand, pos = parse_factor(tokens, pos)
        return ("neg", operand), pos

    if token[0] == "NUM":
        return token[1], pos + 1

    if token[0] == "LPAREN":
        pos += 1
        node, pos = parse_expression(tokens, pos)

        if current_token(tokens, pos)[0] != "RPAREN":
            raise ValueError("Missing closing parenthesis")

        pos += 1
        return node, pos

    if token[0] == "OP" and token[1] == "+":
        raise ValueError("Unary plus not supported")

    raise ValueError("Invalid syntax")


def format_number(value):
    if float(value).is_integer():
        return str(int(value))
    return str(value)


def tree_to_string(node):
    if isinstance(node, float):
        return format_number(node)

    if isinstance(node, tuple) and len(node) == 2 and node[0] == "neg":
        return f"(neg {tree_to_string(node[1])})"

    op, left, right = node
    return f"({op} {tree_to_string(left)} {tree_to_string(right)})"


def evaluate_tree(node):
    if isinstance(node, float):
        return node

    if isinstance(node, tuple) and len(node) == 2 and node[0] == "neg":
        return -evaluate_tree(node[1])

    op, left, right = node
    left_val = evaluate_tree(left)
    right_val = evaluate_tree(right)

    if op == "+":
        return left_val + right_val
    if op == "-":
        return left_val - right_val
    if op == "*":
        return left_val * right_val
    if op == "/":
        return left_val / right_val

    raise ValueError("Unknown operator")


def tokens_to_string(tokens):
    parts = []

    for token_type, value in tokens:
        if token_type == "NUM":
            parts.append(f"[NUM:{format_number(value)}]")
        elif token_type == "OP":
            parts.append(f"[OP:{value}]")
        elif token_type == "LPAREN":
            parts.append(f"[LPAREN:{value}]")
        elif token_type == "RPAREN":
            parts.append(f"[RPAREN:{value}]")
        elif token_type == "END":
            parts.append("[END]")

    return " ".join(parts)


def format_result(value):
    if isinstance(value, str):
        return value

    rounded = round(value, 4)

    if float(rounded).is_integer():
        return str(int(rounded))

    return f"{rounded:.4f}"


def process_expression(expr):
    tokens = tokenize(expr)
    tree, pos = parse_expression(tokens, 0)

    if current_token(tokens, pos)[0] != "END":
        raise ValueError("Extra input after valid expression")

    result = evaluate_tree(tree)

    return {
        "input": expr,
        "tree": tree_to_string(tree),
        "tokens": tokens_to_string(tokens),
        "result": result if isinstance(result, str) else round(result, 4)
    }


def evaluate_file(input_path: str) -> list[dict]:
    results = []

    with open(input_path, "r", encoding="utf-8") as infile:
        lines = infile.readlines()

    output_path = "output.txt"

    with open(output_path, "w", encoding="utf-8") as outfile:
        for raw_line in lines:
            expr = raw_line.rstrip("\n")

            try:
                result_data = process_expression(expr)

                results.append(result_data)

                outfile.write(f"{result_data['input']}\n")
                outfile.write(f"{result_data['tree']}\n")
                outfile.write(f"{result_data['tokens']}\n")
                outfile.write(f"{format_result(result_data['result'])}\n\n")

            except Exception:
                error_data = {
                    "input": expr,
                    "tree": "ERROR",
                    "tokens": "ERROR",
                    "result": "ERROR"
                }

                results.append(error_data)

                outfile.write(f"{expr}\n")
                outfile.write("ERROR\n")
                outfile.write("ERROR\n")
                outfile.write("ERROR\n\n")

    return results




results = evaluate_file("sample_input.txt")
print(results)
