def alpha_beta_search(state, game_tree):
    value = max_value(state, float('-inf'), float('inf'), game_tree, depth=0)
    return value

def max_value(state, alpha, beta, game_tree, depth):
    if state not in game_tree:
        return state

    v = float('-inf')
    print(f"{'  '*depth}MAX(state={state}, α={alpha}, β={beta})")
    for child in game_tree[state]:
        v_child = min_value(child, alpha, beta, game_tree, depth+1)
        v = max(v, v_child)
        print(f"{'  '*(depth+1)}MAX avaliando filho {child}: v={v}, α={alpha}, β={beta}")
        if v >= beta:
            print(f"{'  '*(depth+1)}⛔ Poda Beta em {child} (v={v} ≥ β={beta})")
            return v
        alpha = max(alpha, v)
    return v

def min_value(state, alpha, beta, game_tree, depth):
    if state not in game_tree:
        return state

    v = float('inf')
    print(f"{'  '*depth}MIN(state={state}, α={alpha}, β={beta})")
    for child in game_tree[state]:
        v_child = max_value(child, alpha, beta, game_tree, depth+1)
        v = min(v, v_child)
        print(f"{'  '*(depth+1)}MIN avaliando filho {child}: v={v}, α={alpha}, β={beta}")
        if v <= alpha:
            print(f"{'  '*(depth+1)}⛔ Poda Alpha em {child} (v={v} ≤ α={alpha})")
            return v
        beta = min(beta, v)
    return v

game_tree = {
    "MAX": ["MIN1", "MIN2", "MIN3"],
    "MIN1": [3, 12, 8],
    "MIN2": [2, 4, 6],
    "MIN3": [14, 5, 2]
}

resultado = alpha_beta_search("MAX", game_tree)
resultado