from trezor import utils


def confirm_wipe():
    # TODO: handle btn req
    if utils.MODEL == "1":
        from .t1 import confirm_wipe
    elif utils.MODEL == "T":
        from .tt import confirm_wipe  # type: ignore
    else:
        raise ValueError("Unknown Trezor model")
    confirm_wipe()
