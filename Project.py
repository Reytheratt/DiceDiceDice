import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QFont
from GUI import Ui_MainWindow
import random


class Bot:
    def __init__(self):
        self.dice = []
        self._sum = 0

    def dice_roller(self):
        self.dice = [random.randint(1, 6) for _ in range(3)]
        print(f"Bot rolled {self.dice[random.randint(0, 2)]}. Other dice are hidden.")

    def get_sum(self):
        self._sum = sum(self.dice)
        return self._sum

    def bluffing(self):
        smallest = min(self.dice)

        def more():
            lie = self._sum + smallest
            print(f"He says he has {lie}")
            return lie

        def less():
            lie = self._sum - smallest
            print(f"He says he has {lie}")
            return lie

        def choices():
            if self._sum >= 18:
                return less()
            elif self._sum <= 3:
                return more()
            else:
                return random.choice([more, less])()

        return choices()


class Player:
    def __init__(self, name):
        self.name = name
        self.dice = []
        self._sum = 0

    def dice_roller(self):
        self.dice = [random.randint(1, 6) for i in range(3)]
        print(f"You've rolled {self.dice[0]}, other dice are hidden.")

    def get_sum(self):
        self._sum = sum(self.dice)
        return self._sum

    def player_input(self):
        while True:
            prediction = input("More or Less? \n").strip().lower()
            if prediction in ("more", "less"):
                return prediction
            print("Invalid! Please enter either 'More' or 'Less'!")


def winner(player_sum, bot_sum, prediction):
    if player_sum == bot_sum:
        return "Draw"
    elif prediction == "more":
        return "Player" if player_sum > bot_sum else "Bot"
    elif prediction == "less":
        return "Player" if player_sum < bot_sum else "Bot"
    else:
        raise ValueError("Invalid! Prediction Must be 'More' or 'Less'!")


def play():
    player = Player("Player 1")
    bot = Bot()

    player.dice_roller()
    bot.dice_roller()

    player_sum = player.get_sum()
    bot_sum = bot.get_sum()
    bot.bluffing()

    prediction = player.player_input()

    result = winner(player_sum, bot_sum, prediction)

    if result == "Player":
        print("You win!")
    elif result == "Bot":
        print("You lose. Try again!")
    elif result == "Draw":
        print("Hey, It's a Draw!")

    print(f"Your rolls were: {player.dice}. Your sum: {player._sum}")
    print(f"Bot's rolls were{bot.dice}, while it's real sum was {bot._sum}")


def play_again():
    while True:
        answer = input("Do you wish to play again?: \n").strip().lower()
        if answer == "yes":
            return True
        if answer == "no":
            return False


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setFont(QFont("ByteBounce", 30))
        self.player = Player("Player 1")
        self.bot = Bot()


        self.more_button.setEnabled(False)
        self.less_button.setEnabled(False)

        self.roll_button.clicked.connect(self.play_round)
        self.more_button.clicked.connect(lambda: self.check_winner("more"))
        self.less_button.clicked.connect(lambda: self.check_winner("less"))


    def play_round(self):
        self.player.dice_roller()
        self.bot.dice_roller()

        self.player_sum = self.player.get_sum()
        self.bot_sum = self.bot.get_sum()

        self.bluff = self.bot.bluffing()

        self.info_label.setText(f"You rolled: {self.player.dice[0]} (others hidden)")
        self.bot_claim_label.setText(f"Bot says their sum is {self.bluff}. More or Less?")

        self.roll_button.setEnabled(False)
        self.more_button.setEnabled(True)
        self.less_button.setEnabled(True)

    def check_winner(self, prediction):
        result = winner(self.player_sum, self.bot_sum, prediction)

        if result == "player":
            message = "You Win!"
        elif result == "bot":
            message = "You lost. Try again!"
        elif result == "draw":
            message = "It's a draw!"
        else:
            message = "Unexpected result."

        message += f"\n\nYour rolls: {self.player.dice} (sum = {self.player_sum})"
        message += f"\nBot's rolls: {self.bot.dice} (sum = {self.bot_sum})"

        QMessageBox.information(self, "Result", message)

        self.roll_button.setEnabled(True)
        self.more_button.setEnabled(False)
        self.less_button.setEnabled(False)
        self.info_label.setText("Click 'Roll Dice' to start!")
        self.bot_claim_label.setText("")

        self.player = Player("Player 1")
        self.bot = Bot()



app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
