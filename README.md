# AI Tic-Tac-Toe

A command-line Tic-Tac-Toe game where you play against an unbeatable AI. The AI builds the full game tree with **Breadth-First Search (BFS)**, evaluates it with **Minimax**, and plays the optimal move. The best result a human can get is a **draw**.

---

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Installation & Run](#installation--run)
4. [How to Play](#how-to-play)
5. [How It Works (Deep Dive)](#how-it-works-deep-dive)
6. [Code Walkthrough](#code-walkthrough)
7. [Complexity & Performance](#complexity--performance)
8. [Project Structure](#project-structure)
9. [Possible Improvements](#possible-improvements)
10. [Team](#team)

---

## Features

- Play as **X** against the AI (**O**); you always move first
- Unbeatable AI (BFS game tree + Minimax)
- State deduplication with a `visited` set, so the same board is never expanded twice
- Memoization of Minimax results
- Shows how many states BFS explored on every AI move
- Input validation: non-numbers, out-of-range numbers, occupied cells
- Pure Python standard library, no external packages

## Requirements

- Python 3.7+

## Installation & Run

```bash
git clone https://github.com/emanomar2006git/AI-Tic-Tac-Toe.git
cd AI-Tic-Tac-Toe
python main.py
```

## How to Play

The board cells are numbered 1-9:

```
1 | 2 | 3
---------
4 | 5 | 6
---------
7 | 8 | 9
```

Type the number of the cell you want and press Enter. Taken cells show `X` or `O`; empty cells show their number.

Real example of a first move (you take the center):

```
Welcome to AI Tic-Tac-Toe!
You are X and AI is O.

1 | 2 | 3
---------
4 | 5 | 6
---------
7 | 8 | 9

Choose a cell (1-9): 5
AI chooses position: 1
BFS explored nodes: 1837
```

Possible endings: `You Win!` (never happens against a perfect AI), `AI Wins!`, or `Draw!`.

---

## How It Works (Deep Dive)

### 1. Representing the game

- The board is a **list of 9 cells**, index `0..8`, read row by row. Each cell is `"X"`, `"O"` or `" "` (empty).
- A **state** is a tuple `(board_tuple, next_player)`. The board is converted to a tuple so it is hashable and can be stored in a `set` or used as a dictionary key.
- The player who is about to move is part of the state because the same board can mean different things depending on whose turn it is.

### 2. Terminal states and scoring (`evaluate`)

A state is terminal when someone has won or the board is full. Scores are always from the AI's point of view:

| Outcome | Score |
|---------|-------|
| AI (O) wins | `+1` |
| Human (X) wins | `-1` |
| Draw | `0` |
| Game not over | `None` |

The winner is detected by checking the 8 winning lines: 3 rows, 3 columns, 2 diagonals.

### 3. Building the game tree with BFS (`bfs_build_game_tree`)

Starting from the current board, BFS generates every possible future of the game:

1. Put the start state in a `deque` (queue) and in the `visited` set.
2. Pop a state from the front of the queue.
3. If it is terminal, record it with no children and continue.
4. Otherwise, for each empty cell create a new board where the current player plays there, and flip the turn.
5. Save the edge `(move, new_state)` in the `children` dictionary.
6. If `new_state` was never seen, add it to `visited` and push it to the queue.
7. Repeat until the queue is empty.

The function returns `(start_state, children, len(visited))`:

- `children[state]` is the list of `(move, next_state)` pairs, so it is the game tree stored as an adjacency list.
- `len(visited)` is the "BFS explored nodes" number printed after every AI move.

BFS explores the tree **level by level** (all states after 1 move, then after 2 moves, and so on). `visited` makes the tree a **graph with merged states**: if X plays 1 then 2, or 2 then 1, the final board is the same state and is only expanded once. That is why the numbers are in the low thousands and not hundreds of thousands.

### 4. Minimax (`minimax_value`)

After BFS, Minimax walks the tree **recursively** and gives every state a value:

- **Terminal state** → its score from `evaluate` (+1 / -1 / 0).
- **AI's turn (maximizer)** → the AI wants the highest score, so it takes `max` of its children's values.
- **Human's turn (minimizer)** → the human is assumed to play perfectly against the AI, so it takes `min` of its children's values.

This guarantees the AI picks the move that gives the best result **even if the human plays perfectly**. A `memo` dictionary caches every computed state, so shared states are evaluated only once.

### 5. Choosing the move (`choose_ai_move`)

1. Build the tree from the current board with the AI to move.
2. For every possible AI move (children of the root), get its Minimax value.
3. Keep the move with the highest score (the first one wins ties).
4. Return `(best_move, explored_nodes)`.

### 6. Game loop (`play_game`)

```
print board → human move → check human win / draw
            → AI move    → check AI win / draw
            → repeat
```

`human_turn` loops until it gets a valid input (a digit, inside 1-9, on an empty cell).

### Worked example

You play the center (5). The AI has 8 possible replies. For each reply, BFS already built everything that can follow, and Minimax gives each reply a value. Corner replies reach a value of `0` (a draw with best play), while weak replies like an edge cell can lead to `-1` (a human win). The AI picks a move with the best value, which is why it answers with position 1 (a corner).

---

## Code Walkthrough

| Function | Description |
|----------|-------------|
| `print_board(board)` | Prints the 3x3 board; empty cells show their number 1-9 |
| `get_winner(board)` | Checks the 8 winning lines and returns `"X"`, `"O"` or `None` |
| `is_draw(board)` | True when the board is full and there is no winner |
| `available_moves(board)` | Returns the indexes of empty cells |
| `evaluate(board)` | Returns +1 / -1 / 0 for finished games, `None` if still running |
| `bfs_build_game_tree(start_board, next_player)` | BFS over all reachable states; returns the tree and the number of explored states |
| `minimax_value(state, children, memo)` | Recursive Minimax with memoization |
| `choose_ai_move(board)` | Builds the tree, scores each move, returns the best one |
| `human_turn(board)` | Reads and validates the player's move |
| `play_game()` | Main loop of the game |

Constants: `HUMAN = "X"`, `AI = "O"`, `EMPTY = " "`.

## Complexity & Performance

- Without any pruning, the naive Tic-Tac-Toe game tree has up to **9! = 362,880** move sequences.
- Thanks to the `visited` set, identical boards are merged, so the number of distinct states is much smaller.
- Measured on this code, after your first move the AI explores about **1,837 to 1,902 states** (depending on your move), and the AI replies instantly.
- Memory: the `children` dictionary stores each state once.
- The game gets faster as it progresses, because fewer cells remain empty.

## Project Structure

```
.
├── main.py      # board, BFS, Minimax, game loop
└── README.md
```

## Possible Improvements

- Let the player choose to play second (AI moves first)
- Add **Alpha-Beta pruning** to cut the search further
- Add difficulty levels (random mistakes at easy level)
- Build a GUI with Tkinter or Pygame
- Add unit tests for `get_winner`, `evaluate` and `choose_ai_move`

## Team

| Name | GitHub |
|------|--------|
| Rola Hatem  | 
| Eman Mahmoud | [@emanomar2006git](https://github.com/emanomar2006git) |
| Menna Mohamed  |

## License

This project is for educational purposes.
