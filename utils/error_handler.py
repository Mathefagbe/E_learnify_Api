def error_handler(e):
    msg = ''
    if hasattr(e, 'detail'):
        if isinstance(e.detail, dict):
            for q,k in e.detail.items():
                if k[0].code=="required":
                    msg += f"{q}: {k[0]}"
                    break
                else:
                    msg += f"{k[0]}"
                    break
        elif isinstance(e.detail, list):
            for q in e.detail:
                msg += f"{q} "
                break
        else:
            msg = str(e.detail)
    elif hasattr(e, 'message'):
        if isinstance(e.message, dict):
            for q in e.message.items():
                msg += f"{q[0]}: {q[1][0]} "
                break
        elif isinstance(e.message, list):
            for q in e.message:
                msg += f"{q} "
                break
        elif isinstance(e.message, str):
            msg = e.message
        else:
            msg = str(e)
    else:
        msg = str(e)
    return msg
