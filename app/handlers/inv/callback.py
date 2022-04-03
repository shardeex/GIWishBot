from aiogram import types
from aiogram.utils.i18n.core import I18n

from app.modules import inv
from app.schema import Player

from app import keyboards
from app.keyboards.inline.inv.category import Category


async def call(
    query: types.CallbackQuery,
    i18n: I18n,
    player: Player,
    callback_data: Category
    ) -> dict[str, bool]:
    '''_summary_

    :param types.CallbackQuery query: _description_
    :param I18n i18n: _description_
    :param Player player: _description_
    :param Category callback_data: _description_
    :return dict[str, bool]: _description_
    '''
    category = callback_data.category
    username = query.from_user.full_name

    items = inv.load.items_by_rarity(player.inventory, category=category)
    names = inv.load.names_by_rarity(
        i18n.current_locale, items=items, extra_number=True)
    numbers = inv.load.numbers_by_rarity(items=items)
    text = inv.message.get(player, username, names, numbers, category)

    await query.message.edit_text(
        text, reply_markup=keyboards.inline.inv.category.get(exclude=category))
    await query.answer()

    return {'save_player': False}
