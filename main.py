# Nicely recommend to use '<jd>' in Ctrl+F menu for better navigation

import os
import sys
import time
import keyboard
import string
import random
import secrets
import winreg
from cryptography.fernet import Fernet

from win32gui import GetWindowText, GetForegroundWindow

tm_arrows, tm_enter = 0, 0    # timers for keyreg latency
SW_LATENCY, INP_LATENCY = 0.175, 0.525

window_name = GetWindowText(GetForegroundWindow())  # setting up window name for focus checking

absolute_error, gen_error, add_error = '', '', ''

pass_settings = []
password = ''
saved = False

FILENAME = 'passwords.txt'

KEYVAL = r'SOFTWARE\pGen'  # using regedit to store decryption key <jd>
try:
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, KEYVAL, 0, winreg.KEY_ALL_ACCESS)
    try:
        fkey = bytes(winreg.QueryValueEx(key, 'Fernet Key')[0][2:-1], 'UTF-8')
        fernet = Fernet(fkey)
    except OSError:
        fkey = Fernet.generate_key()
        winreg.SetValueEx(key, 'Fernet Key', 0, winreg.REG_SZ, str(fkey))
        fernet = Fernet(fkey)
except OSError:
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, KEYVAL)
    fkey = Fernet.generate_key()
    winreg.SetValueEx(key, 'Fernet Key', 0, winreg.REG_SZ, str(fkey))
    fernet = Fernet(fkey)

debug_mode = False

headlines = [    # headlines start <jd>
    [
        '        _____            ',
        '       / ____|           ',
        ' _ __ | |  __  ___ _ __  ',
        '| \'_ \\| | |_ |/ _ \\ \'_ \\ ',
        '| |_) | |__| |  __/ | | |',
        '| .__/ \\_____|\\___|_| |_|',
        '| |                      ',
        '|_|                      '
    ],
    [
        '        _______              ',
        '.-----.|     __|.-----.-----.',
        '|  _  ||    |  ||  -__|     |',
        '|   __||_______||_____|__|__|',
        '|__|                         '
    ],
    [
        '         ________               ',
        '______  /  _____/  ____   ____  ',
        '\\____ \\/   \\  ____/ __ \\ /    \\ ',
        '|  |_> >    \\_\\  \\  ___/|   |  \\',
        '|   __/ \\______  /\\___  >___|  /',
        '|__|           \\/     \\/     \\/ '
    ],
    [
        '      ___         ___           ___           ___     ',
        '     /  /\\       /  /\\         /  /\\         /__/\\    ',
        '    /  /::\\     /  /:/_       /  /:/_        \\  \\:\\   ',
        '   /  /:/\\:\\   /  /:/ /\\     /  /:/ /\\        \\  \\:\\  ',
        '  /  /:/~/:/  /  /:/_/::\\   /  /:/ /:/_   _____\\__\\:\\ ',
        ' /__/:/ /:/  /__/:/__\\/\\:\\ /__/:/ /:/ /\\ /__/::::::::\\',
        ' \\  \\:\\/:/   \\  \\:\\ /~~/:/ \\  \\:\\/:/ /:/ \\  \\:\\~~\\~~\\/',
        '  \\  \\::/     \\  \\:\\  /:/   \\  \\::/ /:/   \\  \\:\\  ~~~ ',
        '   \\  \\:\\      \\  \\:\\/:/     \\  \\:\\/:/     \\  \\:\\     ',
        '    \\  \\:\\      \\  \\::/       \\  \\::/       \\  \\:\\    ',
        '     \\__\\/       \\__\\/         \\__\\/         \\__\\/   '
    ],
    [
        '       .oPYo.              ',
        '       8    8              ',
        '.oPYo. 8      .oPYo. odYo. ',
        '8    8 8   oo 8oooo8 8\' `8 ',
        '8    8 8    8 8.     8   8 ',
        '8YooP\' `YooP8 `Yooo\' 8   8 ',
        '8 ....::....8 :.....:..::..',
        '8 ::::::::::8 :::::::::::::',
        '..::::::::::..:::::::::::::'
    ],
    [
        '       ____                      ',
        '      /\\  _`\\                    ',
        ' _____\\ \\ \\L\\_\\     __    ___    ',
        '/\\ \'__`\\ \\ \\L_L   /\'__`\\/\' _ `\\  ',
        '\\ \\ \\L\\ \\ \\ \\/, \\/\\  __//\\ \\/\\ \\ ',
        ' \\ \\ ,__/\\ \\____/\\ \\____\\ \\_\\ \\_\\',
        '  \\ \\ \\/  \\/___/  \\/____/\\/_/\\/_/',
        '   \\ \\_\\                         ',
        '    \\/_/                         '
    ],
    [
        '         MM\'"""""`MM                   ',
        '         M\' .mmm. `M                   ',
        '88d888b. M  MMMMMMMM .d8888b. 88d888b. ',
        '88\'  `88 M  MMM   `M 88ooood8 88\'  `88 ',
        '88.  .88 M. `MMM\' .M 88.  ... 88    88 ',
        '88Y888P\' MM.     .MM `88888P\' dP    dP ',
        '88       MMMMMMMMMMM                   ',
        'dP                                     '
    ],
    [
        '     _____         ',
        ' ___|   __|___ ___ ',
        '| . |  |  | -_|   |',
        '|  _|_____|___|_|_|',
        '|_|                '
    ],
    [
        '             .oooooo.                          ',
        '            d8P\'  `Y8b                         ',
        'oo.ooooo.  888            .ooooo.  ooo. .oo.   ',
        ' 888\' `88b 888           d88\' `88b `888P"Y88b  ',
        ' 888   888 888     ooooo 888ooo888  888   888  ',
        ' 888   888 `88.    .88\'  888    .o  888   888  ',
        ' 888bod8P\'  `Y8bood8P\'   `Y8bod8P\' o888o o888o ',
        ' 888                                           ',
        'o888o                                          '
    ],
    [
        '    dMMMMb  .aMMMMP dMMMMMP dMMMMb ',
        '   dMP.dMP dMP"    dMP     dMP dMP ',
        '  dMMMMP" dMP MMP"dMMMP   dMP dMP  ',
        ' dMP     dMP.dMP dMP     dMP dMP   ',
        'dMP      VMMMP" dMMMMMP dMP dMP    '
    ],
    [
        '           ______         ',
        '    ____  / ____/__  ____ ',
        '   / __ \\/ / __/ _ \\/ __ \\',
        '  / /_/ / /_/ /  __/ / / /',
        ' / .___/\\____/\\___/_/ /_/ ',
        '/_/                       '
    ],
    [
        '        ____            ',
        ' _ __  / ___| ___ _ __  ',
        '| \'_ \\| |  _ / _ \\ \'_ \\ ',
        '| |_) | |_| |  __/ | | |',
        '| .__/ \\____|\\___|_| |_|',
        '|_|                     '
    ],
    [
        '      o-o           ',
        '     o              ',
        'o-o  |  -o o-o o-o  ',
        '|  | o   | |-\' |  | ',
        'O-o   o-o  o-o o  o ',
        '|                   ',
        'o                   '
    ],
    [
        '   dBBBBBb  dBBBBb  dBBBP  dBBBBb',
        '       dB\'                    dBP',
        '   dBBBP\' dBBBB   dBBP   dBP dBP ',
        '  dBP    dB\' BB  dBP    dBP dBP  ',
        ' dBP    dBBBBBB dBBBBP dBP dBP   '
    ],
    [
        ' ______  ______   ______   __   __    ',
        '/\\  == \\/\\  ___\\ /\\  ___\\ /\\ "-.\\ \\   ',
        '\\ \\  _-/\\ \\ \\__ \\\\ \\  __\\ \\ \\ \\-.  \\  ',
        ' \\ \\_\\   \\ \\_____\\\\ \\_____\\\\ \\_\\\\"\\_\\ ',
        '  \\/_/    \\/_____/ \\/_____/ \\/_/ \\/_/ '
    ],
    [
        '██████╗  ██████╗ ███████╗███╗   ██╗',
        '██╔══██╗██╔════╝ ██╔════╝████╗  ██║',
        '██████╔╝██║  ███╗█████╗  ██╔██╗ ██║',
        '██╔═══╝ ██║   ██║██╔══╝  ██║╚██╗██║',
        '██║     ╚██████╔╝███████╗██║ ╚████║',
        '╚═╝      ╚═════╝ ╚══════╝╚═╝  ╚═══╝'
    ],
    [
        ' ▄▄▄· ▄▄ • ▄▄▄ . ▐ ▄ ',
        '▐█ ▄█▐█ ▀ ▪▀▄.▀·•█▌▐█',
        ' ██▀·▄█ ▀█▄▐▀▀▪▄▐█▐▐▌',
        '▐█▪·•▐█▄▪▐█▐█▄▄▌██▐█▌',
        '.▀   ·▀▀▀▀  ▀▀▀ ▀▀ █▪'
    ],
    [
        '      :::::::::   ::::::::  :::::::::: ::::    :::',
        '     :+:    :+: :+:    :+: :+:        :+:+:   :+: ',
        '    +:+    +:+ +:+        +:+        :+:+:+  +:+  ',
        '   +#++:++#+  :#:        +#++:++#   +#+ +:+ +#+   ',
        '  +#+        +#+   +#+# +#+        +#+  +#+#+#    ',
        ' #+#        #+#    #+# #+#        #+#   #+#+#     ',
        '###         ########  ########## ###    ####      '
    ],
    [
        '      8""""8           ',
        'eeeee 8    " eeee eeeee',
        '8   8 8e     8    8   8',
        '8eee8 88  ee 8eee 8e  8',
        '88    88   8 88   88  8',
        '88    88eee8 88ee 88  8'
    ],
    [
        ' ____    ___   ____ __  __',
        ' || \\\\  // \\\\ ||    ||\\ ||',
        ' ||_// (( ___ ||==  ||\\\\||',
        ' ||     \\\\_|| ||___ || \\||'
    ],
    [
        '@@@@@@@   @@@@@@@  @@@@@@@@ @@@  @@@',
        '@@!  @@@ !@@       @@!      @@!@!@@@',
        '@!@@!@!  !@! @!@!@ @!!!:!   @!@@!!@!',
        '!!:      :!!   !!: !!:      !!:  !!!',
        ' :        :: :: :  : :: ::  ::    : '
    ],
    [
        '-----------  ------------ ------------ ----    ----',
        '************ ************ ************ *****   ****',
        '---      --- ----         ----         ------  ----',
        '************ ****  ****** ************ ************',
        '-----------  ----  ------ ------------ ------------',
        '****         ****    **** ****         ****  ******',
        '----         ------------ ------------ ----   -----',
        '****         ************ ************ ****    ****'
    ],
    [
        'P G E N',
        'G E N P',
        'E N P G',
        'N P G E'
    ]
]    # headlines end <jd>

header = random.choices(headlines)[0]


def print_header():
    print('\n'.join(str(o) for o in header))
    print()


trying_to_del = 0    # dont touch it pls
tried_to_del = False
delet = False
iii = 0


def scan_passwords():
    try:
        with open(FILENAME, 'r') as file:
            return not 1 > len(file.readlines())
    except FileNotFoundError:
        with open(FILENAME, 'w') as file:
            file.write('{0}\n'.format(fernet.encrypt('F1r5Tp455W0rD_y0y'.encode())))
    finally:
        with open(FILENAME, 'r') as file:
            return not 1 > len(file.readlines())


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')    # also works properly on linux


def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import termios    # for linux/unix
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)


def about_section():
    about = ('Author: SyberiaK\n',    # i dont think thats fine
             'For any issues contact me:',
             'Discord: SyberiaK.#0396',
             'Twitter: @syberiakey\n',
             'Version: 0.5.1 beta',
             'What\'s new:',
             '- Fixed resetting decryption key process',
             '- Various code optimizations')
    print(*about, '', sep='\n')


mainMenu = ['Generate the password', 'Show saved passwords', 'Settings', 'About\n', 'Exit']    # menus <jd>
showSaved = ['Add my own password', 'Delete all saved passwords', 'Exit to main menu']    # yep, these're lists xd
settingsMenu = ['Debug mode: off', 'Reset decryption key\n', 'Exit to main menu']
passSettingsMenu = ['Use letters (a-z)', 'Use numbers (0-9)', 'Use characters (e.g. "!", "#", "\\")', 'Continue']
passwordMenu = ['Save this password', 'Generate new password', 'Exit to main menu']
aboutMenu = ['Exit to main menu']    # why


def menu(m: list):    # this little fella do all the hard work <jd>
    global tm_arrows, tm_enter, SW_LATENCY, absolute_error, saved,\
        debug_mode, trying_to_del, tried_to_del, delet, iii
    pos, _pos = 0, 0

    def print_list():
        global absolute_error, tried_to_del
        clear_console()
        print_header()
        if absolute_error == 'You must select any setting.':    # TODO: maybe do some fine errors output?
            print(f'ERROR! {absolute_error}')
            absolute_error = ''
        if m == passSettingsMenu:
            print('Choose the settings:\n')
        elif m == passwordMenu:
            print(f'Your generated password: {password}\n')
            if saved:
                if m[0] == 'Save this password':
                    m.remove('Save this password')
                print('Saved!')
            else:
                m.insert(0, 'Save this password') if m[0] != 'Save this password' else None
        elif m == showSaved:
            print('Saved passwords:')
            if scan_passwords():
                with open(FILENAME, 'r') as saved_pass_file:
                    for line in saved_pass_file.readlines():    # scanning saved passwords
                        print(str(fernet.decrypt(eval(line[:-1])).decode()))
            else:
                print('There are no saved passwords.')
            print()
        elif m == aboutMenu:
            about_section()
        for i, v in enumerate(m):    # rendering menu <jd>
            print(f'> {v}' if i == pos else v)
        if debug_mode:
            print(f'\nDebug:\n{pos}')
            if m == passSettingsMenu:
                print(pass_settings)
            if m == passwordMenu:
                print(passwordMenu)
            print(time.time(), tm_arrows, tm_enter, sep='\n')

    print_list()

    while True:
        current_window = GetWindowText(GetForegroundWindow())

        if current_window == window_name:
            if pos != _pos:
                print_list()
                _pos = pos

            if keyboard.is_pressed('Up') and time.time() - tm_arrows > SW_LATENCY:
                pos = max(0, pos - 1)
                tm_arrows = time.time()
            elif keyboard.is_pressed('Down') and time.time() - tm_arrows > SW_LATENCY:
                pos = min(len(m) - 1, pos + 1)
                tm_arrows = time.time()
            elif keyboard.is_pressed('Enter') and time.time() - tm_enter > INP_LATENCY:
                if m == mainMenu:    # main menu do <jd>
                    tm_enter = time.time()
                    if pos == 0:
                        return gen_password()
                    elif pos == 1:
                        return menu(showSaved)
                    elif pos == 2:
                        return menu(settingsMenu)
                    elif pos == 3:
                        return menu(aboutMenu)
                    elif pos == 4:
                        clear_console()
                        flush_input()
                        sys.exit()
                elif m == settingsMenu:    # settings menu do <jd>
                    tm_enter = time.time()
                    if pos == 0:
                        if debug_mode:
                            debug_mode = False
                            settingsMenu[0] = 'Debug mode: off'
                        else:
                            debug_mode = True
                            settingsMenu[0] = 'Debug mode: on'
                        print_list()
                    elif pos == 1:
                        return decryption_key_reset()
                    elif pos == 2:
                        return menu(mainMenu)
                elif m == showSaved:    # showsaved menu do <jd>
                    tm_enter = time.time()
                    if pos == 0:
                        if not delet:
                            m[0] = 'Add my own password'
                            trying_to_del = 0
                            return add_pass()
                        else:
                            m[0] = 'NAH. YOU ARE STAYING HERE TILL U WON\'T DELETE THIS PASSWORD'   # IGNORE
                            print_list()
                    elif pos == 1:
                        if scan_passwords():
                            trying_to_del = 0
                            return wipe_pass()
                        else:
                            if tried_to_del:
                                m[1] = 'There are no passwords to delete.'
                            else:
                                if trying_to_del < 2:   # ignore this code
                                    m[1] = 'There are no saved passwords!'
                                elif 1 < trying_to_del < 4:
                                    m[1] = 'There are still no saved passwords.'
                                elif trying_to_del == 5:
                                    m[1] = 'There are no passwords to delete.'
                                elif trying_to_del == 6:
                                    m[1] = 'Please stop doing it.'
                                elif trying_to_del == 7:
                                    m[1] = 'Seriosly, stop.'
                                elif trying_to_del == 8:
                                    m[1] = 'Thats not funny at all, stop.'
                                elif trying_to_del == 9:
                                    m[1] = 'JUST. STOP.'
                                elif trying_to_del == 10:
                                    m[1] = 'THERE. IS. NOTHING. TO. DELETE.'
                                elif trying_to_del == 11:
                                    m[1] = 'YOU WANT TO DELETE SOMETHING? OK, FINE'
                                    print_list()
                                    time.sleep(1)
                                    m[1] = 'THERE! THERE\'S A PASSWORD FOR YOU!'
                                    with open(FILENAME, 'w') as file:
                                        file.write(str(fernet.encrypt('5CR3W_U_1D!0t'.encode())) + '\n')
                                    print_list()
                                    delet = True    # ignore this code

                            print_list()
                            if not delet:
                                trying_to_del += 1
                                time.sleep(1)
                                m[1] = 'Delete all saved passwords'
                                print_list()
                    elif pos == 2:
                        if not delet:
                            m[2] = 'Exit to main menu'
                            trying_to_del = 0
                            return menu(mainMenu)
                        else:
                            m[2] = 'NAH. YOU ARE STAYING HERE TILL U WON\'T DELETE THIS PASSWORD'    # IGNORE
                            print_list()
                elif m == passSettingsMenu:   # generator settings menu do <jd>
                    tm_enter = time.time()    # actual piece of shit
                    if pos == 0:
                        if 'l' not in pass_settings:
                            passSettingsMenu[0] = '+ ' + passSettingsMenu[0]
                            passSettingsMenu.insert(1, ' Use capital letters (A-Z)')
                            pass_settings.append('l')
                        else:
                            passSettingsMenu[0] = passSettingsMenu[0].split('+ ')[1]
                            del passSettingsMenu[1]
                            pass_settings.remove('l')
                            if '^' in pass_settings:
                                pass_settings.remove('^')
                    elif pos == 1:
                        if 'l' in pass_settings:
                            if '^' not in pass_settings:
                                passSettingsMenu[1] = ' +' + passSettingsMenu[1]
                                pass_settings.append('^')
                            else:
                                passSettingsMenu[1] = passSettingsMenu[1].split(' +')[1]
                                pass_settings.remove('^')
                        else:
                            if 'n' not in pass_settings:
                                passSettingsMenu[1] = '+ ' + passSettingsMenu[1]
                                pass_settings.append('n')
                            else:
                                passSettingsMenu[1] = passSettingsMenu[1].split('+ ')[1]
                                pass_settings.remove('n')
                    elif pos == 2:
                        if 'l' in pass_settings:
                            if 'n' not in pass_settings:
                                passSettingsMenu[2] = '+ ' + passSettingsMenu[2]
                                pass_settings.append('n')
                            else:
                                passSettingsMenu[2] = passSettingsMenu[2].split('+ ')[1]
                                pass_settings.remove('n')
                        else:
                            if 's' not in pass_settings:
                                passSettingsMenu[2] = '+ ' + passSettingsMenu[2]
                                pass_settings.append('s')
                            else:
                                passSettingsMenu[2] = passSettingsMenu[2].split('+ ')[1]
                                pass_settings.remove('s')
                    elif pos == 3:
                        if 'l' in pass_settings:
                            if 's' not in pass_settings:
                                passSettingsMenu[3] = '+ ' + passSettingsMenu[3]
                                pass_settings.append('s')
                            else:
                                passSettingsMenu[3] = passSettingsMenu[3].split('+ ')[1]
                                pass_settings.remove('s')
                        else:
                            if pass_settings:
                                return pass_settings
                            else:
                                absolute_error = 'You must select any setting.'
                    elif pos == 4:
                        if 'l' in pass_settings:
                            if pass_settings:
                                return pass_settings
                            else:
                                absolute_error = 'You must select any setting.'
                    print_list()
                elif m == passwordMenu:    # generated password menu do <jd>
                    tm_enter = time.time()
                    if pos == 0:
                        if saved:
                            time.sleep(INP_LATENCY)
                            return gen_password()
                        else:
                            saved = True
                            with open(FILENAME, 'a') as add_pass_file:
                                add_pass_file.write(str(fernet.encrypt(password.encode())) + '\n')
                            print_list()
                    elif pos == 1:
                        if saved:
                            return menu(mainMenu)
                        else:
                            time.sleep(INP_LATENCY)
                            return gen_password()
                    elif pos == 2:
                        return menu(mainMenu)
                elif m == aboutMenu:    # about section do <jd>
                    tm_enter = time.time()
                    return menu(mainMenu)


def gen_password():    # generating password <jd>
    global password, saved, tm_enter, gen_error
    using = ''
    rnd = secrets.SystemRandom()

    saved = False

    clear_console()
    print_header()
    flush_input()
    if gen_error != '':
        print(f'ERROR! {gen_error}')
    print('Enter the password length (1-100) (or enter "noisia" to cancel): ', end='')
    time.sleep(INP_LATENCY)
    length = input()
    if length == 'noisia':
        clear_console()
        print_header()
        print('Canceled.')
        gen_error = ''
        time.sleep(1)
        return menu(mainMenu)
    if not length.strip() or not length.isnumeric() or not (1 < int(length) < 100):
        if not length.strip():    # exceptions
            gen_error = 'Password length cannot be blank.'
        elif not length.isnumeric():
            gen_error = 'Password length must contain only numbers.'
        elif int(length) < 1:
            gen_error = 'Password length is too small.'
        elif int(length) > 100:
            gen_error = 'Password length is too big.'
        else:
            gen_error = 'Unknown error. Please report to the author.'
        return gen_password()
    tm_enter = time.time()
    gen_error = ''
    _settings = menu(passSettingsMenu)
    using += string.ascii_lowercase if 'l' in _settings else ''   # taking needed symbols
    using += string.ascii_uppercase if '^' in _settings else ''
    using += string.digits if 'n' in _settings else ''
    using += string.punctuation if 's' in _settings else ''
    password = ''.join(rnd.choice(using) for _ in range(int(length)))    # pass generator in one string <jd>
    return menu(passwordMenu)


def add_pass():    # adding your own password <jd>
    global tm_enter, add_error

    clear_console()
    print_header()
    flush_input()

    if add_error != '':
        print(f'ERROR! {add_error}')
    print('Enter your password (or enter "nur haken" to cancel): ', end='')
    time.sleep(INP_LATENCY)
    adding_password = input()
    if adding_password == 'nur haken':
        clear_console()
        print_header()
        print('Canceled.')
        add_error = ''
        time.sleep(1)
        return menu(showSaved)
    if not adding_password.strip() or len(adding_password) > 100 or ' ' in adding_password:    # exceptions
        if not adding_password.strip():
            add_error = 'Password cannot be blank.'
        elif len(adding_password) > 100:
            add_error = 'This password is too big.'
        elif ' ' in adding_password:
            add_error = 'Password cannot contain spaces.'
        else:
            add_error = 'Unknown error. Please report to the author.'
        return add_pass()
    tm_enter = time.time()
    add_error = ''
    with open(FILENAME, 'a') as add_pass_file:
        add_pass_file.write(f'{fernet.encrypt(adding_password.encode())}\n')
    clear_console()
    print_header()
    print(f'The password "{adding_password}" was successfully added!')
    time.sleep(1)
    return menu(showSaved)


def wipe_pass():    # wiping passlist <jd>
    global delet, tried_to_del, showSaved
    clear_console()    # TODO: create a menu where you can select what passwords you want to delete
    flush_input()
    print('All these passwords will be deleted:')
    with open(FILENAME, 'r') as saved_pass_file:
        for line in saved_pass_file.readlines():
            print(str(fernet.decrypt(eval(line[:-1])).decode()))
    print()
    print('Please, enter "pGen is dope" if you sure (or something else to cancel): ', end='')
    time.sleep(INP_LATENCY)
    des = input()
    if des == 'pGen is dope' or delet:
        if delet:
            showSaved = ['Delete all saved passwords', 'Exit to main menu']
        delet = False
        tried_to_del = True
        clear_console()
        flush_input()
        with open(FILENAME, 'w') as file:
            file.write('')
        print('Done!')
        time.sleep(1)
        return menu(showSaved)
    clear_console()
    flush_input()
    print('Canceled.')
    time.sleep(1)
    return menu(showSaved)


def decryption_key_reset():   # resetting decryption key <jd>
    global fkey, fernet       # this thing will delete all your saved passwords

    clear_console()           # (or else this program will be broken)
    print_header()
    flush_input()
    print('CAUTION!\nBy resetting the decryption key you will lost all of your saved passwords.')
    print('If you are being pressured by someone to do this '
          'just because he/she wants that - please leave this step.')
    print('Anyway, please, enter "This Is The Greatest Plan" if you really '
          'need to reset the key (or something else to cancel): ', end='')
    time.sleep(INP_LATENCY)
    des = input()
    if des == 'This Is The Greatest Plan':
        clear_console()
        flush_input()
        with open(FILENAME, 'w') as file:
            file.write('')
        fkey = Fernet.generate_key()
        winreg.SetValueEx(key, 'Fernet Key', 0, winreg.REG_SZ, str(fkey))
        fernet = Fernet(fkey)
        print('Done!')
        time.sleep(1)
        return menu(settingsMenu)
    clear_console()
    flush_input()
    print('Canceled.')
    time.sleep(1)
    return menu(settingsMenu)


if __name__ == '__main__':    # launch <jd>
    menu(mainMenu)

# recommeded command for building project (windows build):
# pyinstaller -F --clean -n "pGen" -i "key.ico" --version-file "file_version_info.txt" main.py
# also there is no support for linux/unix yet (because of winreg and win32gui), sorry about that
