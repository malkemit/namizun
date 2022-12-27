from threading import Thread
from namizun_menu.monitor import system_usage
from namizun_menu.main_menu import menu as main_menu

Thread(target=system_usage).start()
Thread(target=main_menu).start()
