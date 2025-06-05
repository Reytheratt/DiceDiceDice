from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMessageBox
)
from PyQt5.QtGui import QFont, QIcon
import sys
import Project

class GameWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowIcon(QIcon("Dice.png"))
        self.setWindowTitle("Dice! Dice! Dice!")
        self.setGeometry(100, 100, 600, 700)
        self.setFont(QFont("ByteBounce", 30))
        self.player = Project.Player("Player 1")
        self.bot = Project.Bot()

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.info_label = QLabel("Click 'Roll Dice' to start!")
        self.layout.addWidget(self.info_label)

        self.bot_claim_label = QLabel("")
        self.layout.addWidget(self.bot_claim_label)

        self.roll_button = QPushButton("Roll Dice")
        self.roll_button.clicked.connect(self.play_round)
        self.layout.addWidget(self.roll_button)

        self.more_button = QPushButton("More")
        self.more_button.clicked.connect(lambda: self.check_winner("more"))
        self.more_button.setEnabled(False)
        self.layout.addWidget(self.more_button)

        self.less_button = QPushButton("Less")
        self.less_button.clicked.connect(lambda: self.check_winner("less"))
        self.less_button.setEnabled(False)
        self.layout.addWidget(self.less_button)

        self.setLayout(self.layout)

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
        result = Project.winner(self.player_sum, self.bot_sum, prediction)

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

        self.player = Project.Player("Player 1")
        self.bot = Project.Bot()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec_())
