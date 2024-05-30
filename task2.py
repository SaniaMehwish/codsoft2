import math
import random

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        return False

def minimax(position, maximizing_player, alpha, beta):
    if position.current_winner:
        return {'position': None,
                'score': 1 if position.current_winner == 'O' else -1 if position.current_winner == 'X' else 0}
    elif not position.empty_squares():
        return {'position': None, 'score': 0}

    if maximizing_player:
        max_eval = {'position': None, 'score': -math.inf}
        for possible_move in position.available_moves():
            position.make_move(possible_move, 'O')
            evaluation = minimax(position, False, alpha, beta)
            position.board[possible_move] = ' '
            evaluation['position'] = possible_move
            if evaluation['score'] > max_eval['score']:
                max_eval = evaluation
            alpha = max(alpha, evaluation['score'])
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = {'position': None, 'score': math.inf}
        for possible_move in position.available_moves():
            position.make_move(possible_move, 'X')
            evaluation = minimax(position, True, alpha, beta)
            position.board[possible_move] = ' '
            evaluation['position'] = possible_move
            if evaluation['score'] < min_eval['score']:
                min_eval = evaluation
            beta = min(beta, evaluation['score'])
            if beta <= alpha:
                break
        return min_eval

def play_game():
    game = TicTacToe()
    print("To play Tic Tac Toe, please use the following board positions:")
    TicTacToe.print_board_nums()
    print("")

    while game.empty_squares():
        if game.current_winner:
            print(f"The winner is {game.current_winner}")
            break
        print("It's your turn!")
        human_move = None
        while human_move is None:
            try:
                human_move = int(input("Enter your move (0-8): "))
                if human_move not in game.available_moves():
                    print("That is not a valid move. Try again.")
                    human_move = None
            except ValueError:
                print("Please enter a number.")

        game.make_move(human_move, 'X')
        game.print_board()
        print("")

        if game.current_winner:
            break

        print("AI is thinking...")
        ai_move = minimax(game, True, -math.inf, math.inf)['position']
        game.make_move(ai_move, 'O')
        game.print_board()
        print("")

    if not game.current_winner:
        print("It's a tie!")

play_game()
