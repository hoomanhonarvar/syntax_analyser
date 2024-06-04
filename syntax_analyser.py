
def first(grammar):
    first = {}

    for non_terminal in grammar:
        first[non_terminal] = set()

    while True:
        updated = False
        for non_terminal, productions in grammar.items():
            for production in productions:
                for symbol in production:
                    if symbol in first:
                        if len(first[symbol] - first[non_terminal]) > 0:
                            first[non_terminal] |= first[symbol]
                            updated = True
                        if 'ε' not in first[symbol]:
                            break
                else:
                    first[non_terminal].add('ε')
                    updated = True

        if not updated:
            break

    return first


def follow(grammar, first):
    follow = {non_terminal: set() for non_terminal in grammar}

    start_symbol = next(iter(grammar))
    follow[start_symbol].add('$')

    while True:
        updated = False
        for non_terminal, productions in grammar.items():
            for production in productions:
                for i, symbol in enumerate(production):
                    if symbol in grammar:
                        for j in range(i + 1, len(production)):
                            if production[j] in grammar:
                                if len(first[production[j]] - {'ε'}) > 0:
                                    if len(follow[production[j]] - follow[symbol]) > 0:
                                        follow[symbol] |= follow[production[j]]
                                        updated = True
                                    break
                                else:
                                    if len(follow[production[j]] - follow[symbol]) > 0:
                                        follow[symbol] |= follow[production[j]] - {'ε'}
                                        updated = True
                            else:
                                if len(follow[symbol] - follow[production[j]]) > 0:
                                    follow[production[j]] |= follow[symbol] - follow[production[j]]
                                    updated = True
                                break
                        else:
                            if len(follow[non_terminal] - follow[symbol]) > 0:
                                follow[symbol] |= follow[non_terminal]
                                updated = True

        if not updated:
            break

    return follow

