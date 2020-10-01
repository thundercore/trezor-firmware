from trezor.ui.model.t1.confirm import Confirm
from trezor.ui.model.t1.text import Text


def confirm_wipe() -> Confirm:
    text = Text(new_lines=False)
    text.bold("Do you want to wipe")
    text.br()
    text.bold("the device?")
    text.br()
    text.br_half()
    text.normal("All data will be lost.")
    return Confirm(text, confirm="WIPE DEVICE", cancel="CANCEL")
