# Instantiates a Game Instance
class Game(object):
    def __init__(self, game_state, game_board):
        self.game_state = game_state
        self.game_board = game_board


# Display the Game Board
class Board(object):
    def __init__(self, boardSquares):
        self.boardSquares = boardSquares

    def printBoard(self):
        print(end="\n")
        print(self.boardSquares[0] + "  | " + self.boardSquares[1] + " |  " + self.boardSquares[2])
        print("-----------")
        print(self.boardSquares[3] + "  | " + self.boardSquares[4] + " |  " + self.boardSquares[5])
        print("-----------")
        print(self.boardSquares[6] + "  | " + self.boardSquares[7] + " |  " + self.boardSquares[8])
        print(end="\n")


# Instantiate the Players
class Player(object):
    def __init__(self, name, marker, turn):
        self.name = name
        self.marker = marker
        self.turn = turn


# Play the Game
def playGame(new_game, player):
    while new_game.game_state:

        for action in player:
            getAction(new_game.game_board, action)
            win_result = checkWinner(action.marker, new_game.game_board)
            draw_result = checkDraw(new_game.game_board)

            if win_result:
                return 'win'

            if draw_result:
                return 'Draw'


# Get the Player's Action
def getAction(game_board, active_player):
    while True:
        player_input = input(active_player.name + ", enter an integer (1 - 9): ")

        if player_input.isdigit():
            player_input = int(player_input)

            if 0 < player_input <= 9 and game_board[player_input - 1] == ' ':
                break
            else:
                print("Please enter a valid action.")
                continue
        else:
            print("Please enter a valid action.")
            continue

    playerMove(game_board, player_input, active_player.marker)


# Place the Player's Action
def playerMove(game_board, valid_input, marker):
    game_board[valid_input - 1] = marker
    Board(game_board).printBoard()


# Check if Game is Won
def checkWinner(player_marker, game_board):
    if (game_board[0] == game_board[1] and game_board[0] == game_board[2] and game_board[0] == player_marker or
                         game_board[3] == game_board[4] and game_board[3] == game_board[5] and game_board[3] == player_marker or
                         game_board[6] == game_board[7] and game_board[6] == game_board[8] and game_board[6] == player_marker or
                         game_board[0] == game_board[3] and game_board[0] == game_board[6] and game_board[0] == player_marker or
                         game_board[1] == game_board[4] and game_board[1] == game_board[7] and game_board[1] == player_marker or
                         game_board[2] == game_board[5] and game_board[2] == game_board[8] and game_board[2] == player_marker or
                         game_board[0] == game_board[4] and game_board[0] == game_board[8] and game_board[0] == player_marker or
                         game_board[6] == game_board[4] and game_board[6] == game_board[2] and game_board[6] == player_marker):
        return True
    else:
        return False


# Check if Game is a Draw
def checkDraw(game_board):
    if " " not in game_board:
        return True
    else:
        return False


def checkResult(outcome):
    if outcome == "win":
        print("Winner!")
    elif outcome == "Draw":
        print("Draw")


def playAgain():
    answer = input("Do you want to play again? (Y / N): ")
    answer = answer[0].lower()

    if answer == 'y':
        init()
    elif answer == 'n':
        print("Thanks for Playing!")
    else:
        print("Please give a valid response.")
        playAgain()


def init():
    # Instantiate Game Instance
    new_game = Game(True, [' '] * 9)

    # Display the Game Board
    Board(new_game.game_board).printBoard()

    # Instantiate the Players
    player_one = Player(input("Enter your player name: "), "X", 0)
    player_two = Player(input("Enter your player name: "), "O", 1)
    active_player = [player_one, player_two]

    outcome = playGame(new_game, active_player)

    checkResult(outcome)

    playAgain()


init()
