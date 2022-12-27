from os import system
from colored import fg
from pyfiglet import Figlet

cornsilk_color = fg("cornsilk_1")
cyan_color = fg("cyan")
gold_color = fg("gold_1")
green_color = fg("green")
magenta_color = fg("magenta")
red_color = fg("light_red")
reset_color = fg("white")
yellow_color = fg("yellow")


def clear_terminal():
    system('clear')


def line_remover(lines):
    for i in range(lines):
        print('\033[1A', end='\x1b[2K')


def line_jumper(lines):
    if lines < 0:
        print(f'\033[{-1 * lines}A')
    else:
        print(f'\033[{lines}B')


def banner():
    custom_fig = Figlet(font='poison')
    clear_terminal()
    print(f"{gold_color}{custom_fig.renderText('NAMIZUN')}{reset_color}")
