from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

def is_valid(board, row, col, num):
    """Check if placing num at board[row][col] is valid"""
    # Check row
    if num in board[row]:
        return False
    
    # Check column
    if num in [board[i][col] for i in range(9)]:
        return False
    
    # Check 3x3 box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False
    
    return True

def solve_sudoku(board):
    """Solve sudoku using backtracking"""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    board = data.get('board', [])
    
    if solve_sudoku(board):
        return jsonify({'success': True, 'board': board})
    return jsonify({'success': False, 'message': 'No solution exists'})

if __name__ == '__main__':
    app.run(debug=True)
