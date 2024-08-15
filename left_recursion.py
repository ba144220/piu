import re

EMPTY = "ϵ"


def parse_grammar(grammar: str):
    index = 0
    tokens = [tok for tok in re.split(r"\s+", grammar) if tok != ""]
    grammar_dict = {}
    head = None
    while index < len(tokens):
        if index + 1 < len(tokens) and tokens[index + 1] == "->":
            head = tokens[index]
            index += 2
            grammar_dict[head] = [[]]
        elif tokens[index] == "|":
            assert head is not None
            grammar_dict[head].append([])
            index += 1
        else:
            grammar_dict[head][-1].append(tokens[index])
            index += 1
    for definition in grammar_dict.items():
        for branch in definition:
            if len(branch) == 0:
                branch.append(EMPTY)
    return grammar_dict


def eliminate_left_recursion(grammar: dict):
    new_grammar = grammar.copy()
    refs = list(grammar.keys())
    for i, ref_1 in enumerate(refs):
        for ref_2 in refs[:i]:
            extended = []

            for branch_1 in new_grammar[ref_1]:
                if branch_1[0] == ref_2:
                    for branch_2 in new_grammar[ref_2]:
                        extended.append(branch_2 + branch_1[1:])
                else:
                    extended.append(branch_1)

            new_grammar[ref_1] = extended

        has_direct_recursion = any(branch[0] == ref_1 for branch in new_grammar[ref_1])

        if not has_direct_recursion:
            continue

        helper_name = ref_1 + "'"
        while helper_name in new_grammar:
            helper_name += "'"
        new_grammar[helper_name] = []

        j = 0
        for k in range(len(new_grammar[ref_1])):
            if new_grammar[ref_1][k][0] == ref_1:
                new_grammar[helper_name].append(
                    new_grammar[ref_1][k][1:] + [helper_name]
                )
                continue

            if len(new_grammar[ref_1][k]) == 1 and new_grammar[ref_1][k][0] == EMPTY:
                new_grammar[ref_1][k] = [helper_name]
            else:
                new_grammar[ref_1][k].append(helper_name)

            new_grammar[ref_1][j] = new_grammar[ref_1][k]
            j += 1

        new_grammar[ref_1] = new_grammar[ref_1][:j]
        new_grammar[helper_name].append([EMPTY])

    return new_grammar


def print_grammar(grammar: dict):
    for key, tokens in grammar.items():
        tokens = [" ".join(token) for token in tokens]
        print(key, "->", " | ".join(tokens))


def test():
    grammar = """
    S -> S S + | S S * | a
    """
    grammar_dict = parse_grammar(grammar)
    print("Original Grammar:")
    print_grammar(grammar_dict)

    print("After Eliminating Left Recursion:")
    new_grammar_dict = eliminate_left_recursion(grammar_dict)
    print_grammar(new_grammar_dict)


if __name__ == "__main__":
    test()
