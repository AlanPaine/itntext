def str2bool(value):
    if isinstance(value, bool):
        return value
    return str(value).lower() in {"true", "1", "yes", "y"}
