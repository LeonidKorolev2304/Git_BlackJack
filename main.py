import copy
import random
import sqlite3
import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QWidget

from bj_ui import Ui_MainWindow

# список картинок карт
pictures = ['2_черви.jpg', '2_буби.jpg', '2_пики.jpg', '2_крести.jpg',
            '3_черви.jpg', '3_буби.jpg', '3_пики.jpg', '3_крести.jpg',
            '4_черви.jpg', '4_буби.jpg', '4_пики.jpg', '4_крести.jpg',
            '5_черви.jpg', '5_буби.jpg', '5_пики.jpg', '5_крести.jpg',
            '6_черви.jpg', '6_буби.jpg', '6_пики.jpg', '6_крести.jpg',
            '7_черви.jpg', '7_буби.jpg', '7_пики.jpg', '7_крести.jpg',
            '8_черви.jpg', '8_буби.jpg', '8_пики.jpg', '8_крести.jpg',
            '9_черви.jpg', '9_буби.jpg', '9_пики.jpg', '9_крести.jpg',
            '10_черви.jpg', '10_буби.jpg', '10_пики.jpg', '10_крести.jpg',
            'валет_черви.jpg', 'валет_буби.jpg', 'валет_пики.jpg', 'валет_крести.jpg',
            'дама_черви.jpg', 'дама_буби.jpg', 'дама_пики.jpg', 'дама_крести.jpg',
            'король_черви.jpg', 'король_буби.jpg', 'король_пики.jpg', 'король_крести.jpg',
            'туз_черви.jpg', 'туз_буби.jpg', 'туз_пики.jpg', 'туз_крести.jpg']


class BlackJack(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.need_result = None
        self.con = None
        self.setupUi(self)
        self.start_button.clicked.connect(self.start)  # кнопка "Начать игру"
        self.add_button.clicked.connect(self.add)  # кнопка "Добавить"
        self.leave_button.clicked.connect(self.leave)  # кнопка "Оставить"
        self.close_button.clicked.connect(self.close)  # кнопка "Закрыть"

        self.class_pictures = None  # список карт, который будет скопирован
        self.pixmap = None
        self.hidden_card = None  # перевёрнутая карта банкира

        self.count_of_ace_player = 0  # количество тузов у игрока, если будет перебор, то значение туза станет равным 1
        self.count_of_ace_banker = 0  # количество тузов у банкира, тот же принцип
        self.player_iterator = 0  # это значение потребуется при добавлении карт у игрока
        self.banker_iterator = 0  # это значение потребуется при добавлении карт у банкира
        self.sum_of_players_cards = 0  # сумма значений карт игрока
        self.sum_of_bankers_cards = 0  # сумма значений карт банкира

        self.money_lbl.setText('100')
        self.add_button.setEnabled(False)
        self.leave_button.setEnabled(False)

    def start(self):  # кнопка "Играть"
        if int(self.bet_box.text()) == 0:   # если игрок не сделал ставку
            self.central_label.setText('Ставки нет!')
        elif int(self.money_lbl.text()) < int(self.bet_box.text()):   # если ставка больше количества имеющихся денег
            self.central_label.setText('Недостаточно денег!')
        else:
            # всё заново перезаписывается, чтобы корректно проводилась следующая игра
            self.class_pictures = None
            self.pixmap = QPixmap(f'./cards/white.jpg')
            self.hidden_card = None
            self.count_of_ace_player = 0
            self.count_of_ace_banker = 0
            self.player_iterator = 0
            self.banker_iterator = 0
            self.sum_of_players_cards = 0
            self.sum_of_bankers_cards = 0
            self.players_points.setText('0')
            self.bankers_points.setText('0')
            # все QLabel заполняются белым фоном
            self.label_3.setPixmap(self.pixmap)
            self.label_4.setPixmap(self.pixmap)
            self.label_5.setPixmap(self.pixmap)
            self.label_6.setPixmap(self.pixmap)
            self.label_7.setPixmap(self.pixmap)
            self.label_8.setPixmap(self.pixmap)
            self.label_9.setPixmap(self.pixmap)
            self.label_12.setPixmap(self.pixmap)
            self.label_13.setPixmap(self.pixmap)
            self.label_14.setPixmap(self.pixmap)
            self.label_15.setPixmap(self.pixmap)
            self.label_16.setPixmap(self.pixmap)
            self.label_17.setPixmap(self.pixmap)
            self.label_18.setPixmap(self.pixmap)
            self.add_button.setEnabled(False)
            self.leave_button.setEnabled(False)
            self.start_button.setEnabled(False)
            self.start_button.setText('Начать новую игру')
            self.money_lbl.setText(str(int(self.money_lbl.text()) - int(self.bet_box.text())))   # игрок делает ставку
            self.bet_box.setEnabled(False)
            self.central_label.setText('')

            self.con = sqlite3.connect("cards_db.sqlite")
            # список карт нужно скопировать, ведь карты из него будут удаляться
            self.class_pictures = copy.copy(pictures)
            for i in range(2):  # размещение первых карт игрока
                random_pic = random.choice(self.class_pictures)
                if random_pic == 'туз_черви.jpg' or random_pic == 'туз_буби.jpg' \
                        or random_pic == 'туз_пики.jpg' or random_pic == 'туз_крести.jpg':  # проверяется, есть ли тузы
                    self.count_of_ace_player += 1
                self.class_pictures.remove(random_pic)  # удаление карты из списка
                self.pixmap = QPixmap(f'./cards/{random_pic}')
                # здесь мы находим значения карт игрока и прибавляем к сумме карт игрока
                result = self.con.cursor().execute(f"""SELECT point FROM points
                            WHERE name = '{random_pic}'""").fetchone()[0]
                self.sum_of_players_cards += result
                self.players_points.setText(str(self.sum_of_players_cards))
                # здесь мы их размещаем
                if i == 0:
                    self.label_1.setPixmap(self.pixmap)
                else:
                    self.label_2.setPixmap(self.pixmap)

            for i in range(2):  # размещение первых карт банкира
                random_pic = random.choice(self.class_pictures)
                self.class_pictures.remove(random_pic)  # удаление карты из списка
                if random_pic == 'туз_черви.jpg' or random_pic == 'туз_буби.jpg' \
                        or random_pic == 'туз_пики.jpg' or random_pic == 'туз_крести.jpg':  # проверяется, есть ли тузы
                    self.count_of_ace_player += 1
                self.pixmap = QPixmap(f'./cards/{random_pic}')
                # находим значения карт банкира и прибавляем к сумме карт банкира
                result = self.con.cursor().execute(f"""SELECT point FROM points
                                        WHERE name = '{random_pic}'""").fetchone()[0]
                self.sum_of_bankers_cards += result
                # размещение карт банкира
                if i == 0:
                    self.label_10.setPixmap(self.pixmap)
                    self.need_result = result   # т. к. вторая карта скрыта, игрок не должен видеть её очки
                else:
                    self.hidden_card = random_pic  # перевёрнутая карта
                    self.pixmap = QPixmap('./cards/nothing.jpg')
                    self.label_11.setPixmap(self.pixmap)
            self.bankers_points.setText(str(self.need_result))
            # теперь игрок может нажать на кнопки "Добавить" и "Оставить"
            self.add_button.setEnabled(True)
            self.leave_button.setEnabled(True)

    def add(self):  # кнопка "Добавить"
        # изменение очков, если перебор, и есть тузы
        while self.sum_of_players_cards > 21 and self.count_of_ace_player:
            self.sum_of_players_cards -= 10
            self.count_of_ace_player -= 1
            self.players_points.setText(str(self.sum_of_players_cards))
        if self.sum_of_players_cards <= 21:
            random_pic = random.choice(self.class_pictures)
            if random_pic == 'туз_черви.jpg' or random_pic == 'туз_буби.jpg' \
                    or random_pic == 'туз_пики.jpg' or random_pic == 'туз_крести.jpg':  # проверяется, есть ли тузы
                self.count_of_ace_player += 1
            self.class_pictures.remove(random_pic)
            self.pixmap = QPixmap(f'./cards/{random_pic}')
            # нахождение значений карт игрока
            result = self.con.cursor().execute(f"""SELECT point FROM points
                                        WHERE name = '{random_pic}'""").fetchone()[0]
            self.sum_of_players_cards += result
            self.players_points.setText(str(self.sum_of_players_cards))
            # размещение карт игрока
            # везде стоит if, чтобы появилась карта, из-за которой произошёл перебор
            if self.player_iterator == 0:
                self.label_3.setPixmap(self.pixmap)
            if self.player_iterator == 1:
                self.label_4.setPixmap(self.pixmap)
            if self.player_iterator == 2:
                self.label_5.setPixmap(self.pixmap)
            if self.player_iterator == 3:
                self.label_6.setPixmap(self.pixmap)
            if self.player_iterator == 4:
                self.label_7.setPixmap(self.pixmap)
            if self.player_iterator == 5:
                self.label_8.setPixmap(self.pixmap)
            if self.player_iterator == 6:
                self.label_9.setPixmap(self.pixmap)
            if self.sum_of_players_cards > 21:
                self.central_label.setText('Проигрыш!')
                self.bet_box.setEnabled(True)
                # теперь игрок не сможет нажать на кнопки "Добавить" и "Оставить"
                self.add_button.setEnabled(False)
                self.leave_button.setEnabled(False)
                self.start_button.setEnabled(True)
            # значение увеличивается, чтобы карты были на месте незаполненных объектов QLabel
            self.player_iterator += 1

    def leave(self):  # кнопка "Оставить"
        # теперь игрок не сможет нажать на кнопки "Добавить" и "Оставить"
        self.add_button.setEnabled(False)
        self.leave_button.setEnabled(False)
        self.pixmap = QPixmap(f'./cards/{self.hidden_card}')
        self.label_11.setPixmap(self.pixmap)  # размещение скрытой карты
        # карты добавляются до тех пор, пока сумма значений карт банкира не достигнет 17
        while self.sum_of_bankers_cards < 17:
            random_pic = random.choice(self.class_pictures)
            if random_pic == 'туз_черви.jpg' or random_pic == 'туз_буби.jpg' \
                    or random_pic == 'туз_пики.jpg' or random_pic == 'туз_крести.jpg':  # проверяется, есть ли туз
                self.count_of_ace_banker += 1
            # изменение очков, если перебор, и есть тузы
            while self.sum_of_bankers_cards > 21 and self.count_of_ace_banker:
                self.sum_of_bankers_cards_cards -= 10
                self.count_of_ace_banker -= 1
                self.bankers_points.setText(str(self.sum_of_bankers_cards))
            self.class_pictures.remove(random_pic)
            self.pixmap = QPixmap(f'./cards/{random_pic}')
            # нахождение значений карт банкира
            result = self.con.cursor().execute(f"""SELECT point FROM points
                                        WHERE name = '{random_pic}'""").fetchone()[0]
            self.sum_of_bankers_cards += result
            self.bankers_points.setText(str(self.sum_of_bankers_cards))
            # размещение карт банкира
            if self.banker_iterator == 0:
                self.label_12.setPixmap(self.pixmap)
            elif self.banker_iterator == 1:
                self.label_13.setPixmap(self.pixmap)
            elif self.banker_iterator == 2:
                self.label_14.setPixmap(self.pixmap)
            elif self.banker_iterator == 3:
                self.label_15.setPixmap(self.pixmap)
            elif self.banker_iterator == 4:
                self.label_16.setPixmap(self.pixmap)
            elif self.banker_iterator == 5:
                self.label_17.setPixmap(self.pixmap)
            else:
                self.label_18.setPixmap(self.pixmap)
            self.banker_iterator += 1
        else:
            self.bankers_points.setText(str(self.sum_of_bankers_cards))
            # выявляется, чья победа
            if self.sum_of_bankers_cards > 21 or self.sum_of_players_cards > self.sum_of_bankers_cards:
                # если очков у банкира больше, чем у игрока, и у банкира нет перебора
                self.central_label.setText('Выигрыш!')
                self.money_lbl.setText(str(int(self.money_lbl.text()) + 2 * int(self.bet_box.text())))
            elif self.sum_of_players_cards == self.sum_of_bankers_cards:
                self.central_label.setText('Ничья!')  # если очков у банкира столько же, сколько у игрока
                self.money_lbl.setText(str(int(self.money_lbl.text()) + int(self.bet_box.text())))
            else:
                # если очков у банкира меньше, чем у игрока, и у игрока нет перебора
                self.central_label.setText('Проигрыш!')
        self.start_button.setEnabled(True)
        self.bet_box.setEnabled(True)

    def close(self):  # кнопка "Закрыть"
        value, ok_pressed = QInputDialog.getItem(  # диалоговое окно
            self, "Выберите вариант ответа.", "Выйти?",
            ("Нет", "Да"), 1, False)
        if ok_pressed:
            if value == 'Да':
                self.con.close()
                QWidget.close(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = BlackJack()
    form.show()
    sys.exit(app.exec())
