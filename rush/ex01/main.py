#!/usr/bin/env python3

import sys

def checkmate(board):
    try:
        # Convert the board string into a 2D board list
        board = [list(row) for row in board.splitlines()]
        n = len(board)  # Get the size of the board

        # Find the king's position (assuming there is only one king 'K')
        king_pos = None
        for i in range(n):
            for j in range(n):
                if board[i][j] == 'K':
                    king_pos = (i, j)
                    break
        if not king_pos:
            print("Error")  # If no king found
            return

        king_x, king_y = king_pos

        # Check for threats from enemy pieces
        if is_under_attack(board, king_x, king_y, 'R', rook_moves) or \
           is_under_attack(board, king_x, king_y, 'B', bishop_moves) or \
           is_under_attack(board, king_x, king_y, 'Q', queen_moves) or \
           is_under_attack(board, king_x, king_y, 'P', pawn_moves):
            print("Success")
        else:
            print("Fail")

    except Exception:
        print("Error")  # Handle any exceptions


def is_under_attack(board, king_x, king_y, piece_type, move_func):
    n = len(board)
    for i in range(n):
        for j in range(n):
            if board[i][j] == piece_type:
                if move_func(board, i, j, king_x, king_y):
                    return True
    return False

def rook_moves(board, x, y, king_x, king_y):
    """Check if a rook at (x, y) can attack the king at (king_x, king_y)"""
    if x == king_x:
        step = 1 if king_y > y else -1
        for j in range(y + step, king_y, step):
            if board[x][j] != '.':
                return False
        return True
    elif y == king_y:
        step = 1 if king_x > x else -1
        for i in range(x + step, king_x, step):
            if board[i][y] != '.':
                return False
        return True
    return False

def bishop_moves(board, x, y, king_x, king_y):
    """Check if a bishop at (x, y) can attack the king at (king_x, king_y)"""
    if abs(king_x - x) == abs(king_y - y):
        step_x = 1 if king_x > x else -1
        step_y = 1 if king_y > y else -1
        i, j = x + step_x, y + step_y
        while i != king_x and j != king_y:
            if board[i][j] != '.':
                return False
            i += step_x
            j += step_y
        return True
    return False

def queen_moves(board, x, y, king_x, king_y):
    """A queen moves like both a rook and a bishop"""
    return rook_moves(board, x, y, king_x, king_y) or bishop_moves(board, x, y, king_x, king_y)

def pawn_moves(board, x, y, king_x, king_y):
    """Check if a pawn at (x, y) can attack the king"""
    # Assuming pawns are white (moving upward)
    return (king_x == x - 1 and abs(king_y - y) == 1)

def read_board(file_path):
    """Read chessboard from a file."""
    with open(file_path, 'r') as f:
        return f.read().strip()

def main():
    for file_path in sys.argv[1:]:
        try:
            board = read_board(file_path)
            checkmate(board)
        except Exception:
            print("Error")  # Print error if file reading fails

if __name__ == "__main__":
    main()