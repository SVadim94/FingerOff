def join_columns(columns):
    res = "\n".join(str(_) for _ in columns)

    return res if res else "No results"


def transfers_to_str(transfers):
    return '\n'.join("/transfer %s %s %s" % (s, d, str(a)) for s, d, a in transfers)
