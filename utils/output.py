def join_columns(columns):
    res = "\n".join(str(_) for _ in columns)

    return res if res else "No results"
