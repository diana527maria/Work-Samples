# Coded at Artificial Intellgence workshop at Codette- 13.06.2018

import sys
from tic_tac_toe import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

W_BTN = 185
H_BTN = 185
X_BTN_GRP = 20
Y_MAIN = 20

class StartWindow(QMainWindow):

    def __init__(self):
        super(StartWindow, self).__init__()
        self.board = Board()
        self.initUI()

    def initUI(self):
        self.add_label_to_main_window("Player One: ", 20, 20, 100, 30)
        self.playerOneName = self.add_line_edit_to_main_window(140, 20, 100, 30)

        self.add_label_to_main_window("Player Two: ", 20, 60, 100, 30)
        self.playerTwoName = self.add_line_edit_to_main_window(140, 60, 100, 30)
        self.add_button_to_main_window("Play with Chuck Norris",
                                       self.bot2_game_button_func, 250, 60, 300, 30)

        self.add_label_to_main_window("... powered by ", 20, 130, 100, 50)
        self.algorithms = ["Minimax", "Alpha-beta"]
        self.logoScaleGroup = self.add_radio_boxes_to_main_window(self.algorithms, \
                                                                  self.on_algorithmBox_toggled, 140, 130, 110,
                                                                  100, 50)

        self.add_button_to_main_window("Exit", self.exit_game_button_func, 300, 200, 250, 50)
        self.add_button_to_main_window("Start Game!", self.start_game_button_func, 20, 200, 250, 50)

        self.setGeometry(500, 200, 600, 300)
        self.setWindowTitle('Tic Tac Toe')
        self.show()

    def add_label_to_main_window(self, text, x, y, w, h):
        lbl = QLabel(text, self)
        lbl.move(x, y)
        lbl.resize(w, h)
        return lbl

    def add_line_edit_to_main_window(self, x, y, w, h):
        le = QLineEdit(self)
        le.move(x, y)
        le.resize(w, h)
        return le

    def add_button_to_main_window(self, text, func, x, y, w, h):
        btn = QPushButton(text, self)
        btn.move(x, y)
        btn.resize(w, h)
        btn.clicked.connect(func)
        return btn

    @pyqtSlot(QAbstractButton)
    def on_algorithmBox_toggled(self, b):
        if b.isChecked() == True:
            self.board.game.setAlgorithm(str(b.text()))

    def add_radio_boxes_to_main_window(self, txt_list, func, x0, y0, x_inc, w, h):
        rbGroup = QButtonGroup(self)
        x = x0; y = y0;
        for ext in txt_list:
            elem = QRadioButton(ext, self)
            elem.move(x, y)
            elem.resize(w, h)
            x += x_inc
            rbGroup.addButton(elem)

        rbGroup.buttonClicked['QAbstractButton *'].connect(func)
        rbGroup.setExclusive(True)

        return rbGroup

    def exit_game_button_func(self):
        self.close()

    def start_game_button_func(self):
        self.board.game.player1 = str(self.playerOneName.text())
        self.board.game.player2 = str(self.playerTwoName.text())
        self.board.statusBar().showMessage(
            self.board.game.player1 + ": " + str(self.board.game.score1) + "; " + \
            self.board.game.player2 + ": " + str(self.board.game.score2))
        self.board.show()

    def bot2_game_button_func(self):
        self.playerTwoName.setText("Chuck Norris")
        self.board.game.player2_ai = True

class Board(QMainWindow):

    def __init__(self):
        super(Board, self).__init__()
        self.game = GameEngine()
        self.initUI()

    def initUI(self):
        global Y_MAIN, X_BTN_GRP
        self.board_group = self.add_buttons_group_to_main_window(self.on_FillXOBtn_clicked, X_BTN_GRP, Y_MAIN, W_BTN, H_BTN)
        self.statusBar()
        self.setGeometry(500, 200, 600, 600)
        self.setWindowTitle('Tic Tac Toe')

    def add_buttons_group_to_main_window(self, func, x0, y0, w, h):
        rbGroup = QButtonGroup(self)
        y = y0
        for row in range(0,3):
            x = x0
            for col in range(0,3):
                elem = QPushButton('', self)
                elem.setAccessibleName(str(row * 3 + col))
                elem.move(x, y)
                elem.resize(w, h)
                rbGroup.addButton(elem)
                x += w
            y += h
        rbGroup.buttonClicked['QAbstractButton *'].connect(func)

        return rbGroup

    def on_FillXOBtn_clicked(self, button):
        if(button.text() == ''):
            button.setText(self.game.symbol)
            self.game.move(int(button.accessibleName()))
            if (self.game.moves >= 9 and self.game.winner == None) or self.game.winner:
                self.make_game_over_dialog_box()
            else:
                if self.game.player2_ai:
                    symbol = self.game.symbol
                    pos = self.game.ai_move()
                    print(pos)
                    for b in self.board_group.buttons():
                        if b.accessibleName() == str(pos):
                            b.setText(symbol)

                    if (self.game.moves >= 9 and self.game.winner == None) or self.game.winner:
                        self.make_game_over_dialog_box()

    def make_game_over_dialog_box(self):
        print("Dialog Box")
        dialog = QMessageBox.question(self, "Game Over!", "Do you want to play again?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if dialog == QMessageBox.Yes:
            self.game.init_board()
            self.game.init_players()
            self.reinit_GUI()
        else:
            self.close()

    def reinit_GUI(self):
        buttonsList = self.board_group.buttons()
        for button in buttonsList:
            button.setText('')
        self.statusBar().showMessage(
            self.game.player1 + ": " + str(self.game.score1) + "; " + self.game.player2 + ": " + str(self.game.score2))

def main():
    app = QApplication(sys.argv)
    ex = StartWindow()
    app.exec_()

if __name__ == '__main__':
    main()
