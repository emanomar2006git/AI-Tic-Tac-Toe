from collections import deque

HUMAN = "X"
AI = "O"
EMPTY = " "
def print_board(board):
    print()
    for row in range(3):
        print(" | ".join(
            board[row * 3 + col] if board[row * 3 + col] != EMPTY
            else str(row * 3 + col + 1)
            for col in range(3)
        ))
        if row < 2:
            print("---------")
    print()

def get_winner(board):
    winning_lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    for a, b, c in winning_lines:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]

    return None

def is_draw(board):
    return get_winner(board) is None and EMPTY not in board



def available_moves(board):
    return [i for i in range(9) if board[i] == EMPTY]



def evaluate(board):
    winner = get_winner(board)

    if winner == AI:
        return 1
    elif winner == HUMAN:
        return -1
    elif is_draw(board):
        return 0

    return None



def bfs_build_game_tree(start_board, next_player):

    start_state = (tuple(start_board), next_player)
    queue = deque([start_state])
    visited = {start_state}
    children = {}

    while queue:
        state = queue.popleft()
        board_tuple, player = state
        board = list(board_tuple)

        if evaluate(board) is not None:
            children[state] = []
            continue

        children[state] = []

        for move in available_moves(board):
            new_board = board.copy()
            new_board[move] = player

            next_turn = HUMAN if player == AI else AI
            new_state = (tuple(new_board), next_turn)

            children[state].append((move, new_state))

            if new_state not in visited:
                visited.add(new_state)
                queue.append(new_state)

    return start_state, children, len(visited)



def minimax_value(state, children, memo):

    if state in memo:
        return memo[state]

    board_tuple, player = state
    score = evaluate(list(board_tuple))

    if score is not None:
        memo[state] = score
        return score

    scores = [
        minimax_value(child, children, memo)
        for _, child in children[state]
    ]

    if player == AI:
        best_score = max(scores)
    else:
        best_score = min(scores)

    memo[state] = best_score
    return best_score



def choose_ai_move(board):

    start_state, children, explored_nodes = bfs_build_game_tree(board, AI)

    memo = {}
    best_move = None
    best_score = float("-inf")

    for move, child_state in children[start_state]:

        score = minimax_value(child_state, children, memo)

        if score > best_score:
            best_score = score
            best_move = move

    return best_move, explored_nodes



def human_turn(board):

    while True:
        choice = input("Choose a cell (1-9): ")

        if not choice.isdigit():
            print("Please enter a number.")
            continue

        position = int(choice) - 1

        if position < 0 or position > 8:
            print("Invalid position!")
        elif board[position] != EMPTY:
            print("Cell already occupied!")
        else:
            board[position] = HUMAN
            break



def play_game():

    board = [EMPTY] * 9

    print("Welcome to AI Tic-Tac-Toe!")
    print("You are X and AI is O.")

    while True:

        print_board(board)

        
        human_turn(board)

        if get_winner(board) == HUMAN:
            print_board(board)
            print("You Win!")
            break

        if is_draw(board):
            print_board(board)
            print("Draw!")
            break

        
        move, explored_nodes = choose_ai_move(board)

        if move is None:
            break

        board[move] = AI

        print("AI chooses position:", move + 1)
        print("BFS explored nodes:", explored_nodes)

        if get_winner(board) == AI:
            print_board(board)
            print("AI Wins!")
            break

        if is_draw(board):
            print_board(board)
            print("Draw!")
            break



if __name__ == "__main__":
    play_game()