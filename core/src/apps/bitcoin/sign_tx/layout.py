from micropython import const
from ubinascii import hexlify

from trezor.messages import OutputScriptType
from trezor.strings import format_amount
from trezor.ui import widgets
from trezor.ui.widgets import require

from .. import addresses
from . import omni

if False:
    from trezor import wire
    from trezor.messages.TxOutput import TxOutput

    from apps.common.coininfo import CoinInfo

_LOCKTIME_TIMESTAMP_MIN_VALUE = const(500000000)


def format_coin_amount(amount: int, coin: CoinInfo) -> str:
    return "%s %s" % (format_amount(amount, coin.decimals), coin.coin_shortcut)


async def confirm_output(ctx: wire.Context, output: TxOutput, coin: CoinInfo) -> None:
    if output.script_type == OutputScriptType.PAYTOOPRETURN:
        data = output.op_return_data
        assert data is not None
        if omni.is_valid(data):
            # OMNI transaction
            title = "OMNI transaction"
            await require(widgets.confirm_output(ctx, title, data=omni.parse(data)))
        else:
            # generic OP_RETURN
            hex_data = hexlify(data).decode()
            await require(widgets.confirm_output(ctx, "OP_RETURN", hex_data=hex_data))
    else:
        address = output.address
        assert address is not None
        address_short = addresses.address_short(coin, address)
        await require(
            widgets.confirm_output(
                ctx,
                "Confirm sending",
                address=address_short,
                amount=format_coin_amount(output.amount, coin),
            )
        )


async def confirm_joint_total(
    ctx: wire.Context, spending: int, total: int, coin: CoinInfo
) -> None:
    await require(
        widgets.confirm_joint_total(
            ctx,
            spending_amount=format_coin_amount(spending, coin),
            total_amount=format_coin_amount(total, coin),
        ),
    )


async def confirm_total(
    ctx: wire.Context, spending: int, fee: int, coin: CoinInfo
) -> None:
    await require(
        widgets.confirm_total(
            ctx,
            total_amount=format_coin_amount(spending, coin),
            fee_amount=format_coin_amount(fee, coin),
        ),
    )


async def confirm_feeoverthreshold(ctx: wire.Context, fee: int, coin: CoinInfo) -> None:
    await require(
        widgets.confirm_feeoverthreshold(ctx, fee_amount=format_coin_amount(fee, coin))
    )


async def confirm_change_count_over_threshold(
    ctx: wire.Context, change_count: int
) -> None:
    await require(
        widgets.confirm_change_count_over_threshold(ctx, change_count=change_count)
    )


async def confirm_nondefault_locktime(
    ctx: wire.Context, lock_time: int, lock_time_disabled: bool
) -> None:
    if int(lock_time) < _LOCKTIME_TIMESTAMP_MIN_VALUE:
        await require(
            widgets.confirm_nondefault_locktime(
                ctx,
                lock_time_disabled=lock_time_disabled,
                lock_time_height=lock_time,
            ),
        )
    else:
        await require(
            widgets.confirm_nondefault_locktime(
                ctx,
                lock_time_disabled=lock_time_disabled,
                lock_time_stamp=lock_time,
            ),
        )
