from zerolan.ui.api.toasts import ProgressToast


def test_info_progress_toast():
    ProgressToast(message="Information...",
                  level="info",
                  duration=5,
                  busy=True,
                  max_value=100,
                  cur_value=0).show_toast()

def test_warn_progress_toast():
    ProgressToast(message="Warning...",
                  level="warn",
                  duration=5,
                  busy=True,
                  max_value=100,
                  cur_value=0).show_toast()

def test_error_progress_toast():
    ProgressToast(message="Error...",
                  level="error",
                  duration=5,
                  busy=True,
                  max_value=100,
                  cur_value=0).show_toast()