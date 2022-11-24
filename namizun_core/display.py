from os import system
from colored import fg
from pyfiglet import Figlet

cornsilk = fg("cornsilk_1")
cyan = fg("cyan")
gold = fg("gold_1")
green = fg("green")
magenta = fg("magenta")
red = fg("light_red")
reset = fg("white")
yellow = fg("yellow")


def clear():
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
    clear()
    print(f"{gold}{custom_fig.renderText('NAMIZUN')}{reset}")


def description():
    print(f"\n {gold}--------------{magenta}Description{gold}-------------\n\n{cornsilk}"
          f"This project is used to remove the limitation of asymmetric ratio\n"
          f"for uploading and downloading Iranian servers\n\n"
          f"{gold}Developed by {green}Mal{reset}Ke{red}Mit{cornsilk}")
