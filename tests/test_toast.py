from zerolan.ui.api.toasts import Toast


def test_info_toast():
    Toast("Test for showing toast!", "info", duration=5).show_toast()
