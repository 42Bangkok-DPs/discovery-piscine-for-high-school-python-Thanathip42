#!/usr/bin/env python3

class ChessBoard:
    def __init__(self):
        self.board = self.create_board()
        self.turn = "Butter Bear"  # เริ่มต้นที่ฝ่าย Butter Bear
        self.move_history = []  # ประวัติการเคลื่อนที่
        self.king_positions = {'Butter Bear': (0, 4), 'Moo Deng': (7, 4)}  # ตำแหน่ง King ของทั้งสองฝ่าย
        self.rook_moved = {'Butter Bear': [False, False], 'Moo Deng': [False, False]}  # เช็คว่าหมาก Rook เคลื่อนที่แล้วหรือไม่

    def create_board(self):
        return [
            ["MR", "MN", "MB", "MQ", "MK", "MB", "MN", "MR"],  # Moo Deng pieces
            ["MP", "MP", "MP", "MP", "MP", "MP", "MP", "MP"],  # Moo Deng Pawns
            [". ", ". ", ". ", ". ", ". ", ". ", ". ", ". "],   # Empty row
            [". ", ". ", ". ", ". ", ". ", ". ", ". ", ". "],   # Empty row
            [". ", ". ", ". ", ". ", ". ", ". ", ". ", ". "],   # Empty row
            [". ", ". ", ". ", ". ", ". ", ". ", ". ", ". "],   # Empty row
            ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],  # Butter Bear Pawns
            ["BR", "BN", "BB", "BQ", "BK", "BB", "BN", "BR"]   # Butter Bear pieces
        ]

    def print_board(self, selected=None):
        print("   a    b    c    d    e    f    g    h")  # แสดงหมายเลขคอลัมน์
        for row in range(8):
            print(8 - row, end=" ")  # หมายเลขแถว
            for col in range(8):
                piece = self.board[row][col]
                if selected and (row, col) in selected:
                    print(f"[{piece}]", end=" ")  # แสดงหมากที่สามารถเคลื่อนที่ได้
                else:
                    print(f" {piece} ", end=" ")
            print()  # เปลี่ยนบรรทัด
        print()
        print(f"It's {self.turn}'s turn.")

    def show_possible_moves(self, position):
        possible_moves = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(position, (row, col)):
                    possible_moves.append((row, col))
        return possible_moves

    def print_move_history(self):
        print("Move History:")
        for move in self.move_history:
            print(move)
        print()

    def is_valid_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        piece = self.board[start_row][start_col]
        target_piece = self.board[end_row][end_col]

        if piece == ". ":
            return False  # ไม่มีหมากในตำแหน่งเริ่มต้น

        if (self.turn == "Moo Deng" and piece[0] == 'B') or (self.turn == "Butter Bear" and piece[0] == 'M'):
            return False  # ตรวจสอบว่าเป็นหมากของฝ่ายที่เล่นอยู่

        # ตรวจสอบการเคลื่อนที่ของหมากแต่ละประเภท
        if piece[1] == "P":  # Pawn
            direction = -1 if piece[0] == 'B' else 1
            start_rank = 6 if piece[0] == 'B' else 1
            if start_col == end_col:  # เคลื่อนที่ตรง
                if (end_row - start_row) == direction and target_piece == ". ":
                    return True
                if (end_row - start_row) == 2 * direction and start_row == start_rank and self.board[end_row][end_col] == ". " and self.board[start_row + direction][start_col] == ". ":
                    return True
            elif abs(start_col - end_col) == 1 and (end_row - start_row) == direction and target_piece != ". ":
                return True  # สามารถโจมตี

        elif piece[1] == "R":  # Rook
            if start_row == end_row or start_col == end_col:
                if self.path_clear(start, end):
                    return True

        elif piece[1] == "N":  # Knight
            if (abs(start_row - end_row), abs(start_col - end_col)) in [(2, 1), (1, 2)]:
                return True

        elif piece[1] == "B":  # Bishop
            if abs(start_row - end_row) == abs(start_col - end_col):
                if self.path_clear(start, end):
                    return True

        elif piece[1] == "Q":  # Queen
            if (start_row == end_row or start_col == end_col or
                    abs(start_row - end_row) == abs(start_col - end_col)):
                if self.path_clear(start, end):
                    return True

        elif piece[1] == "K":  # King
            if max(abs(start_row - end_row), abs(start_col - end_col)) == 1:
                return True  # การเคลื่อนที่ปกติ

            # ตรวจสอบการ castling
            if start_row == end_row and (start_col == 4 and (end_col == 2 or end_col == 6)):
                if end_col == 2:  # Queen's side castling
                    if not self.rook_moved[self.turn][0] and self.path_clear((start_row, 3), (start_row, 0)) and self.is_king_safe_after_move(start, (start_row, 2)):
                        return True
                elif end_col == 6:  # King's side castling
                    if not self.rook_moved[self.turn][1] and self.path_clear((start_row, 5), (start_row, 7)) and self.is_king_safe_after_move(start, (start_row, 6)):
                        return True

        return False

    def is_king_safe_after_move(self, start, end):
        original_king_pos = self.king_positions[self.turn]
        self.king_positions[self.turn] = end
        in_check = self.is_king_in_check(self.turn)
        self.king_positions[self.turn] = original_king_pos  # คืนค่าตำแหน่งเดิม
        return not in_check

    def move_piece(self, start, end):
        if self.is_valid_move(start, end):
            start_row, start_col = start
            piece = self.board[start_row][start_col]
            target_piece = self.board[end[0]][end[1]]

            # ตรวจสอบการโจมตี
            if target_piece != ". ":
                print(f"{piece} attacks {target_piece}!")  # แจ้งการโจมตี

            # เคลื่อนที่ของ King และตรวจสอบ castling
            if piece[1] == 'K':
                if start_col == 4:  # King is moving
                    if end[1] == 2:  # Queen's side castling
                        self.board[start_row][0] = ". "  # Rook moves
                        self.board[start_row][3] = "R" if self.turn == "Butter Bear" else "r"
                        self.rook_moved[self.turn][0] = True  # Rook moved
                    elif end[1] == 6:  # King's side castling
                        self.board[start_row][7] = ". "  # Rook moves
                        self.board[start_row][5] = "R" if self.turn == "Butter Bear" else "r"
                        self.rook_moved[self.turn][1] = True  # Rook moved

            # เปลี่ยนตำแหน่งหมาก
            self.board[start_row][start_col] = ". "
            self.board[end[0]][end[1]] = piece

            # ตรวจสอบโปรโมชั่นของ Pawn
            if piece[1] == 'P' and ((piece == 'BP' and end[0] == 0) or (piece == 'MP' and end[0] == 7)):
                self.promote_pawn(end)

            if self.is_king_in_check("Moo Deng" if self.turn == "Butter Bear" else "Butter Bear"):
                print(f"{self.turn} is in check!")

            # บันทึกการเคลื่อนที่
            move_notation = f"{piece} from {start} to {end}"
            self.move_history.append(move_notation)

            if self.is_checkmate("Moo Deng" if self.turn == "Butter Bear" else "Butter Bear"):
                winner = "Butter Bear" if self.turn == "Moo Deng" else "Moo Deng"
                print(f"{winner} wins! Checkmate!")
                return False

            self.king_positions[self.turn] = end  # อัปเดตตำแหน่ง King
            self.turn = "Moo Deng" if self.turn == "Butter Bear" else "Butter Bear"  # สลับฝ่าย

            return True
        return False

    def promote_pawn(self, position):
        # จัดการโปรโมชั่นของ Pawn
        row, col = position
        piece = self.board[row][col]
        print("Pawn promotion! Choose piece type (Q/R/B/N): ")
        
        # รับค่าจากผู้เล่น
        while True:
            new_piece = input("Choose (Q/R/B/N): ").upper()
            if new_piece in ["Q", "R", "B", "N"]:
                self.board[row][col] = new_piece + ('B' if piece[0] == 'B' else 'M')
                break
            else:
                print("Invalid choice, please try again.")

    def is_checkmate(self, color):
        # ตรวจสอบ checkmate
        if not self.is_king_in_check(color):
            return False

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if (color == "Moo Deng" and piece[0] == "B") or (color == "Butter Bear" and piece[0] == "M"):
                    if self.show_possible_moves((row, col)):
                        return False  # มีการเคลื่อนที่ที่เป็นไปได้

        return True

    def path_clear(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        step_row = (end_row - start_row) // max(1, abs(end_row - start_row)) if start_row != end_row else 0
        step_col = (end_col - start_col) // max(1, abs(end_col - start_col)) if start_col != end_col else 0

        row, col = start_row + step_row, start_col + step_col
        while (row, col) != (end_row, end_col):
            if self.board[row][col] != ". ":
                return False
            row += step_row
            col += step_col

        return True

    def is_king_in_check(self, color):
        king_pos = self.king_positions[color]
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != ". " and (piece[0] == 'B' if color == "Moo Deng" else piece[0] == 'M'):  # ตรวจสอบเฉพาะหมากฝ่ายตรงข้าม
                    if self.is_valid_move((row, col), king_pos):
                        return True  # คิงถูกโจมตี

        return False

def main():
    chess_board = ChessBoard()
    chess_board.print_board()

    while True:
        move = input("Enter your move (e.g., 'e2 e4'), 'history' to see move history or 'quit' to exit: ")
        if move.lower() == "quit":
            break
        elif move.lower() == "history":
            chess_board.print_move_history()
            continue

        try:
            start, end = move.split()
            start_row = 8 - int(start[1])
            start_col = ord(start[0]) - ord('a')
            end_row = 8 - int(end[1])
            end_col = ord(end[0]) - ord('a')

            # แสดงตำแหน่งที่สามารถเคลื่อนที่ได้ก่อนที่จะทำการเคลื่อนที่
            possible_moves = chess_board.show_possible_moves((start_row, start_col))
            chess_board.print_board(possible_moves)

            if chess_board.move_piece((start_row, start_col), (end_row, end_col)):
                chess_board.print_board()
            else:
                print("Invalid move. Please try again.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter in the format 'e2 e4'.")

if __name__ == "__main__":
    main()