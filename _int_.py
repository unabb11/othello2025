# Generation ID: Hutch_1764574009837_lk2oe34c5 (前半)

def myai(board, color):
    """
    オセロAI: 四つ角戦略 + 相手の選択肢削減 + 3手先読み
    """
    BLACK, WHITE = 1, 2
    opponent = WHITE if color == BLACK else BLACK
    size = len(board)

    def is_valid_move(b, col, row, c):
        if b[row][col] != 0:
            return False
        directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            found_opponent = False
            while 0 <= nr < size and 0 <= nc < size:
                if b[nr][nc] == 0:
                    break
                if b[nr][nc] == opponent if c == color else c:
                    found_opponent = True
                    nr, nc = nr + dr, nc + dc
                elif found_opponent:
                    return True
                else:
                    break
            if nr < 0 or nr >= size or nc < 0 or nc >= size:
                if found_opponent:
                    continue
        return any(is_line_valid(b, col, row, c, dr, dc) for dr, dc in directions)

    def is_line_valid(b, col, row, c, dr, dc):
        nr, nc = row + dr, col + dc
        found_opponent = False
        opp = opponent if c == color else color
        while 0 <= nr < size and 0 <= nc < size:
            if b[nr][nc] == 0:
                return False
            if b[nr][nc] == opp:
                found_opponent = True
            elif b[nr][nc] == c and found_opponent:
                return True
            else:
                return False
            nr, nc = nr + dr, nc + dc
        return False

    def get_valid_moves(b, c):
        moves = []
        for r in range(size):
            for col in range(size):
                if is_valid_move(b, col, r, c):
                    moves.append((col, r))
        return moves

    def apply_move(b, col, row, c):
        new_b = [r[:] for r in b]
        new_b[row][col] = c
        directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        for dr, dc in directions:
            flip_line(new_b, col, row, c, dr, dc)
        return new_b

    def flip_line(b, col, row, c, dr, dc):
        nr, nc = row + dr, col + dc
        opp = opponent if c == color else color
        flips = []
        while 0 <= nr < size and 0 <= nc < size and b[nr][nc] == opp:
            flips.append((nr, nc))
            nr, nc = nr + dr, nc + dc
        if 0 <= nr < size and 0 <= nc < size and b[nr][nc] == c:
            for fr, fc in flips:
                b[fr][fc] = c

    def evaluate(b, c):
        corners = [(0,0), (0,size-1), (size-1,0), (size-1,size-1)]
        corner_score = sum(10 if b[r][col] == c else -10 if b[r][col] != 0 else 0
                          for r, col in corners)

        opp_moves = len(get_valid_moves(b, opponent if c == color else color))
        mobility_score = -opp_moves * 5

        piece_count = sum(1 for row in b for cell in row if cell == c)
        return corner_score + mobility_score + piece_count

    def minimax(b, c, depth, is_max):
        if depth == 0:
            return evaluate(b, color), None

        moves = get_valid_moves(b, c)
        if not moves:
            moves_opp = get_valid_moves(b, opponent if c == color else color)
            if not moves_opp:
                return evaluate(b, color), None
            return minimax(b, opponent if c == color else color, depth - 1, not is_max)

        if is_max:
            max_eval = float('-inf')
            best_move = None
            for col, row in moves:
                new_b = apply_move(b, col, row, c)
                eval_score, _ = minimax(new_b, opponent if c == color else color, depth - 1, False)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = (col, row)
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for col, row in moves:
                new_b = apply_move(b, col, row, c)
                eval_score, _ = minimax(new_b, color if c == opponent else opponent, depth - 1, True)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = (col, row)
            return min_eval, best_move

    valid_moves = get_valid_moves(board, color)
    if not valid_moves:
        return None

    _, best_move = minimax(board, color, 3, True)
    return best_move if best_move else valid_moves[0]

# Generation ID: Hutch_1764574009837_lk2oe34c5 (後半)
