def is_int(n):
    try:
        int(n, 10)
        return True
    except ValueError:
        return False

def join_columns(columns):
    res = "\n".join(str(_) for _ in columns)
    
    return res if res else "No results"
