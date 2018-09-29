"""
Author: Kristian Saure Knotten
Student ID: 8284
E-mail: ksknotten@outlook.com
"""

# Importere offisielle biblotek
from tkinter import *
from random import randint
from time import sleep
import threading


# Sette ein GUI klass som styrer GUI til spelet
class GUI:
    def __init__(self, cards_amount, game, img, server_client=''):
        # Sett variablar for og enkelt kunne endre på dei i heile klassa
        self.player1 = None
        self.player2 = None
        self.network = False
        self.last_choice = None
        self.chosen_card = None
        self.cards = {}
        self.game = game
        self.cards_disabled = False
        self.img = img
        self.cards_amount = cards_amount

        # Sjekke om eigaren av denne klassa er ein klient eller ikkje, send så gui klassa til game klassa
        if server_client == 'client':
            self.game.client_gui = self
        else:
            self.game.server_gui = self

        # Lag til vindauget som spelet skal vere i. Lag også til 2 frames; 1 til informasjon og ein for spelet
        self.root = Tk()
        self.root.title('Memory Game')
        # self.root.geometry('400x450')
        # Styrer informasjon som poenga til dei to spelarane
        self.f_information = Frame(self.root, borderwidth=4, relief="ridge", width=10, height=20)
        self.f_information.pack(side=TOP, anchor=N)
        # Styrer korta i spelet
        self.f_game = Canvas(self.root)
        self.f_game.pack(side=TOP, anchor=N)

        # Start og fyll inn informasjon framen
        self.l_player1, self.l_player2 = self.information_gui()
        # Om spelaren er ein klient skal han lage eit eige bord
        if not self.game.client_gui:
            self.make_game_gui()

    # Funksjon som lager widgets til informasjon framen
    def information_gui(self):
        #title = Label(self.f_information, image=self.img)
        #title.pack(pady=(0, 25))

        player1 = Label(self.f_information, width=15, height=1, relief="ridge", bd=5)
        player1.pack(side=RIGHT, padx=10, pady=10)

        player2 = Label(self.f_information, width=15, height=1, relief="ridge", bd=2)
        player2.pack(side=LEFT, padx=10, pady=10)
        return player1, player2

    # Funksjon som lager widgets til game framen, lager lista som korta ligg i ved hjelp av make_board funkjsonen
    def make_game_gui(self):
        column, row, num, card_number = 0, 0, 0, 0
        x, y = self.cards_amount.split('x')
        for card in range(1, int(x) * int(y) + 1):
            column, row, card_number = self.make_board(int(y) - 1, row, column, card_number, int(x) * int(y), num)
            num += 1

    # Lager korta i ein grid og lagrer dei i ein liste variabel
    def make_board(self, max_column, row, column, card_number, amount_cards, num):
        var = 'card {}'.format(num)
        font = ("Courier", 50)
        while True:
            # Finn ein verdi som er ledig, skal vere 2 kort med same verdi i lista
            random_int = randint(1, amount_cards / 2)
            if self.check_card_number(random_int):
                self.cards[var] = [Label(self.f_game, text=' ', borderwidth=4, relief="groove", bg='moccasin',
                                         font=font, height=1, width=2), random_int, card_number]
                card_number += 1
                break

        self.cards[var][0].grid(row=row, column=column, pady=2)
        self.cards[var][0].pack_propagate(0)
        # Bind labelane til fleire eventer
        self.cards[var][0].bind("<Button-1>", self.card_click)
        self.cards[var][0].bind("<Enter>", self.card_enter)
        self.cards[var][0].bind("<Leave>", self.card_leave)
        if column == max_column:
            row += 1
            column = 0
        else:
            column += 1
        return column, row, card_number

    # Versjon som lager korta frå ein eksiterande liste. Denne er får klienten
    def make_client_board(self):
        x, y = self.cards_amount.split('x')
        row, column, max_column = 0, 0, int(y) - 1
        font = ("Courier", 50)
        for key, card in self.cards.items():
            label = Label(self.f_game, text=' ', borderwidth=4, relief="groove", bg='moccasin', font=font, width=2,
                          height=1)
            card[0] = label
            card[0].grid(row=row, column=column, pady=2)
            card[0].pack_propagate(0)
            card[0].bind("<Button-1>", self.card_click)
            card[0].bind("<Enter>", self.card_enter)
            card[0].bind("<Leave>", self.card_leave)
            if column == max_column:
                row += 1
                column = 0
            else:
                column += 1

    # Sjekk om num verdien er 2 av i kort listen
    def check_card_number(self, num):
        for value in self.cards.values():
            if value[1] == num:
                for x in self.cards.values():
                    if x != value and x[1] == num:
                        return False
        return True

    # Gå igjennom korta på bordet som ikkje er valgt og reset korta
    def reset_board(self):
        sleep(1)
        for card, x, y in self.cards.values():
            card.config(text=' ', bg='moccasin')

    # Oppdater scoren til spelarane
    def update_score(self):
        try:
            self.l_player2.config(text='{} = {}'.format(self.player2.name, self.player2.points))
            self.l_player1.config(text='{} = {}'.format(self.player1.name, self.player1.points))
        except AttributeError:
            pass

    # Om 2 kort er rett vil denne funksjonen fjerne korta fra lista og fjerne events frå dei korta
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

    # Funksjonen som kjører når spelaren trykker på eit kort
    def card_click(self, event):
        self.cards_disabled = True
        self.game.card_clicked(event, self.cards)
        self.cards_disabled = False

    # Funksjonen som kjører når nåken har musen over eit kort
    def card_enter(self, event):
        # Sjekk om det er nettverk spel, vist det er spelarens tur, endre fargen til lys blå
        if self.game.network:
            if self.game.client_gui:
                if self.game.player2 == self.game.choosing_player:
                    if event.widget.cget('text') == ' ':
                        event.widget.config(bg='light blue')
                        event.widget.update_idletasks()

            elif self.game.server_gui:
                if self.game.player1 == self.game.choosing_player:
                    if event.widget.cget('text') == ' ':
                        event.widget.config(bg='light blue')
                        event.widget.update_idletasks()
        else:
            if event.widget.cget('text') == ' ':
                event.widget.config(bg='light blue')
                event.widget.update_idletasks()

    # Funksjonen når musen går ut av ei kort; fjerner den lys blå fargen
    def card_leave(self, event):
        if event.widget.cget('text') == ' ':
            event.widget.config(bg='moccasin')
            event.widget.update_idletasks()

    # Snur det kortet som blei klikka på
    def turn_card(self, num):
        for key, card in self.cards.items():
            if card[2] == num:
                card[0].config(text=card[1])
                card[0].update_idletasks()
                break

    # Endre på gui og merk den nye spelaren
    def switch_turn(self, player_num):
        if player_num == 1:
            self.l_player1.config(bd=2)
            self.l_player2.config(bd=5)
        else:
            self.l_player2.config(bd=2)
            self.l_player1.config(bd=5)

    # Tar ein frame og fjerner alt i den widgeten
    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    # Clear framen og legg til ein quit knapp og ein beskjed når spelet er ferdig
    def message(self, msg, title):
        self.clear_frame(self.f_game)
        self.root.title('Game won!')
        Label(self.f_game, text=msg).pack(pady=8)
        Button(self.f_game, text='Quit', command=quit).pack(side=BOTTOM, pady=14)


# Ein klasse for spelarane, tar inn namn, nummer, gui å gamen til spelet
class Player:
    def __init__(self, name, number, gui, game):
        # Set fleire variablar som enkelt kan hentast i klassa seinare
        self.points = 0
        self.player_number = number
        self.name = name
        # Om spelaren ikkje har sett eit namn so sett det til Player 1 eller Player 2
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
        # Oppdater informasjons framen
        gui.update_score()


# Ein klasse som styrer gamen
class Game:
    def __init__(self):
        # Set fleire variablar som enkelt kan hentast i klassa seinare
        self.pick = 0
        self.last_choice = None
        self.current_choice = None
        self.client_gui = None
        self.server_gui = None
        self.network = None
        self.choosing_player = None
        self.player1, self.player2 = None, None

    # Event som kjører når ein spelar trykker på eit kort. Om det er eit nettverk so sjekk om det er spelarens tur
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

    # Sjekk om spelaren kan snu kortert, legg det valgte kortet til current choice eller last choice alt etter
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
        # Om det er valg nr 2 til spelaren
        if self.pick == 1:
            if self.client_gui:
                self.client_gui.reset_board()
            else:
                self.server_gui.reset_board()
            self.player_choose()
            # Sjekk om ein spelar har vunnet (kun for lokalt spel)
            if not self.network and self.server_gui.cards == {}:
                self.check_win()
                return
            self.pick = 0
            self.switch_player_turn()
            # Send oppdatering til klient eller server om dei valgte korta
            if self.network:
                threading.Thread(target=self.send_updates).start()
        else:
            self.last_choice = self.current_choice
            self.pick += 1

    # Endre på kven sin tur det er, setter choosing_player til den spelaren som velger og oppdaterer GUI
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

    # Kjører når ein spelar har valgt dei 2 korta
    def player_choose(self):
        # Sjekker om dei 2 korta hadde same verdi; om dei er like gi spelaren poeng og oppdater GUI
        if self.current_choice[0] == self.last_choice[0]:
            self.choosing_player.points += 1
            if self.client_gui:
                self.client_gui.card_taken(self.current_choice[1], self.last_choice[1])
                self.client_gui.update_score()

            else:
                self.server_gui.card_taken(self.current_choice[1], self.last_choice[1])
                self.server_gui.update_score()

        if not self.network:
            self.current_choice, self.last_choice = None, None

    # Funksjon som sender oppdatering til den andre spelaren på serveren og venter på ny oppdatering
    def send_updates(self):
        if self.client_gui:
            self.network.send([self.current_choice, self.last_choice])
            # Om kort lista er tom så sjekk kven vinnaren er
            if self.client_gui.cards == {}:
                self.check_win()
                return
            self.current_choice, self.last_choice = self.network.receive()
            self.receive_update()

        # Same koda som over men for serveren istaden for klienten
        elif self.server_gui:
            self.network.send([self.current_choice, self.last_choice])
            if self.server_gui.cards == {}:
                self.check_win()
                return
            self.current_choice, self.last_choice = self.network.receive()
            self.receive_update()

    # Kjører når spelaren venter på oppdatering frå den andre spelaren på serveren
    def receive_update(self):
        if self.client_gui:
            self.client_gui.reset_board()
        else:
            self.server_gui.reset_board()

        # Sjekk om dei 2 korta som den andre spelaren valgt er like, om ikkje; vis dei i 2 sekunder
        if self.current_choice[0] != self.last_choice[0]:
            self.show_opponent_picks()
        self.player_choose()

        if self.client_gui and self.client_gui.cards == {}:
            self.check_win()
            return
        if self.server_gui and self.server_gui.cards == {}:
            self.check_win()
            return

        self.pick = 0
        self.switch_player_turn()
        self.current_choice, self.last_choice = None, None

    # Viser kva den andre spelaren valgte i nokre sekunder før dei forsvinner igjen
    def show_opponent_picks(self):
        if self.client_gui:
            self.client_gui.turn_card(self.current_choice[1])
            self.client_gui.turn_card(self.last_choice[1])
            sleep(0.5)
            self.client_gui.reset_board()
        else:
            self.server_gui.turn_card(self.current_choice[1])
            self.server_gui.turn_card(self.last_choice[1])
            sleep(0.5)
            self.server_gui.reset_board()

    # Kjører på starten når klienten starter opp spelet. Klienten startar og ta i mot beskjeder frå server
    def client_start(self):
        self.current_choice, self.last_choice = self.network.receive()
        self.receive_update()

    # Starar opp GUI og spelet
    def start_local_game(self):
        if self.client_gui:
            threading.Thread(target=self.client_start).start()
            self.client_gui.root.mainloop()
        else:
            self.server_gui.root.mainloop()

    # Sjekker kven som har vunnet og sender så beskjed til spelaren om resultatet
    def check_win(self):
        if self.client_gui:
            if self.player1.points > self.player2.points:
                self.client_gui.message('{} won the game with {} points'.format(self.player1.name, self.player1.points),
                                        'Winner!')
            elif self.player2.points > self.player1.points:
                self.client_gui.message('{} won the game with {} points'.format(self.player2.name, self.player2.points),
                                        'Winner!')
            elif self.player1.points == self.player2.points:
                self.client_gui.message('It\'s a draw', 'Draw!')
        else:
            if self.player1.points > self.player2.points:
                self.server_gui.message('{} won the game with {} points'.format(self.player1.name, self.player1.points),
                                        'Winner!')
            elif self.player2.points > self.player1.points:
                self.server_gui.message('{} won the game with {} points'.format(self.player2.name, self.player2.points),
                                        'Winner!')
            elif self.player1.points == self.player2.points:
                self.server_gui.message('It\'s a draw', 'Draw!')
