def is_int(n):
    try:
        int(n, 10)
        return True
    except ValueError:
        return False
