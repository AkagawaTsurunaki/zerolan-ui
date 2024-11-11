import threading


def multithread(method):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=method, args=args, kwargs=kwargs, daemon=True)
        thread.start()
        return thread

    return wrapper
