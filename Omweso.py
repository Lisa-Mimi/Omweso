import sys
import copy
INF = sys.maxsize

class Moves:
    def __init__(self):
        self.row_new = None
        self.col_new = None
        self.row_prev = None
        self.col_prev = None
        self.winner = None

    def terminal_state(self, board_1, board_2):
        seeds_num = 0  # number of seeds in board 1
        seeds_num_1 = 0  # number of seeds in board_2
        for i in range(1):  # number of columns
            for j in range(7):  # number of rows
                if board_1[i][j] < 2:
                    seeds_num = seeds_num + 1
                elif board_2[i][j] < 2:
                    seeds_num_1 = seeds_num_1 + 1
        return seeds_num == 16 or seeds_num_1 == 16

    def winner(self, board_1, board_2):
        # change variable names of num and num_1
        seeds_num = 0  # number of seeds in board 1
        seeds_num_1 = 0  # number of seeds in board_2
        for i in range(1): # number of columns
            for j in range(7): # number of rows
                if board_1[i][j] < 2:
                    seeds_num = seeds_num + 1
                elif board_2[i][j] < 2:
                    seeds_num_1 = seeds_num_1 + 1
        if seeds_num == 16 and seeds_num_1 < 16:
            self.winner = board_2
        elif seeds_num_1 == 16 and seeds_num < 16:
                self.winner = board_1
        else:
            self.winner = self.winner_non_terminal_state(board_1,board_2)
        return self.winner

    def winner_non_terminal_state(self, board_1, board_2):
        seeds_num = 0
        seeds_num_1 = 0
        for i in range(1):
            for j in range(7):
                if board_1[i][j] > 0:
                    seeds_num = seeds_num + 1
                if board_2[i][j] > 0:
                    seeds_num_1 = seeds_num_1 + 1
        if seeds_num > seeds_num_1:
            self.winner = board_2
        elif seeds_num_1 > seeds_num:
            self.winner = board_1
        return self.winner

    def upper_row_sowing(self, row, col, player, num=0):
        # player to be changed to board
        if num == 0: # number of seeds
            num = player[row][col]
            player[row][col] = 0
        num_1 = num # keeps track of number of seeds distributed
        for j in range(num):
            col = col - 1
            if col >= 0:
                player[row][col] = player[row][col] + 1
                num_1 = num_1 - 1
            else:
                row = 1
                num = num_1
                self.lower_row_sowing(row, col, player, num)
                return
        self.row_new = row
        self.col_new = col

    def lower_row_sowing(self, row, col, player, num=0):
        if num == 0:
            num = player[row][col]
            player[row][col] = 0
        num_1 = num
        for j in range(num):
            col = col + 1
            if col <= 7:
                player[row][col] = player[row][col] + 1
                num_1 = num_1 - 1
            else:
                row = 0
                num = num_1
                self.upper_row_sowing(row, col, player, num)
                return
        self.row_new = row
        self.col_new = col

    def reverse_upper_row_sowing(self, row, col, player, num=0):
        if num == 0:
            num = player[row][col]
            player[row][col] = 0
        num_1 = num
        for j in range(num):
            col = col + 1
            if col <= 7:
                player[row][col] = player[row][col] + 1
                num_1 = num_1 - 1
            else:
                row = 1
                num = num_1
                self.reverse_lower_row_sowing(row, col, player, num)
                return
        self.row_new = row
        self.col_new = col

    def reverse_lower_row_sowing(self, row, col, player, num=0):
        if num == 0:
            num = player[row][col]
            player[row][col] = 0
        num_1 = num
        for j in range(num):
            col = col - 1
            if col >= 0:
                player[row][col] = player[row][col] + 1
                num_1 = num_1 - 1
            else:
                row = 0
                num = num_1
                self.reverse_upper_row_sowing(row, col, player, num)
                return
        self.row_new = row
        self.col_new = col

    def is_relay_sowing(self, player):
        return player[self.row_new][self.col_new] >= 2

    def legal_moves(self, board):
        moves = []
        for i in range(1):  # number of columns
            for j in range(7):
                if board[i][j] >= 2:
                    moves.append((i,j))
        return moves

    def sowing(self, row, col, player):
        self.row_prev = row
        self.col_prev = col
        if (0 <= row < len(player)) and (0 <= col < len(player[0])):
            if player[row][col] >= 2:
                if row == 0:
                    self.upper_row_sowing(row, col, player)
                if row == 1:
                    self.lower_row_sowing(row, col, player)

        else:
            print("Wrong Input!Try Again!")

    def reverse_sowing(self, row, col, player):
        self.row_prev = row
        self.col_prev = col
        if (0 <= row < len(player)) and (0 <= col < len(player[0])):
            if player[row][col] >= 2:
                if row == 0:
                    self.reverse_upper_row_sowing(row, col, player)
                if row == 1:
                    self.reverse_lower_row_sowing(row, col, player)

        else:
            print("Wrong Input!Try Again!")

    def relay_sowing(self, player):
        self.sowing(self.row_new, self.col_new, player)

    def is_capture(self, player_opp, player):
        row = self.row_new
        col = self.col_new
        if row == 0 and 0 < col < 7:
            return player[row][col] >= 2 and player_opp[row][col] >= 1 and player_opp[row + 1][col] >= 1
        else:
            return False

    def capture(self, player_opp, player):
        row_prev = self.row_prev
        col_prev = self.col_prev
        row_current = self.row_new
        col_current = self.col_new
        if row_current == 0:
            num = player[row_prev][col_prev]
            player[row_prev][col_prev] = player_opp[row_current][col_current] + player_opp[row_current + 1][col_current]
            player_opp[row_current][col_current] = 0
            player_opp[row_current + 1][col_current] = 0
            self.sowing(row_prev, col_prev, player)
            player[row_prev][col_prev] = num

    def is_reverse_capture(self, player_opp, player):
        row = self.row_new
        col = self.col_new
        if (row == 0 and col == 0) or (row == 0 and col == 1) or (row == 1 and col == 0) or (row == 1 and col == 1):
            self.reverse_sowing(row, col, player)
            return self.is_capture(player_opp, player)

    def reverse_capture(self, player_opp, player):
        row = self.row_new
        col = self.col_new
        self.reverse_sowing(row, col, player)
        self.capture(player_opp, player)

    def is_terminal_state(self, player_1, player_2):
        num = 0
        num_1 = 0
        for i in range(1):
            for j in range(7):
                if player_1[i][j] < 2:
                    num = num + 1
                elif player_2[i][j] < 2:
                    num_1 = num_1 + 1
        return num == 16 and num_1 < 16 or num_1 == 16 and num < 16

    def print_boards(self, board_1, board_2):
        board = [board_1[1][7],board_1[1][6],board_1[1][5],board_1[1][4],board_1[1][3],board_1[1][2],board_1[1][1],
              board_1[1][0]]
        board1 = [board_1[0][7], board_1[0][6], board_1[0][5], board_1[0][4], board_1[0][3], board_1[0][2], board_1[0][1],
              board_1[0][0]]
        print(board)
        print(board1)
        print()
        print(board_2[0])
        print(board_2[1])
        print()


class Omweso(Moves):
    def __init__(self):
        super().__init__()
        self.board_1 = [[4, 4, 4, 4, 4, 4, 4, 4], [0, 0, 0, 0, 0, 0, 0, 0]]
        self.board_2 = [[4, 4, 4, 4, 4, 4, 4, 4], [0, 0, 0, 0, 0, 0, 0, 0]]
        self.curr_player_name = None
        self.n_levels = 0
        self.states = dict()

    def playing(self, row, col, curr_board, opp_board, print_status=True):
        if True:
            self.sowing(row, col, curr_board)
            if print_status:
                print("Board after sowing")
                self.print_boards(self.board_1, self.board_2)

        if self.is_capture(opp_board, curr_board):
            self.capture(opp_board, curr_board)
            if print_status:
                print("Board after capture:")
                self.print_boards(self.board_1, self.board_2)

        if self.is_reverse_capture(opp_board, curr_board):
            self.reverse_capture(opp_board, curr_board)
            if print_status:
                print("Board after reverse capture:")
                self.print_boards(self.board_1, self.board_2)

        if self.is_relay_sowing(curr_board):
            self.relay_sowing(curr_board)
            if print_status:
                print("Board after relay sowing")
                self.print_boards(self.board_1, self.board_2)

    def ManualPlay(self, player1_name, player2_name):
        curr_board = self.board_1
        opp_board = self.board_2
        self.curr_player_name = player1_name
        while not self.is_terminal_state(curr_board, opp_board):
            print(self.curr_player_name + " is playing")
            row, col = input("Enter row<Enter> and column:").split(" ")
            row = int(row)
            col = int(col)
            self.playing(row, col, curr_board, opp_board)

            # change turns
            if curr_board is self.board_1:
                curr_board = self.board_2
                opp_board = self.board_1
                self.curr_player_name = player2_name

            elif curr_board is self.board_2:
                curr_board = self.board_1
                opp_board = self.board_2
                self.curr_player_name = player1_name

        if self.terminal_state(self.board_1, self.board_2):
            winner = self.winner(self.board_1, self.board_2)
            print("________Board for terminal state_______")
            self.print_boards(self.board_1, self.board_2)
            if winner is self.board_1:
                print(player1_name + " has won!")
            if winner is self.board_2:
                print(player2_name + " has won!")
            return

    def PlayerVsComputer(self, player_name, player_turn):
        player1_name = None
        player2_name = None
        curr_board = self.board_1
        opp_board = self.board_2
        if player_turn == 1:
            player1_name = player_name
            player2_name = "Computer"
        elif player_turn == 2:
            player1_name = "Computer"
            player2_name = player_name

        self.curr_player_name = player1_name

        while not self.is_terminal_state(curr_board, opp_board):
            print(self.curr_player_name + " is playing")
            if self.curr_player_name == "Computer":
                row, col = self.minimax([self.board_1[0],self.board_1[1], self.board_2[0], self.board_2[1]])
                self.playing(row, col, curr_board, opp_board)

            else:
                row, col = input("Enter row<Enter> and column:").split(" ")
                row = int(row)
                col = int(col)
                self.playing(row, col, curr_board, opp_board)

            # change turns
            if curr_board is self.board_1:
                curr_board = self.board_2
                opp_board = self.board_1
                self.curr_player_name = player2_name

            elif curr_board is self.board_2:
                curr_board = self.board_1
                opp_board = self.board_2
                self.curr_player_name = player1_name

        if self.terminal_state(self.board_1, self.board_2):
            winner = self.winner(self.board_1, self.board_2)
            print("________Board for terminal state_______")
            self.print_boards(self.board_1, self.board_2)
            if winner is self.board_1:
                print(player1_name + " has won!")
            if winner is self.board_2:
                print(player2_name + " has won!")
            return

    def utility(self, board_1, board_2):
        winner = self.winner(board_1, board_2)
        if winner is board_1:
            return 1
        elif winner is board_2:
            return -1

    def utility_1(self,board_1, board_2):
        winner = self.winner_non_terminal_state(board_1,board_2)
        if winner is board_1:
            return 1
        elif winner is board_2:
            return -1
        else:
            return 0

    def results(self, action, board_1, board_2, player):
        self.playing(action[0], action[1], board_1, board_2, False)
        if player == 1:
            self.playing(action[0], action[1], board_1, board_2, False)
        elif player == 2:
            self.playing(action[0], action[1], board_2, board_1, False)

        res_state = [board_1[0], board_1[1], board_2[0], board_2[1]]
        return res_state

    def board_to_string(self, boards):
        boards_1 = copy.deepcopy(boards)
        for board in boards_1:
            for i in range(len(board)):
                board[i] = str(board[i])
        return "".join(boards_1[0]) + "".join(boards_1[1]) + "".join(boards_1[2]) + "".join(boards_1[3])

    def max_value(self, state, level):
        self.n_levels = max(self.n_levels, level)
        board_1 = [state[0].copy(), state[1].copy()]
        board_2 = [state[2].copy(), state[3].copy()]
        if self.is_terminal_state(board_1, board_2):
            util = self.utility(board_1, board_2)
            return util
        elif self.n_levels == 100:
            util = self.utility_1(board_1, board_2)
            return util
        value = -INF
        actions = self.legal_moves(board_1)
        for action in actions:
            next_state = self.results(action, board_1, board_2, 1)
            statestr = self.board_to_string(next_state)
            if statestr in self.states:
                next_state_value = self.states[statestr]
            else:
                next_state_value = self.min_value(next_state, level + 1)
                self.states[self.board_to_string(next_state)] = next_state_value
            value = max(value, next_state_value)
        return value

    def min_value(self, state, level):
        self.n_levels = max(self.n_levels, level)
        board_1 = [state[0].copy(), state[1].copy()]
        board_2 = [state[2].copy(), state[3].copy()]
        if self.is_terminal_state(board_1, board_2):
            util = self.utility(board_1, board_2)
            return util
        elif self.n_levels == 100:
            util = self.utility_1(board_1, board_2)
            return util
        value = INF
        actions = self.legal_moves(board_2)
        for action in actions:
            next_state = self.results(action, board_1, board_2, 2)
            statestr = self.board_to_string(next_state)
            if statestr in self.states:
                next_state_value = self.states[statestr]
            else:
                next_state_value = self.max_value(next_state, level + 1)
                self.states[self.board_to_string(next_state)] = next_state_value
            value = min(value, next_state_value)
        return value

    def minimax(self,state):
        value = -INF
        best_action = None
        board_1 = [state[0].copy(), state[1].copy()]
        board_2 = [state[2].copy(), state[3].copy()]
        actions = self.legal_moves(board_1)
        for i in range(len(actions)):
            result_state = self.results(actions[i], board_1, board_2, 1)
            statestr = self.board_to_string(result_state)
            if statestr in self.states:
                next_state_value = self.states[statestr]
            else:
                next_state_value = self.min_value(result_state, 1)
                self.states[statestr] = next_state_value
            if next_state_value > value:
                value = next_state_value
                best_action = actions[i]
            return best_action


obj = Omweso()

