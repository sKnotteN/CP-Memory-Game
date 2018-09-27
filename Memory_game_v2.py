"""
Author: Kristian Saure Knotten
Student ID: 8284
E-mail: ksknotten@outlook.com
"""

# Hent dei andre python scripta
import Memory_Game_Server_Game_Core
import Memory_Game_Networking as Networking

# Importer offisielle libs
from tkinter import *
from tkinter import messagebox
import threading


# Lag ein root vindauge for houvd menyen
menu_root = Tk()
menu_root.geometry('400x400')


# Ein klasse for main menu som er hovud menyen der du velger og setter alle innstillinger. Bestemmer over lokalt spel
class Mainmenu:
    def __init__(self):
        # Set variablar som ein enkelt kan endre på igjennom heile classen
        self.game = Memory_Game_Server_Game_Core.Game()
        self.game_gui = None
        self.network_menu = None
        self.name1, self.name2, self.card_amount = '', '', ''
        self.name1_entry, self.name2_entry, self.card_amount_entry = None, None, None

        # Lag frames som skal innehalde forskjellig informasjon. f_user_input skal vere til player input
        self.f_information = Frame(menu_root)
        self.f_information.pack(fill=None, expand=False)
        self.f_user_input = Frame(menu_root)
        self.f_user_input.place(relx=.5, rely=.5, anchor="c")
        self.game_title_frame, self.game_info_frame = self.information_frame()

        # Start og lag vindauget
        self.user_input_frame()

    # Setter inn informasjonen som skal vere i informasjons framen, Informasjon om spelet og titel på spelet
    def information_frame(self):
        title = Label(self.f_information, width=20, text='Game title')
        title.pack()
        info = Label(self.f_information, width=20, height=4, text='This game is a')
        info.pack()
        return title, info

    # Gjer klar user_input framen som skal innehalde widget som skal samle inn informasjon om spelarane
    def user_input_frame(self, command=None):
        # Sjekk om funksjonen he fått tilsendt kommandoen 'name'. Vist 'name' så fjern alt i framen og legg til nytt.
        if command == 'name':
            self.clear_frame(self.f_user_input)
            return self.create_input_widgets(self.f_user_input)
        # Lag til hovud menyen der en velger mellom lokal eller nettverk. Quit er og her.
        else:
            local = Button(self.f_user_input, text='Local play', command=self.local_play)
            local.grid(column=0, row=0, pady=10)
            network = Button(self.f_user_input, text='Network play', command=self.network_play)
            network.grid(column=0, row=1)
            b_quit = Button(self.f_user_input, text='Quit Game', command=quit)
            b_quit.grid(row=2, pady=20)

    # Lag til user_input framen med options for spelet.
    def create_input_widgets(self, frame):
        # Lag ei liste med dei mulige størrelsane på spelet
        text1 = Label(frame, text='Amount of cards: ')
        text1.grid(column=0, row=2)
        card_amount = Listbox(frame, selectmode=EXTENDED, height=4)
        card_amount.insert(1, '3x4')
        card_amount.insert(2, '5x6')
        card_amount.insert(3, '8x8')
        card_amount.insert(4, '10x10')
        card_amount.select_set(0)
        card_amount.grid(column=1, row=2)

        # Lag ein start knapp, tilbake knapp og ein quit knapp
        b_back = Button(frame, text='Back', command=self.back_button)
        b_back.grid(column=0, row=3, pady=20)
        b_play = Button(frame, text='Start Game', command=self.start_button)
        b_play.grid(column=1, row=3)
        b_quit = Button(frame, text='Quit Game', command=quit)
        b_quit.grid(columnspan=2, row=4)

        # Lag til for at spelaren skal kunne legge inn namn til spelar 1 og spelar 2.
        text1 = Label(frame, text='Player name: ')
        text1.grid(column=0, row=0)
        name = Entry(frame)
        name.grid(pady=5, padx=15, column=1, row=0)
        text2 = Label(frame, text='Player 2 name: ')
        text2.grid(column=0, row=1)
        name2 = Entry(frame)
        name2.grid(pady=5, column=1, row=1)

        # Send tilbake alle entry widgets som trengst.
        return name, name2, card_amount

    # Når back knappen blir trykt; fjern alt frå framen og lag nytt. Tøm og variablar.
    def back_button(self):
        self.clear_frame(self.f_user_input)
        self.user_input_frame()
        self.name1_entry, self.name2_entry, self.card_amount_entry = None, None, None
        self.name1, self.name2, self.card_amount = '', '', ''

    # Når start knappen blir trykt; sjekk kva input brukaren har gitt og send det vidare til spelet.
    def start_button(self):
        self.card_amount = self.card_amount_entry.get(ACTIVE)
        self.name1 = self.name1_entry.get()
        self.name2 = self.name2_entry.get()
        self.send_info()

    # Når network knappen blir trykt; Lag ein ny class for nettverk speling or clear framen. Sjekk NetworkMenu class.
    def network_play(self):
        self.clear_frame(self.f_user_input)
        self.network_menu = NetworkMenu(self, self.game)

    # Når local play knappen blir trykt; Lag til user_input framen med muligheite til go skrive inn namn og størrelse.
    def local_play(self):
        self.name1_entry, self.name2_entry, self.card_amount_entry = self.user_input_frame('name')

    # Tar i mot ein frame og fjerner alle widgets som er inn i.
    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    # Send all infoen til game scriptet (Memory_Game_Server_Game_core
    def send_info(self):
        self.game_gui = Memory_Game_Server_Game_Core.GUI(self.card_amount, self.game)
        self.player1 = Memory_Game_Server_Game_Core.Player(self.name1, 1, self.game_gui, self.game)
        self.player2 = Memory_Game_Server_Game_Core.Player(self.name2, 2, self.game_gui, self.game)
        menu_root.destroy()

    def message(self, msg, title):
        win = Toplevel()
        win.wm_geometry('250x100')
        win.title(title)
        Label(win, text=msg).pack(pady=8)
        Button(win, text='Quit', command=quit).pack(side=BOTTOM, pady=14)


class NetworkMenu(Mainmenu):
    def __init__(self, main_menu, game):
        # super().__init__()
        self.main_menu = main_menu
        self.game, self.game_gui = game, None
        self.name, self.client_name, self.card_amount = '', '', ''
        self.name_entry, self.card_amount_entry = None, None
        self.network = None
        self.win = None
        self.t = None
        self.s_ip = ''
        self.player1, self.player2 = None, None
        self.name_input, self.ip_input = '', ''

        self.make_window()

    def make_window(self):
        self.f_server_user_input = Frame(menu_root)
        self.f_server_user_input.place(relx=.5, rely=.5, anchor="c")
        self.name_entry, self.card_amount_entry = self.create_server_input_widgets(self.f_server_user_input)

    def create_server_input_widgets(self, frame):
        text1 = Label(frame, text='Amount of cards: ')
        text1.grid(column=0, row=2)
        card_amount = Listbox(frame, selectmode=EXTENDED, height=4)
        card_amount.insert(1, '3x4')
        card_amount.insert(2, '5x6')
        card_amount.insert(3, '8x8')
        card_amount.insert(4, '10x10')
        card_amount.select_set(0)
        card_amount.grid(column=1, row=2)

        b_back = Button(frame, text='Back', command=self.back_b)
        b_back.grid(column=0, row=3, pady=20)
        b_play = Button(frame, text='Host game', command=self.waiting_for_client)
        b_play.grid(column=1, row=3)
        b_find = Button(frame, text='Find game', command=self.server_info)
        b_find.grid(column=2, row=3)
        b_quit = Button(frame, text='Quit Game', command=quit)
        b_quit.grid(columnspan=1, column=1, row=4)

        text1 = Label(frame, text='Player name: ')
        text1.grid(column=0, row=0)
        name = Entry(frame)
        name.grid(pady=5, padx=15, column=1, row=0)
        return name, card_amount

    def back_b(self):
        self.clear_frame(self.f_server_user_input)
        self.f_server_user_input.place_forget()
        self.main_menu.user_input_frame()
        try:
            self.network.close
        except AttributeError:
            pass

    def server_info(self):
        self.message2('Name: ', 'Your name', self.close_message, 'Connect')

    def waiting_for_client(self):
        self.message2('Name:', 'Host a server', self.close_message_server_host, 'Start server', True)

    def thread_networking_server(self):
        threading.Thread(target=self.host_game).start()

    def thread_networking_client(self):
        threading.Thread(target=self.find_server).start()

    def host_game(self):
        self.player1, self.player2 = None, None
        # self.card_amount = self.card_amount_entry.get(ACTIVE)
        # self.name = self.name_entry.get()
        self.network = Networking.Server('127.0.0.1', 5000)
        if self.network.look() == 'Connected':
            data = self.network.receive()
            if data.startswith('name:'):
                data, name = data.split(' ')
                self.network.send('Connected')
                self.client_name = name
                self.server_start_game()

    def find_server(self):
        self.network = Networking.Client(self.s_ip, 5000)
        self.network.look()
        self.network.send('name: ' + str(self.name))
        answer = self.network.receive()
        if answer == 'No server found':
            messagebox.showinfo('No server found', 'Was not able to find a server')
        elif answer == 'Connected':
            answer2 = self.network.receive()
            self.card_amount, self.name, self.client_name = answer2[0], answer2[1], answer2[2]

            threading.Thread(target=self.thread_client_start_game).start()
            menu_root.destroy()

    def message2(self, msg, title, button_event, button_text, host_server=False):
        self.win = Toplevel()
        self.win.wm_geometry('230x150')
        self.win.title(title)

        if host_server:
            Label(self.win, text=msg).grid(column=0, row=0, pady=8, padx=20)
            self.name_input = Entry(self.win)
            self.name_input.grid(column=1, row=0)
            text1 = Label(self.win, text='Amount of cards: ')
            text1.grid(column=0, row=1)
            self.card_amount_entry = Listbox(self.win, selectmode=EXTENDED, height=4)
            self.card_amount_entry.insert(1, '3x4')
            self.card_amount_entry.insert(2, '5x6')
            self.card_amount_entry.insert(3, '8x8')
            self.card_amount_entry.insert(4, '10x10')
            self.card_amount_entry.select_set(0)
            self.card_amount_entry.grid(column=1, row=1)
            Button(self.win, text=button_text, command=button_event).grid(columnspan=2, row=2, pady=14)
        else:
            Label(self.win, text=msg).grid(column=0, row=0, pady=8, padx=20)
            self.name_input = Entry(self.win)
            self.name_input.grid(column=1, row=0)
            Label(self.win, text='Server IP:').grid(column=0, row=1, pady=8)
            self.ip_input = Entry(self.win)
            self.ip_input.grid(column=1, row=1)
            Button(self.win, text=button_text, command=button_event).grid(columnspan=2, row=2, pady=14)
            # Button(self.win, text='Back', command=self.close_message_noinput).grid(column=1, row=2, pady=14)

    def close_message_server_host(self):
        self.name = self.name_input.get()
        self.card_amount = self.card_amount_entry.get(ACTIVE)
        print(self.card_amount_entry)
        self.win.destroy()
        self.thread_networking_server()

    def close_message(self):
        self.name = self.name_input.get()
        self.s_ip = self.ip_input.get()
        self.win.destroy()
        # self.thread_networking_client()
        self.find_server()

    def server_start_game(self):
        if self.name == '' or self.name == ' ':
            self.name == 'Player 1'
        if self.client_name == '' or self.client_name == ' ':
            self.client_name == 'Player 2'

        threading.Thread(target=self.thread_server_start_game).start()
        menu_root.destroy()

    def thread_server_start_game(self):
        self.game_gui = Memory_Game_Server_Game_Core.GUI(self.card_amount, self.game)
        self.player1 = Memory_Game_Server_Game_Core.Player(self.name, 1, self.game_gui, self.game)
        self.player2 = Memory_Game_Server_Game_Core.Player(self.client_name, 2, self.game_gui, self.game)
        self.game.network = self.network

        self.network.send([self.card_amount, self.name, self.client_name])
        new_dict = {}
        for key, card in self.game_gui.cards.items():
            new_dict[key] = [None, card[1], card[2]]

        self.network.send(new_dict)
        self.game.start_local_game()

    def thread_client_start_game(self):
        self.game_gui = Memory_Game_Server_Game_Core.GUI(self.card_amount, self.game, 'client')
        self.player1 = Memory_Game_Server_Game_Core.Player(self.name, 1, self.game_gui, self.game)
        self.player2 = Memory_Game_Server_Game_Core.Player(self.client_name, 2, self.game_gui, self.game)
        self.game.network = self.network

        cards = self.network.receive()
        self.game_gui.cards = cards
        self.game_gui.make_client_board()
        self.game.start_local_game()




main_menu = Mainmenu()
menu_root.mainloop()
