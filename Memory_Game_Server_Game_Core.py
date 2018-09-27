"""
Author: Kristian Saure Knotten
Student ID: 8284
E-mail: ksknotten@outlook.com
"""

from tkinter import *
from random import randint
from time import sleep
import threading


class GUI:
    def __init__(self, cards_amount, game, server_client=''):
        self.player1 = None
        self.player2 = None
        self.network = False
        self.last_choice = None
        self.chosen_card = None
        self.cards = {}
        self.game = game

        if server_client == 'client':
            self.game.client_gui = self
        else:
            self.game.server_gui = self

        self.cards_amount = cards_amount
        self.root = Tk()
        self.f_information = Frame(self.root, borderwidth=4, relief="ridge", width=10, height=20)
        self.f_information.pack(side=TOP, anchor=N)
        self.f_game = Canvas(self.root)
        self.f_game.pack(side=TOP, anchor=N)
        self.l_player1, self.l_player2 = self.information_gui()
        self.make_game_gui()

    def information_gui(self):
        player1 = Label(self.f_information, width=15, height=1, relief="ridge", bd=5)
        player1.pack(side=RIGHT, padx=10, pady=10)

        player2 = Label(self.f_information, width=15, height=1, relief="ridge", bd=2)
        player2.pack(side=LEFT, padx=10, pady=10)
        return player1, player2

    def make_game_gui(self):
        column, row, num, card_number = 0, 0, 0, 0
        x, y = self.cards_amount.split('x')
        for card in range(1, int(x) * int(y) + 1):
            column, row, card_number = self.make_board(int(y) - 1, row, column, card_number, int(x) * int(y), num)
            num += 1

    def make_board(self, max_column, row, column, card_number, amount_cards, num):
        var = 'card {}'.format(num)
        while True:
            random_int = randint(1, amount_cards / 2)
            if self.check_card_number(random_int):
                self.cards[var] = [Label(self.f_game, text=' ', borderwidth=4, relief="groove", bg='moccasin',
                                         width=4, height=3), random_int, card_number]
                card_number += 1
                break

        self.cards[var][0].grid(row=row, column=column, pady=2)
        self.cards[var][0].bind("<Button-1>", self.card_click)
        # Game.cards[var][0].bind("<Enter>", self.card_enter)
        # Game.cards[var][0].bind("<Leave>", self.card_leave)
        if column == max_column:
            row += 1
            column = 0
        else:
            column += 1
        return column, row, card_number

    def make_client_board(self):
        x, y = self.cards_amount.split('x')
        row, column, max_column = 0, 0, int(y) - 1
        for key, card in self.cards.items():
            label = Label(self.f_game, text=' ', borderwidth=4, relief="groove", bg='moccasin', width=4, height=3)
            card[0] = label
            card[0].grid(row=row, column=column, pady=2)
            card[0].bind("<Button-1>", self.card_click)
            # card[0].bind("<Enter>", self.card_enter)
            # card[0].bind("<Leave>", self.card_leave)
            if column == max_column:
                row += 1
                column = 0
            else:
                column += 1

    def check_card_number(self, num):
        for value in self.cards.values():
            if value[1] == num:
                for x in self.cards.values():
                    if x != value and x[1] == num:
                        return False
        return True

    def reset_board(self):
        self.disable_cards()
        sleep(1)
        for card, x, y in self.cards.values():
            card.config(text=' ', bg='moccasin')
        self.disable_cards(False)

    def disable_cards(self, disable=True):
        if disable:
            for card, x, y in self.cards.values():
                card.unbind("<Button-1>")
        else:
            for card, x, y in self.cards.values():
                card.bind("<Button-1>", self.card_click)

    def update_score(self):
        try:
            self.l_player2.config(text='{} = {}'.format(self.player2.name, self.player2.points))
            self.l_player1.config(text='{} = {}'.format(self.player1.name, self.player1.points))
        except AttributeError:
            pass

    def card_taken(self, card1, card2):
        delete_keys = []
        for key, card in self.cards.items():
            if card[2] == card1 or card[2] == card2:
                card[0].unbind("<Button-1>")
                card[0].config(bg='dim gray', text=card[1])
                card[0].update_idletasks()
                delete_keys.append(key)

        del self.cards[delete_keys[0]]
        del self.cards[delete_keys[1]]

    def card_click(self, event):
        self.game.card_clicked(event, self.cards)

    def turn_card(self, num):
        for key, card in self.cards.items():
            if card[2] == num:
                card[0].config(text=card[1])
                card[0].update_idletasks()
                break

    def switch_turn(self, player_num):
        if player_num == 1:
            self.l_player1.config(bd=2)
            self.l_player2.config(bd=5)
        else:
            self.l_player2.config(bd=2)
            self.l_player1.config(bd=5)

    def message(self, msg, title):
        win = Toplevel()
        win.wm_geometry('250x100')
        win.title(title)
        Label(win, text=msg).pack(pady=8)
        Button(win, text='Quit', command=quit).pack(side=BOTTOM, pady=14)


class Player:
    def __init__(self, name, number, gui, game):

        self.points = 0
        self.player_number = number
        self.name = name
        if name == '' or name == ' ':
            self.name = 'Player ' + str(number)
        if number == 1:
            gui.player1 = self
            gui.choosing_player = self
            game.player1 = self
            game.choosing_player = self
        elif number == 2:
            gui.player2 = self
            game.player2 = self
        gui.update_score()


class Game:
    def __init__(self):
        self.pick = 0
        self.last_choice = None
        self.current_choice = None
        self.client_gui = None
        self.server_gui = None
        self.network = None
        self.choosing_player = None
        self.player1, self.player2 = None, None

    def card_clicked(self, event, card_list):
        if self.network:
            if self.client_gui:
                if self.player2 == self.choosing_player:
                    self.turn_cards(event, card_list)
                    pass
                else:
                    print('not your turn')
                    return
            elif self.server_gui:
                if self.player1 == self.choosing_player:
                    self.turn_cards(event, card_list)
                    pass
                else:
                    print('not your turn')
                    return
        else:
            self.turn_cards(event, card_list)

    def turn_cards(self, event, card_list):
        if self.pick <= 1:
            if event and card_list:
                for key, card in card_list.items():
                    if card[0] == event.widget:
                        if self.last_choice:
                            if card[2] != self.last_choice[1]:
                                if self.client_gui:
                                    self.client_gui.turn_card(card[2])
                                else:
                                    self.server_gui.turn_card(card[2])
                                self.current_choice = [card[1], card[2]]
                                break
                            else:
                                return
                        else:
                            if self.client_gui:
                                self.client_gui.turn_card(card[2])
                            else:
                                self.server_gui.turn_card(card[2])
                            self.current_choice = [card[1], card[2]]
                            break
            else:
                return

        if self.pick == 1:
            if self.client_gui:
                self.client_gui.reset_board()
            else:
                self.server_gui.reset_board()
            self.player_choose()
            self.pick = 0
            self.switch_player_turn()
            if self.network:
                threading.Thread(target=self.send_updates).start()
        else:
            self.last_choice = self.current_choice
            self.pick += 1

    def switch_player_turn(self):
        if self.choosing_player == self.player1:
            self.choosing_player = self.player2
            if self.client_gui:
                self.client_gui.switch_turn(1)
            else:
                self.server_gui.switch_turn(1)

        elif self.choosing_player == self.player2:
            self.choosing_player = self.player1
            if self.client_gui:
                self.client_gui.switch_turn(2)
            else:
                self.server_gui.switch_turn(2)

    def player_choose(self):
        if self.current_choice[0] == self.last_choice[0]:
            self.choosing_player.points += 1
            if self.client_gui:
                self.client_gui.card_taken(self.current_choice[1], self.last_choice[1])
                self.client_gui.update_score()
                if self.client_gui.cards == {}:
                    self.check_win()
            else:
                self.server_gui.card_taken(self.current_choice[1], self.last_choice[1])
                self.server_gui.update_score()
                if self.server_gui.cards == {}:
                    self.check_win()

        if not self.network:
            self.current_choice, self.last_choice = None, None

    def send_updates(self):
        if self.client_gui:
            self.network.send([self.current_choice, self.last_choice])
            self.current_choice, self.last_choice = self.network.receive()
            self.receive_update()

        elif self.server_gui:
            self.network.send([self.current_choice, self.last_choice])
            self.current_choice, self.last_choice = self.network.receive()
            self.receive_update()

    def receive_update(self):
        if self.client_gui:
            self.client_gui.reset_board()
        else:
            self.server_gui.reset_board()

        self.player_choose()
        self.pick = 0
        self.switch_player_turn()
        self.current_choice, self.last_choice = None, None

    def client_start(self):
        self.current_choice, self.last_choice = self.network.receive()
        self.receive_update()

    def start_local_game(self):
        if self.client_gui:
            threading.Thread(target=self.client_start).start()
            self.client_gui.root.mainloop()
        else:
            self.server_gui.root.mainloop()

    def check_win(self):
        if self.client_gui:
            if self.player1.points > self.player2.points:
                self.client_gui.message('{} won the game with {} points'.format(self.player1.name, self.player1.points),
                                        'Winner!')
            if self.player2.points > self.player1.points:
                self.client_gui.message('{} won the game with {} points'.format(self.player2.name, self.player2.points),
                                        'Winner!')
            if self.player1.points == self.player2.points:
                self.client_gui.message('It\'s a draw', 'Draw!')
        else:
            if self.player1.points > self.player2.points:
                self.server_gui.message('{} won the game with {} points'.format(self.player1.name, self.player1.points),
                                        'Winner!')
            if self.player2.points > self.player1.points:
                self.server_gui.message('{} won the game with {} points'.format(self.player2.name, self.player2.points),
                                        'Winner!')
            if self.player1.points == self.player2.points:
                self.server_gui.message('It\'s a draw', 'Draw!')
