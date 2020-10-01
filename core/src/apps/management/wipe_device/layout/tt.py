from trezor.ui.model.tt.button import ButtonCancel
from trezor.ui.model.tt.confirm import HoldToConfirm
from trezor.ui.model.tt.text import Text
from trezor import ui
from trezor.ui import loader


def confirm_wipe() -> HoldToConfirm:
    text = Text("Wipe device", ui.ICON_WIPE, ui.RED)
    text.normal("Do you really want to", "wipe the device?", "")
    text.bold("All data will be lost.")
    return HoldToConfirm(text, confirm_style=ButtonCancel, loader_style=loader.LoaderDanger)
