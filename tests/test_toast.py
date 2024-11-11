from zerolan.ui.api.toasts import Toast


def test_info_toast():
    Toast("Information!", "info", duration=5).show_toast()

def test_warn_toast():
    Toast("Warning!", "warn", duration=5).show_toast()

def test_error_toast():
    Toast("Error!", "error", duration=5).show_toast()