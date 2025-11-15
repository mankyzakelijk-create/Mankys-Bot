# main.py
import threading
import os
from gui_server import start_gui
from bot_core import run_bot

if __name__ == '__main__':
    # Start GUI in aparte thread (Flask)
    gui_thread = threading.Thread(target=start_gui, daemon=True)
    gui_thread.start()

    # Start bot (blokkeert, dus start GUI eerst)
    run_bot()
