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
            self.winner = "Player 2"
        else:
            if seeds_num_1 == 16 and seeds_num < 16:
                self.winner = "Player 1"
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
        return player[row][col] >= 2 and player_opp[row][col] >= 1 and player_opp[row + 1][col] >= 1

    def capture(self, player_opp, player):
        row_prev = self.row_prev
        col_prev = self.col_prev
        row_current = self.row_new
        col_current = self.col_new
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
        print(board_1[1])
        print(board_1[0])
        print()
        print(board_2[0])
        print(board_2[1])
        print()


class Omweso(Moves):
    def __init__(self):
        super().__init__()
        self.board_1 = [[4, 4, 4, 4, 4, 4, 4, 4],
                    [0, 0, 0, 0, 0, 0, 0, 0]]
        self.board_2 = [[4, 4, 4, 4, 4, 4, 4, 4],
                    [0, 0, 0, 0, 0, 0, 0, 0]]
        print("________Boards:_______")
        self.print_boards(self.board_1, self.board_2)
        self.curr_player_name = None
        self.curr_board = None
        self.opp_board = None

    def playing(self, player_1_name, player_2_name):
        self.curr_board = self.board_1
        self.opp_board = self.board_2
        self.curr_player_name = player_1_name

        while True:
            print(self.curr_player_name + " is playing")
            row, col = input("Enter row<Enter> and column:").split(" ")
            row = int(row)
            col = int(col)

            self.sowing(row, col, self.curr_board)
            print("Board after sowing")
            self.print_boards(self.board_1, self.board_2)

            if self.is_capture(self.opp_board, self.curr_board):
                self.capture(self.opp_board, self.curr_board)
                print("Board after capture:")
                self.print_boards(self.board_1, self.board_2)

            elif self.is_reverse_capture(self.opp_board, self.curr_board):
                self.reverse_capture(self.opp_board, self.curr_board)
                print("Board after reverse capture:")
                self.print_boards(self.board_1, self.board_2)

            elif self.is_relay_sowing(self.curr_board):
                self.relay_sowing(self.curr_board)
                print("Board after relay sowing")
                self.print_boards(self.board_1, self.board_2)

            elif self.terminal_state(self.board_1, self.board_2):
                    winner = self.winner(self.board_1, self.board_2)
                    print("________Board for terminal state_______")
                    self.print_boards(self.board_1, self.board_2)
                    if winner == "Player 1":
                        print(player_1_name + " has won!")
                    if winner == "Player 2":
                        print(player_2_name + " has won!")
                    return

            else:
                if self.curr_board == self.board_1:
                    self.curr_board = self.board_2
                    self.opp_board = self.board_1
                    self.curr_player_name = player_2_name

                elif self.curr_board == self.board_2:
                    self.curr_board = self.board_1
                    self.opp_board = self.board_2
                    self.curr_player_name = player_1_name


obj = Omweso()
player_1_name = input("Enter the name of the player 1:")
player_2_name = input("Enter the name of the player 2:")
obj.playing(player_1_name, player_2_name)







