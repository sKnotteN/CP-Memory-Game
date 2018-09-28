"""
Author: Kristian Saure Knotten
Student ID: 8284
E-mail: ksknotten@outlook.com
"""

# Hent dei andre python scripta
import Memory_Game_Core_v2
import Memory_Game_Networking as Networking

# Importer offisielle libs
from tkinter import *
from tkinter import messagebox
import threading


# Lag ein root vindauge for houvd menyen
menu_root = Tk()
menu_root.title('Main Menu')
menu_root.geometry('400x450')
menu_root.resizable(width=False, height=False)


# Ein klasse for main menu som er hovud menyen der du velger og setter alle innstillinger. Bestemmer over lokalt spel
class Mainmenu:
    def __init__(self):
        # Set variablar som ein enkelt kan endre på igjennom heile classen
        self.game = Memory_Game_Core_v2.Game()
        self.game_gui = None
        self.network_menu = None
        self.name1, self.name2, self.card_amount = '', '', ''
        self.name1_entry, self.name2_entry, self.card_amount_entry = None, None, None

        # Lag frames som skal innehalde forskjellig informasjon. f_user_input skal vere til player input
        self.f_information = Frame(menu_root)
        self.f_information.pack(fill=BOTH, expand=True, side=TOP)
        self.f_user_input = Frame(menu_root)
        self.f_user_input.pack(side=TOP)
        self.img = PhotoImage(file='Game_pic.png')
        self.game_title_frame, self.game_info_frame = self.information_frame()



        # Start og lag vindauget
        self.user_input_frame()

    # Setter inn informasjonen som skal vere i informasjons framen, Informasjon om spelet og titel på spelet
    def information_frame(self):
        title = Label(self.f_information, image=self.img)
        title.pack(pady=(0, 25))
        info = Label(self.f_information, text='This is a memory game\n The player with the most points wins the game')
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
            local.grid(column=0, row=0, pady=(0, 10))
            network = Button(self.f_user_input, text='Network play', command=self.network_play)
            network.grid(column=0, row=1, pady=(0, 86))
            b_quit = Button(self.f_user_input, text='Quit Game', command=quit)
            b_quit.grid(row=2, pady=(0, 20))

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
        b_quit.grid(columnspan=2, row=4, pady=(20, 20))

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

    # Send all infoen som er hentet inn til game scriptet (Memory_Game_Core_v2) og sett i eit lokalt spel
    def send_info(self):
        self.game_gui = Memory_Game_Core_v2.GUI(self.card_amount, self.game, self.img)
        self.player1 = Memory_Game_Core_v2.Player(self.name1, 1, self.game_gui, self.game)
        self.player2 = Memory_Game_Core_v2.Player(self.name2, 2, self.game_gui, self.game)

        # Fjern main menu vindauget
        menu_root.destroy()

    # Lager eit vindauge som har ein beskjed samt ein quit knapp
    def message(self, msg, title):
        win = Toplevel()
        win.wm_geometry('250x100')
        win.resizable(width=False, height=False)
        win.title(title)
        Label(win, text=msg).pack(pady=8)
        Button(win, text='Quit', command=quit).pack(side=BOTTOM, pady=14)


# Ein netverk klass til ein nettverk meny. Arver Mainmenu klassa.
class NetworkMenu(Mainmenu):
    # Input er mainmenu klassa og game klassa frå Memory_Game_Core_v2
    def __init__(self, main_menu, game):
        # Lag variablar igjen for og enkelt få tilgang til dei i heile klassa
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
        self.network_lobby = False

        self.f_server_user_input = self.main_menu.f_user_input
        self.create_server_input_widgets(self.f_server_user_input)

    # Lag til input til brukaren der han kan velge mellom å gå tilbake, host ein game eller finne ein game.
    def create_server_input_widgets(self, frame):
        b_play = Button(frame, text='Host game', command=self.waiting_for_client)
        b_play.grid(column=0, row=0)
        b_find = Button(frame, text='Find game', command=self.server_info)
        b_find.grid(column=0, row=1, pady=(10, 50))

        b_back = Button(frame, text='Back', command=self.back_b)
        b_back.grid(column=0, row=2, pady=(0, 10))
        b_quit = Button(frame, text='Quit Game', command=quit)
        b_quit.grid(column=0, row=3, pady=(0, 20))

    # Når back blir trykt; clear framen og lag til mainmenu framen. Prøv og close sockets som er oppe.
    def back_b(self):
        if self.network_lobby:
            self.clear_frame(self.f_server_user_input)
            self.create_server_input_widgets(self.f_server_user_input)
            self.network_lobby = False
        else:
            self.clear_frame(self.f_server_user_input)
            # self.f_server_user_input.place_forget()
            self.main_menu.user_input_frame()
        try:
            self.network.close
        except AttributeError:
            pass

    # Når find game blir trykt; Vindauge der klienten skriv inn namnet og server ip. Lager og ein connect knapp.
    def server_info(self):
        self.message2('Name: ', 'Your name', self.close_message, 'Connect')

    # Når host game blir trykt; Vindauge for og velge mengden kort og namn. Lager og ein host og quit knapp.
    def waiting_for_client(self):
        self.message2('Name:', 'Host a server', self.close_message_server_host, 'Start server', True)

    # Lager ein ny tråd som blir brukt til og lage serveren slik menyen ikkje frys
    def thread_networking_server(self):
        threading.Thread(target=self.host_game).start()

    # def thread_networking_client(self):
    #     threading.Thread(target=self.find_server).start()

    # Setter opp ein socket og venter på at nokon kopler til.
    def host_game(self):
        self.player1, self.player2 = None, None
        self.network = Networking.Server('127.0.0.1', 5000)
        if self.network.look() == 'Connected':
            # Når nåken kopler til sjekk kva namnet til klienten er
            data = self.network.receive()
            if data.startswith('name:'):
                data, name = data.split(' ')
                # Send bekreftelse til klienten
                self.network.send('Connected')
                # Sett namnet til klienten i ein variabel og start eit nettverks spel
                self.client_name = name
                self.server_start_game()

    # Lager til ein socket og prøver og kople seg til ein server, om det ikkje går gi beskjed
    def find_server(self):
        self.network = Networking.Client(self.s_ip, 5000)
        # Set informasjonen om serveren
        self.network.look()
        # Send det valgte namnet
        self.network.send('name: ' + str(self.name))
        # Vent på bekreftelse frå serveren
        answer = self.network.receive()
        if answer == 'No server found':
            messagebox.showinfo('No server found', 'Was not able to find a server')
        elif answer == 'Connected':
            # Vent på informasjon frå serveren
            answer2 = self.network.receive()
            # Lagre den informasjonen som serveren sendte som er namn til player 1 og 2 og mendgen kort
            self.card_amount, self.name, self.client_name = answer2[0], answer2[1], answer2[2]

            # Start ein ny tråd for og lage klienten sin versjon av spelet
            threading.Thread(target=self.thread_client_start_game).start()
            # Fjern så hovud menyen
            menu_root.destroy()

    # Lager 2 forskjellige vindauger som skal kome opp når brukaren trykk på ein av knappane host game eller find game
    def message2(self, msg, title, button_event, button_text, host_server=False):
        # Clear input framen
        self.main_menu.clear_frame(self.f_server_user_input)
        # to only go back to network lobby (with the host game and find game options)
        self.network_lobby = True

        # Om host game blir trykt; legg til i input frame der ein får velge mengden kort og namn.
        if host_server:
            l_name = Label(self.f_server_user_input, text='Player name: ')
            l_name.grid(column=0, row=0)
            name = Entry(self.f_server_user_input)
            name.grid(pady=5, padx=15, column=1, row=0)

            text1 = Label(self.f_server_user_input, text='Amount of cards: ')
            text1.grid(column=0, row=1)
            entry = Listbox(self.f_server_user_input, selectmode=EXTENDED, height=4)
            entry.insert(1, '3x4')
            entry.insert(2, '5x6')
            entry.insert(3, '8x8')
            entry.insert(4, '10x10')
            entry.select_set(0)
            entry.grid(column=1, row=1)

            b_back = Button(self.f_server_user_input, text='Back', command=self.back_b)
            b_back.grid(column=0, row=2, pady=(20, 20))
            b_play = Button(self.f_server_user_input, text=button_text, command=button_event)
            b_play.grid(column=1, row=2)

            b_quit = Button(self.f_server_user_input, text='Quit Game', command=quit)
            b_quit.grid(columnspan=2, row=3, pady=(20, 20))

            self.card_amount_entry = entry
            self.name_input = name

        # Om find game blir trykt: lag eit vindu der ein får skrive inn namn og server ip. Får og submit knapp
        else:
            l_name = Label(self.f_server_user_input, text='Player name: ')
            l_name.grid(column=0, row=0)
            name = Entry(self.f_server_user_input)
            name.grid(padx=15, column=1, row=0)
            l_ip = Label(self.f_server_user_input, text='Server IP: ')
            l_ip.grid(column=0, row=1, pady=(10, 20))
            ip = Entry(self.f_server_user_input)
            ip.grid(padx=15, column=1, row=1, pady=(10, 20))

            b_back = Button(self.f_server_user_input, text='Back', command=self.back_b)
            b_back.grid(column=0, row=2, pady=20)
            b_play = Button(self.f_server_user_input, text=button_text, command=button_event)
            b_play.grid(column=1, row=2)

            b_quit = Button(self.f_server_user_input, text='Quit Game', command=quit)
            b_quit.grid(columnspan=2, row=3, pady=(20, 20))

            self.name_input = name
            self.ip_input = ip

    # Når ein trykker på host game i det nye vindauget: hent informasjonen, fjern vindauget og start ein ny tråd
    def close_message_server_host(self):
        self.name = self.name_input.get()
        self.card_amount = self.card_amount_entry.get(ACTIVE)
        # self.win.destroy()
        # Start ein tråd og prøv og finne ein klient
        self.thread_networking_server()

    # Når ein trykker på find game i det nye vindauget: hent informasjon, fjern vindauget, prøv og kople til ein server.
    def close_message(self):
        self.name = self.name_input.get()
        self.s_ip = self.ip_input.get()
        # self.win.destroy()
        # self.thread_networking_client()
        # Prøv og kople til ein server
        self.find_server()

    # Start eit nettverks spel. Sjekk om namna er sett, om ikkje sett dei til default (player 1 og player 2)
    def server_start_game(self):
        if self.name == '' or self.name == ' ':
            self.name == 'Player 1'
        if self.client_name == '' or self.client_name == ' ':
            self.client_name == 'Player 2'

        # Start ein tråd for det nye spelet
        threading.Thread(target=self.thread_server_start_game).start()
        # Fjern hovud menyen
        menu_root.destroy()

    # Send over variabler som trengst i spelet og send nødvendig informasjon til klienten
    def thread_server_start_game(self):
        self.game_gui = Memory_Game_Core_v2.GUI(self.card_amount, self.game, self.img)
        self.player1 = Memory_Game_Core_v2.Player(self.name, 1, self.game_gui, self.game)
        self.player2 = Memory_Game_Core_v2.Player(self.client_name, 2, self.game_gui, self.game)
        self.game.network = self.network

        # Send mengden kort og namnet på speler 1 og 2 til klienten.
        self.network.send([self.card_amount, self.name, self.client_name])

        # Lag ein ny dict utan tkinter objekt i da disse objekta ikkje er mulig og sende med pickle som blir brukt
        new_dict = {}
        for key, card in self.game_gui.cards.items():
            # Fjern tkinter objektet og legg til ein midlertidig erstattning
            new_dict[key] = [None, card[1], card[2]]

        # Send den nye dictinary til klienten og start opp spelet
        self.network.send(new_dict)
        self.game.start_local_game()

    # Send dei nødvendige variablane over til spelet og motta korta(og deira rekkefølge) som blei laget på serveren
    def thread_client_start_game(self):
        self.game_gui = Memory_Game_Core_v2.GUI(self.card_amount, self.game, self.img, 'client')
        self.player1 = Memory_Game_Core_v2.Player(self.name, 1, self.game_gui, self.game)
        self.player2 = Memory_Game_Core_v2.Player(self.client_name, 2, self.game_gui, self.game)
        self.game.network = self.network

        # Lagre den lista(new_dict) som blei sendt frå server, send så dette til spelet og start spelet
        cards = self.network.receive()
        self.game_gui.cards = cards
        self.game_gui.make_client_board()
        self.game.start_local_game()


# Lagre Mainmenu klassen i ein variabel for og initialisere klassa. Opne så vindauget
main_menu = Mainmenu()

menu_root.mainloop()
