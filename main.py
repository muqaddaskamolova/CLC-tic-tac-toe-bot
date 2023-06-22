from telegram.ext import Updater, Dispatcher, InlineQueryHandler, CallbackContext, CallbackQueryHandler
from telegram.update import Update
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup

updater = Updater(token='6152418030:AAGk1Sba3R7Tk7fLo4pzyEkFvqbmSW-pZ7g')

dispatcher: Dispatcher = updater.dispatcher


def generate_keyboards(game: list):
    NONE = '⬜'
    CROSS = '❌'
    CIRCLE = '⭕'

    keyboard = []

    for i in range(3):
        temp_keyboard = []
        for j in range(3):
            index = i * 3 + j
            item = game[index]
            if item == 0:
                temp_keyboard.append(InlineKeyboardButton(text=NONE, callback_data=index))
            elif item == 1:
                temp_keyboard.append(InlineKeyboardButton(text=CROSS, callback_data=index))
            elif item == 2:
                temp_keyboard.append(InlineKeyboardButton(text=CIRCLE, callback_data=index))

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
    keyboard = generate_keyboards([0, 0, 0, 0, 0, 2, 0, 1, 0])
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
    index = int(query.data)
    game = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    game[index] = 1
    query.edit_message_text(text=f"Selection option", reply_markup=InlineKeyboardMarkup(generate_keyboards(game)))


dispatcher.add_handler(InlineQueryHandler(inline_query))
dispatcher.add_handler(CallbackQueryHandler(callback_query))
updater.start_polling()
updater.idle()
