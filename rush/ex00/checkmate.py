#!/usr/bin/env python3

# K = King
# R = Rook
# B = Bishop
# Q = Queen
# P = Pawn

def checkmate(board):
    try:
        # แปลง string ของกระดานเป็น 2D board list
        board = [list(row) for row in board.splitlines()]
        n = len(board)  # ตรวจขนาดของกระดาน

        # หาตำแหน่งของ King
        king_pos = None
        for i in range(n):
            for j in range(n):
                if board[i][j] == 'K':
                    king_pos = (i, j)  # เก็บข้อมูลตำแหน่ง King
                    break
        if not king_pos:  # กรณีไม่มี King ในกระดาน
            print("Error: No king found on the board.")
            return

        king_x, king_y = king_pos  # แยกตำแหน่ง x และ y

        # ตรวจสอบ King จะโดน check จากฝ่ายตรงข้าม
        if is_under_attack(board, king_x, king_y, 'R', rook_moves) or \
           is_under_attack(board, king_x, king_y, 'B', bishop_moves) or \
           is_under_attack(board, king_x, king_y, 'Q', queen_moves) or \
           is_under_attack(board, king_x, king_y, 'P', pawn_moves):
            print("Success")  # กรณี King โดน check
        else:
            print("Fail")  # กรณี King ไม่โดน check

    except Exception as e:  # กรณีหาตำแหน่ง King แล้ว error
        print(f"Error: {str(e)}")

def is_under_attack(board, king_x, king_y, piece_type, move_func):
    # ตรวจสอบว่า piece_type สามารถ check King ได้ไหม
    n = len(board)
    for i in range(n):
        for j in range(n):
            if board[i][j] == piece_type:  # กรณีเจอ piece_type
                if move_func(board, i, j, king_x, king_y):  # ตรวจสอบการเคลื่อนที่
                    return True  # กรณีสามรถ check ได้
    return False  # กรณีไม่มีการ check

def rook_moves(board, x, y, king_x, king_y):
    # เช็คว่า Rook ที่ (x, y) in check ไหม
    if x == king_x:  # ถ้าอยู่ในแนวนอน
        step = 1 if king_y > y else -1  # กำหนดทิศทาง
        for j in range(y + step, king_y, step):  # ตรวจสอบช่องว่างระหว่าง
            if board[x][j] != '.':
                return False
        return True  # ถ้าทางโล่ง
    elif y == king_y:  # ถ้าอยู่ในแนวตั้ง
        step = 1 if king_x > x else -1  # กำหนดทิศทาง
        for i in range(x + step, king_x, step):  # ตรวจสอบช่องว่างระหว่าง
            if board[i][y] != '.':
                return False
        return True  # ถ้าทางโล่ง
    return False  # ถ้าไม่อยู่ในแนวที่สามารถ check ได้

def bishop_moves(board, x, y, king_x, king_y):
    # เช็คว่า Bishop ที่ (x, y) in check ไหม
    if abs(king_x - x) == abs(king_y - y):  # ถ้าอยู่ในแนวเฉียง
        step_x = 1 if king_x > x else -1  #  กำหนดทิศทางแนวนอน
        step_y = 1 if king_y > y else -1  #  กำหนดทิศทางแนวตั้ง
        i, j = x + step_x, y + step_y
        while i != king_x and j != king_y:  #  ตรวจสอบช่องว่างระหว่าง
            if board[i][j] != '.':
                return False
            i += step_x  # เคลื่อนที่ในแนวนอน
            j += step_y  # เคลื่อนที่ในแนวตั้ง
        return True  # ถ้าทางโล่ง
    return False  # ถ้าไม่อยู่ในแนวที่สามารถ check ได้

def queen_moves(board, x, y, king_x, king_y):
    # Queen เคลื่อนที่เหมือน Rook และ Bishop
    return rook_moves(board, x, y, king_x, king_y) or bishop_moves(board, x, y, king_x, king_y)

def pawn_moves(board, x, y, king_x, king_y):
    # เช็คว่า Pawn ที่ (x, y) in check ไหม
    return (king_x == x - 1 and abs(king_y - y) == 1)  # ให้ Pawn อยู่ฝ่ายขาว (เคลื่อนที่ไปด้านบน) 