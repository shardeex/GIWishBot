from aiogram import html, types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.utils.i18n.core import I18n

from app import genshin
from app.schema import Player
from app.loader import i18n, assets_path
from app.modules import profile
from app.states import profile as states

state = states.ShowcaseEdit.character.state

_ = i18n.gettext

async def query(
    query: types.InlineQuery,
    i18n: I18n,
    state: FSMContext,
    player: Player
    ):
    query_offset = int(query.offset) if query.offset else 0

    def condition(character: genshin.Character) -> bool:
        return character.category == 'characters' and \
            character.get_name(i18n.current_locale).lower().startswith(query.query.lower())

    char_inv = profile.showcase.load.player_items(player, i18n.current_locale, query_offset, condition=condition)

    if char_inv is None:
        results = [
            types.InlineQueryResultArticle(
                title=_('No free characters! :('),
                id=0, description=profile.message.showcase.no_characters.get(),
                thumb_url=None,
                input_message_content=types.InputTextMessageContent(
                    message_text=profile.message.showcase.player_answer_no_characters.get()))
        ]
        await query.answer(results, is_personal=True, cache_time=0)
        return

    results = [
        types.InlineQueryResultArticle(
            title=char.name_with_constellation(i18n.current_locale, player.inventory[char.id]) + ' ' + char.stars,
            id=char.id, description=char.get_desc(i18n.current_locale),
            thumb_url=f'{assets_path}/images/icons/{char.id}.png',
            input_message_content=types.InputTextMessageContent(message_text=f'#{char.id}')
        ) for char in char_inv]

    next_offset = "" if len(results) < 50 else str(query_offset+50)
    await query.answer(results, is_personal=True, cache_time=0, next_offset=next_offset)
