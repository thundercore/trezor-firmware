from trezor import utils

if utils.MODEL == "1":
    from trezor.ui.model.t1.confirm import Confirm
    from trezor.ui.model.t1.text import Text
elif utils.MODEL == "T":
    from trezor.ui.model.tt.button import ButtonCancel
    from trezor.ui.model.tt.confirm import HoldToConfirm
    from trezor.ui.model.tt.text import Text
    from trezor import ui
    from trezor.ui import loader
else:
    raise ValueError("Unknown Trezor model")


def common_layout(content: str):
    text = Text("Wipe device", ui.ICON_WIPE, ui.RED)
    text.normal(content)
    return Confirm(text, confirm="WIPE DEVICE", cancel="CANCEL")
