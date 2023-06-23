from typing import Optional

from telegram.ext import Updater, Dispatcher, InlineQueryHandler, CallbackContext, CallbackQueryHandler
from telegram.update import Update
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup

updater = Updater(token='6152418030:AAGk1Sba3R7Tk7fLo4pzyEkFvqbmSW-pZ7g')

dispatcher: Dispatcher = updater.dispatcher


class Game:
    def __init__(self, context: CallbackContext):
        self._context = context
        self._chat_data = context.chat_data
        self._chat_data.update({
            'games_increment': 1
        })

    def _get_next_game_id(self):
        _id = self._chat_data['games_increment']
        self._chat_data.update({
            'games_increment': _id + 1
        })
        return _id

    def store_data(self):
        self._chat_data.update({
            self.game_name: self.game
        })

    def new_game(self):
        self.game_name = 'game' + str(self._get_next_game_id())
        self.game = {
            'player1': None,
            'player2': None,
            'game': [0, 0, 0, 0, 0, 0, 0, 0, 0],
            'turn': False,
        }
        self.store_data()

    def get_name(self, name):
        self.game = self._chat_data.get(name, None)


def generate_keyboards(game: Optional[Game], is_new_game=False):
    NONE = '⬜'
    CROSS = '❌'
    CIRCLE = '⭕'

    keyboard = []

    for i in range(3):
        temp_keyboard = []
        for j in range(3):
            index = i * 3 + j
            item = game[index]
            text = NONE if item == 0 else CROSS if item == 1 else CIRCLE
            temp_keyboard.append(
                InlineKeyboardButton(text=text, callback_data=f'{game.game_name}{index}')
            )
            # if item == 0:
            #   temp_keyboard.append(InlineKeyboardButton(text=NONE, callback_data=f'{game.game_name}{index}'))
            # elif item == 1:
            #    temp_keyboard.append(InlineKeyboardButton(text=CROSS, callback_data=f'{game.game_name}{index}'))
            ## elif item == 2:
            #  temp_keyboard.append(InlineKeyboardButton(text=CIRCLE, callback_data=f'{game.game_name}{index}'))

            keyboard.append(temp_keyboard)

    return keyboard


# return [
#  [
#     InlineKeyboardButton(text='⬜', callback_data='0'),
#     InlineKeyboardButton(text='⬜', callback_data='1'),
#   InlineKeyboardButton(text='⬜', callback_data='2'),
# ],

# [
#   InlineKeyboardButton(text='⬜', callback_data='3'),
#    InlineKeyboardButton(text='⬜', callback_data='4'),
#  InlineKeyboardButton(text='⬜', callback_data='5'),
# ],

# [
#    InlineKeyboardButton(text='⬜', callback_data='6'),
#   InlineKeyboardButton(text='⬜', callback_data='7'),
#   InlineKeyboardButton(text='⬜', callback_data='8'),
# ],
# ]
#

def inline_query(update: Update, context: CallbackContext) -> None:
    query = update.inline_query.query
    # query.answer()
    keyboard = generate_keyboards(None, is_new_game=True)
    update.inline_query.answer([
        InlineQueryResultArticle(id="x", title="x",
                                 input_message_content=InputTextMessageContent('x'),
                                 reply_markup=InlineKeyboardMarkup(keyboard)),

        InlineQueryResultArticle(id="0", title="0",
                                 input_message_content=InputTextMessageContent('0'),
                                 reply_markup=InlineKeyboardMarkup(keyboard)
                                 ),
    ])


def callback_query(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    game = Game(context)
    if query.data == 'new_game':
        game.new_game()
        query.edit_message_text(text=f"Selection option", reply_markup=InlineKeyboardMarkup(generate_keyboards(game)))
    else:
        game_name, index = query.data.split('|')
        game.get_name(game_name)
        query.edit_message_text(text=f"Selection option", reply_markup=InlineKeyboardMarkup(generate_keyboards(game)))
    # index = int(query.data)
    # game = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    # game[index] = 1
    # query.edit_message_text(text=f"Selection option", reply_markup=InlineKeyboardMarkup(generate_keyboards(game)))

    print(query)


dispatcher.add_handler(InlineQueryHandler(inline_query))
dispatcher.add_handler(CallbackQueryHandler(callback_query))
updater.start_polling()
updater.idle()
