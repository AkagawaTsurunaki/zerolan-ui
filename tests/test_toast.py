from multiprocessing import Process
import time

from zerolan.ui.api.toasts import Toast
from zerolan.ui.app import start_ui_application

def test_info_toast():
    # p = Process(target=start_ui_application)
    # p.start()
    time.sleep(5)
    Toast("Test for showing toast!", "info", duration=5).show_toast()
    time.sleep(5)
    # p.kill()
