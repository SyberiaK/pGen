import os
import sys
import time
import keyboard
import random
import winreg
from cryptography.fernet import Fernet

tm_arrows = 0
tm_enter = 0
SW_LATENCY = 0.175

absolute_error = ''

pass_settings = []
password = ''
saved = False

FILENAME = 'passwords.txt'

KEYVAL = r'SOFTWARE\pGen'
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

headlines = [
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
        '      8""""8           '
        'eeeee 8    " eeee eeeee'
        '8   8 8e     8    8   8'
        '8eee8 88  ee 8eee 8e  8'
        '88    88   8 88   88  8'
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
        'P G E N'
        ''
        'G E N P'
        ''
        'E N P G'
        ''
        'N P G E'
    ]
]
header = headlines[random.randint(0, len(headlines) - 1)]

trying_to_del = 0
tried_to_del = False
delet = False
iii = 0


def print_header():
    for header_line in header:
        print(header_line)
    print()


def scan_passwords():
    try:
        with open(FILENAME, 'r') as file:
            p = file.readlines()
            if len(p) < 1:
                return False
            else:
                return True
    except FileNotFoundError:
        with open(FILENAME, 'w') as file:
            file.write(str(fernet.encrypt('F1r5Tp455W0rD_y0y'.encode())) + '\n')
    finally:
        with open(FILENAME, 'r') as file:
            p = file.readlines()
            if len(p) < 1:
                return False
            else:
                return True


def clear_console():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys
        import termios    # for linux/unix
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)


def about_section():
    about = ['Author: SyberiaK',
             '',
             'For any issues contact me:',
             'Discord: SyberiaK.#0396',
             'Twitter: @syberiakey',
             '',
             'Version: 0.3 beta',
             'What\'s new:',
             '- Hidden decryption key! Now no one can steal your password file and encrypt it\n  (at least not that easily)',
             '- BUT if someone somehow found your decryption key - you can always reset it in settings menu',
             '  (at the cost of all your saved passwords)',
             '- Also added a bunch more ascii headers']
    for o in about:
        print(o)
    print()


mainMenu = ['Generate the password', 'Show saved passwords', 'Settings', 'About', '', 'Exit']
showSaved = ['Add my own password', 'Delete all saved passwords', 'Exit to main menu']
settingsMenu = ['Debug mode: off', 'Reset decryption key', '', 'Exit to main menu']
passSettingsMenu = ['Use letters (a-z)', 'Use numbers (0-9)', 'Use characters (e.g. "!", "#", "\\")', 'Continue']
passwordMenu = ['Save this password', 'Generate new password', 'Exit to main menu']
aboutMenu = ['Exit to main menu']


def menu(m: list):
    global tm_arrows, tm_enter, SW_LATENCY, absolute_error, saved,\
        debug_mode, trying_to_del, tried_to_del, delet, iii
    pos, _pos = 0, 0

    def print_list():
        global absolute_error, tried_to_del
        clear_console()
        print_header()
        if absolute_error == 'You must select any setting.':
            print('ERROR!', absolute_error)
            absolute_error = ''
        if m == passSettingsMenu:
            print('Choose the settings:\n')
        elif m == passwordMenu:
            print('Your generated password:', password, '\n')
            if saved:
                if m[0] == 'Save this password':
                    m.remove('Save this password')
                print('Saved!')
            else:
                if m[0] != 'Save this password':
                    m.insert(0, 'Save this password')
        elif m == showSaved:
            print('Saved passwords:')
            if not scan_passwords():
                print('There are no saved passwords.')
            else:
                with open(FILENAME, 'r') as saved_pass_file:
                    sp = saved_pass_file.readlines()
                    for line in sp:
                        print(str(fernet.decrypt(eval(line[:-1])).decode()))
            print()
        elif m == aboutMenu:
            about_section()
        for i, v in enumerate(m):
            if i == pos:
                print(">", v)
            else:
                print(v)
        if debug_mode:
            print('\nDebug:\n' + str(pos))
            if m == passSettingsMenu:
                print(pass_settings)
            if m == passwordMenu:
                print(passwordMenu)
            else:
                print(time.time(), tm_arrows, tm_enter, sep='\n')

    print_list()

    while True:
        if pos != _pos:
            print_list()
            _pos = pos

        if keyboard.is_pressed('Up'):
            if time.time() - tm_arrows > SW_LATENCY:
                if pos > 0:
                    pos -= 1
                    if m[pos] == '':
                        pos -= 1
                tm_arrows = time.time()
        elif keyboard.is_pressed('Down'):
            if time.time() - tm_arrows > SW_LATENCY:
                if pos < len(m) - 1:
                    pos += 1
                    if m[pos] == '':
                        pos += 1
                tm_arrows = time.time()
        elif keyboard.is_pressed('Enter'):
            if time.time() - tm_enter > SW_LATENCY * 3:
                if m == mainMenu:
                    tm_enter = time.time()
                    if pos == 0:
                        return gen_password()
                    elif pos == 1:
                        return menu(showSaved)
                    elif pos == 2:
                        return menu(settingsMenu)
                    elif pos == 3:
                        return menu(aboutMenu)
                    elif pos == 5:
                        clear_console()
                        flush_input()
                        sys.exit()
                elif m == settingsMenu:
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
                    elif pos == 3:
                        return menu(mainMenu)
                elif m == showSaved:
                    tm_enter = time.time()
                    if pos == 0:
                        if not delet:
                            m[0] = 'Add my own password'
                            trying_to_del = 0
                            return add_pass()
                        else:
                            m[0] = 'NAH. YOU ARE STAYING HERE TILL U WON\'T DELETE THIS PASSWORD'
                            print_list()
                    elif pos == 1:
                        if not scan_passwords():
                            if not tried_to_del:
                                if trying_to_del < 2:
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
                                    delet = True
                            else:
                                m[1] = 'There are no passwords to delete.'
                            print_list()
                            if not delet:
                                trying_to_del += 1
                                time.sleep(1)
                                m[1] = 'Delete all saved passwords'
                                print_list()
                        else:
                            trying_to_del = 0
                            return wipe_pass()
                    elif pos == 2:
                        if not delet:
                            m[2] = 'Exit to main menu'
                            trying_to_del = 0
                            return menu(mainMenu)
                        else:
                            m[2] = 'NAH. YOU ARE STAYING HERE TILL U WON\'T DELETE THIS PASSWORD'
                            print_list()
                elif m == passSettingsMenu:
                    tm_enter = time.time()
                    if pos == 0:
                        if 'l' not in pass_settings:
                            passSettingsMenu[0] = '+ ' + passSettingsMenu[0]
                            passSettingsMenu.insert(1, ' Use capital letters (A-Z)')
                            pass_settings.append('l')
                        else:
                            passSettingsMenu[0] = passSettingsMenu[0].split('+ ')[1]
                            if ' Use capital letters (A-Z)' in passSettingsMenu or ' + Use capital letters (A-Z)':
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
                elif m == passwordMenu:
                    tm_enter = time.time()
                    if pos == 0:
                        if not saved:
                            saved = True
                            with open(FILENAME, 'a') as add_pass_file:
                                add_pass_file.write(str(fernet.encrypt(password.encode())) + '\n')
                            print_list()
                        else:
                            time.sleep(SW_LATENCY * 3)
                            return gen_password()
                    elif pos == 1:
                        if not saved:
                            time.sleep(SW_LATENCY * 3)
                            return gen_password()
                        else:
                            return menu(mainMenu)
                    elif pos == 2:
                        if not saved:
                            return menu(mainMenu)
                elif m == aboutMenu:
                    tm_enter = time.time()
                    if pos == 0:
                        return menu(mainMenu)


def gen_password():
    global password, saved, tm_enter
    letters = 'qwertyuiopasdfghjklzxcvbnm'
    numbers = '1234567890'
    symbols = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    using = ''

    saved = False

    clear_console()
    print_header()
    flush_input()
    print('Enter the password length (1-100) (or enter "noisia" to cancel): ', end='')
    time.sleep(SW_LATENCY * 3)
    length = input()
    if length == 'noisia':
        clear_console()
        print_header()
        print('Canceled.')
        time.sleep(1)
        return menu(mainMenu)
    while length == ' ' * len(length) or length == '' or not length.isnumeric() or int(length) < 1 or int(length) > 100:
        clear_console()
        print_header()
        if length == ' ' * len(length) or length == '':
            gen_error = '"Password length" cannot be blank.'
        elif not length.isnumeric():
            gen_error = '"Password length" must contain only numbers.'
        elif int(length) < 1:
            gen_error = '"Password length" is too small.'
        elif int(length) > 100:
            gen_error = '"Password length" is too big.'
        else:
            gen_error = 'Unknown error.'
        if gen_error != '':
            print('ERROR!', gen_error)
        flush_input()
        print('Enter the password length (1-100) (or enter "noisia" to cancel): ', end='')
        time.sleep(SW_LATENCY * 3)
        length = input()
        if length == 'noisia':
            clear_console()
            print_header()
            print('Canceled.')
            time.sleep(1)
            return menu(mainMenu)
    tm_enter = time.time()
    _settings = menu(passSettingsMenu)
    if 'l' in _settings:
        using += letters
        if '^' in _settings:
            using += letters.upper()
    if 'n' in _settings:
        using += numbers
    if 's' in _settings:
        using += symbols
    password = ''.join(random.choice(using) for _ in range(int(length)))
    return menu(passwordMenu)


def add_pass():
    global tm_enter

    clear_console()
    print_header()
    flush_input()
    print('Enter your password (or enter "nur haken" to cancel): ', end='')
    time.sleep(SW_LATENCY * 3)
    adding_password = input()
    if adding_password == 'nur haken':
        clear_console()
        print_header()
        print('Canceled.')
        time.sleep(1)
        return menu(showSaved)
    while adding_password == ' ' * len(adding_password) or adding_password == '' or len(adding_password) < 1 or len(
            adding_password) > 100 or ' ' in adding_password:
        clear_console()
        print_header()
        if adding_password == ' ' * len(adding_password) or adding_password == '':
            gen_error = 'Password cannot be blank.'
        elif len(adding_password) < 1:
            gen_error = 'This password is too small.'
        elif len(adding_password) > 100:
            gen_error = 'This password is too big.'
        elif ' ' in adding_password:
            gen_error = 'Password cannot contain spaces.'
        else:
            gen_error = 'Unknown error. Please report to the author.'
        if gen_error != '':
            print('ERROR!', gen_error)
        flush_input()
        print('Enter your password (or enter "nur haken" to cancel): ', end='')
        time.sleep(SW_LATENCY * 3)
        adding_password = input()
        if adding_password == 'nur haken':
            clear_console()
            print_header()
            print('Canceled.')
            time.sleep(1)
            return menu(showSaved)
    tm_enter = time.time()
    with open(FILENAME, 'a') as add_pass_file:
        add_pass_file.write(str(fernet.encrypt(adding_password.encode())) + '\n')
    clear_console()
    print_header()
    print('The password "{passtr}" was successfully added!'.format(passtr=adding_password))
    time.sleep(1)
    return menu(showSaved)


def wipe_pass():
    global delet, tried_to_del, showSaved
    clear_console()
    flush_input()
    print('All these passwords will be deleted:')
    with open(FILENAME, 'r') as saved_pass_file:
        sp = saved_pass_file.readlines()
        for line in sp:
            print(str(fernet.decrypt(eval(line[:-1])).decode()))
    print()
    print('Please, enter "pGen is dope" if you sure (or something else to cancel): ', end='')
    time.sleep(SW_LATENCY * 3)
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
    else:
        clear_console()
        flush_input()
        print('Canceled.')
        time.sleep(1)
        return menu(showSaved)


def decryption_key_reset():
    clear_console()
    print_header()
    flush_input()
    print('CAUTION!\nBy resetting the decryption key you will lost all of your saved passwords.')
    print('If you are being pressured by someone to do this '
          'just because he/she wants that - please leave this step.')
    print('Anyway, please, enter "This Is The Greatest Plan" if you really need to reset the key (or something else to cancel): ', end='')
    time.sleep(SW_LATENCY * 3)
    des = input()
    if des == 'This Is The Greatest Plan':
        clear_console()
        flush_input()
        with open(FILENAME, 'w') as file:
            file.write('')
        print('Done!')
        time.sleep(1)
        return menu(settingsMenu)
    else:
        clear_console()
        flush_input()
        print('Canceled.')
        time.sleep(1)
        return menu(settingsMenu)


if __name__ == '__main__':
    menu(mainMenu)

# C:\Users\SyberiaK\PycharmProjects\pGen
# pyinstaller -F --clean -n "pGen" -i "key.ico" --version-file "file_version_info.txt" main.py
