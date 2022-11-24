from Omweso import *
choice = int(input("""Enter:
       1 - For Player Vs Player
       2 - For Computer Vs Player
       Choice:"""))

if choice == 1:
    player1_name = input("Enter name for player 1:")
    player2_name = input("Enter name for player 2:")
    obj.ManualPlay(player1_name, player2_name)

elif choice == 2:
    player_name = input("Enter name for player(human):")
    player_turn = int(input("""Enter
           1 - To play first and computer second
           2 - To play second and computer first
           Choice:"""))
    obj.PlayerVsComputer(player_name, player_turn)
