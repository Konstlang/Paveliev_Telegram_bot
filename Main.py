from telegram.ext import *
import Constants as const
import Responses
from telegram import ReplyKeyboardMarkup
import time

print('Bot started...')


def start(update, context):  # стартовое сообщение
    markup = ReplyKeyboardMarkup(const.main_keyboard, one_time_keyboard=False)  # главная клавиатура
    update.message.reply_text(
        const.greeting,
        reply_markup=markup
    )


def first_reminder_response(update, context):  # Запоминание текста напоминания и вызов следующего вопроса
    context.user_data['reminders'].append(update.message.text)
    update.message.reply_text("В какое время вам напомнить? Напишите в виде \"(день)/(месяц)/(год) (час):(минута)\" или"
                              " просто \"(час):(минута)\" в зависимости от того, когда вы хотите получить напоминание.")
    return 12


def second_reminder_response(update, context):
    # Ответ на второй вопрос
    context.user_data['time of reminders'].append(update.message.text)
    update.message.reply_text("Хорошо я вам обязательно напомню!")
    chat_id = update.message.chat_id
    # Создаём таймер который будет отслеживать время напоминания
    context.job_queue.run_repeating(
        task,
        1,
        context={'user_data': context.user_data, 'chat_data': context.chat_data, 'chat_id': chat_id},
        name=str(chat_id)
    )
    return ConversationHandler.END  # Константа, означающая конец диалога.


def first_option_response(update, context):  # Переход в настройки напоминалки
    text = str(update.message.text).lower()
    response = Responses.responser(text)
    if const.options_keyboard[response[1]][0] == const.options_keyboard[0][0]:  # Удалить напоминание
        update.message.reply_text(response[0])
        return 22
    elif const.options_keyboard[response[1]][0] == const.options_keyboard[1][0]:  # Назад
        markup = ReplyKeyboardMarkup(const.main_keyboard, one_time_keyboard=False)
        update.message.reply_text(
            response[0],
            reply_markup=markup
        )
        return ConversationHandler.END


def second_option_response(update, context):  # Удаление напоминания
    number_of_reminder = int(update.message.text) - 1
    context.user_data['reminders'].pop(number_of_reminder)
    context.user_data['time of reminders'].pop(number_of_reminder)
    markup = ReplyKeyboardMarkup(const.main_keyboard, one_time_keyboard=False)
    update.message.reply_text(
        'Напоминание удалено',
        reply_markup=markup
    )
    return ConversationHandler.END


def first_to_do_list_response(update, context):  # Вызов меню списка дел
    text = str(update.message.text).lower()
    response = Responses.responser(text)
    if const.to_do_list_keyboard[response[1]][response[2]] == const.to_do_list_keyboard[0][0]:  # Добавить дело
        update.message.reply_text(
            response[0])
        return 32
    elif const.to_do_list_keyboard[response[1]][response[2]] == const.to_do_list_keyboard[0][1]:  # Удалить дело
        update.message.reply_text(
            response[0])
        return 33
    elif const.to_do_list_keyboard[response[1]][response[2]] == const.to_do_list_keyboard[1][0]:  # Назад
        markup = ReplyKeyboardMarkup(const.main_keyboard, one_time_keyboard=False)
        update.message.reply_text(
            response[0],
            reply_markup=markup
        )
        return ConversationHandler.END


def add_to_do_list_response(update, context):  # Добавление дела в список
    text = str(update.message.text)
    context.user_data['to do list'].append(text)
    update.message.reply_text('Дело добавлено в список\nВаш список дел:')
    markup = ReplyKeyboardMarkup(const.to_do_list_keyboard, one_time_keyboard=False)
    ans = []
    if context.user_data['to do list']:
        for i, j in enumerate(context.user_data['to do list']):
            ans.append(str(i + 1) + ') ' + j)
        update.message.reply_text('\n'.join(ans),
                                  reply_markup=markup)
        return 31
    else:
        update.message.reply_text('У вас их нет ;)', reply_markup=markup)
        return 31


def delete_to_do_list_response(update, context):  # Удаление из списка дел
    number_of_doing = int(update.message.text) - 1
    context.user_data['to do list'].pop(number_of_doing)
    markup = ReplyKeyboardMarkup(const.to_do_list_keyboard, one_time_keyboard=False)
    update.message.reply_text('Дело удалено\nВаш список дел:')
    ans = []
    if context.user_data['to do list']:
        for i, j in enumerate(context.user_data['to do list']):
            ans.append(str(i + 1) + ') ' + j)
        update.message.reply_text('\n'.join(ans),
                                  reply_markup=markup)
        return 31
    else:
        update.message.reply_text('У вас их нет ;)', reply_markup=markup)
        return 31


def handle_command(update, context):  # Данная функция принимает комманды с главной клавиатуры и является ядром системы
    if 'reminders' not in context.user_data.keys():
        context.user_data['reminders'] = []
        context.user_data['time of reminders'] = []
    if 'to do list' not in context.user_data.keys():
        context.user_data['to do list'] = []
    text = str(update.message.text).lower()
    ans = []
    response = Responses.responser(text)
    update.message.reply_text(response[0])
    if const.main_keyboard[response[1]][response[2]] == const.main_keyboard[0][0]:
        return 11
    elif const.main_keyboard[response[1]][response[2]] == const.main_keyboard[0][1]:
        if context.user_data['reminders']:
            markup = ReplyKeyboardMarkup(const.options_keyboard, one_time_keyboard=True)
            for i, j in enumerate(context.user_data['time of reminders']):
                ans.append(str(i + 1) + ') ' + j + ' - ' + context.user_data['reminders'][i])
            update.message.reply_text('\n'.join(ans),
                                      reply_markup=markup)
            return 21
        else:
            update.message.reply_text('У вас их нет ;)')
    elif const.main_keyboard[response[1]][response[2]] == const.main_keyboard[1][0]:
        markup = ReplyKeyboardMarkup(const.to_do_list_keyboard, one_time_keyboard=False)
        if context.user_data['to do list']:
            for i, j in enumerate(context.user_data['to do list']):
                ans.append(str(i + 1) + ') ' + j)
            update.message.reply_text('\n'.join(ans),
                                      reply_markup=markup)
            return 31
        else:
            update.message.reply_text('У вас их нет ;)', reply_markup=markup)
            return 31


def task(context):  # Функция, ответственная за напоминание в намеченое время
    context_of_job = context.job.context
    if 'reminders' not in context_of_job['user_data'].keys():
        context_of_job['user_data']['reminders'] = []
        context_of_job['user_data']['time of reminders'] = []

    for n, i in enumerate(context_of_job['user_data']['time of reminders']):
        separator = i.split()
        used_format = '%d/%m/%Y, %H:%M'
        try:
            if len(separator) == 1:
                time_of_response = time.strptime(
                    f'{time.localtime()[2]}/{time.localtime()[1]}/{time.localtime()[0]}, {separator[0]}', used_format)
            else:
                time_of_response = time.strptime(
                    f'{separator[0]}, {separator[1]}', used_format)
            if time_of_response[:5] == time.localtime()[:5]:
                context.bot.send_message(context_of_job['chat_id'], text=context_of_job['user_data']['reminders'][n])
                context_of_job['user_data']['reminders'].pop(n)
                context_of_job['user_data']['time of reminders'].pop(n)
        except Exception as e:
            context_of_job['user_data']['reminders'].pop(n)
            context_of_job['user_data']['time of reminders'].pop(n)
            context.bot.send_message(context_of_job['chat_id'], text='Вы неправильно оформили напоминание, и оно было'
                                                                     ' удалено. Пожалуйста, следуйте инструкциям!')
            print(e)
            break


def error(update, context):  # Возникает при появлении ошибки
    print(f'Update {update} caused error {context.error}')


def main():
    updater = Updater(const.BOT_KEY, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    reminder_handler = ConversationHandler(
        # Точка входа в диалог.
        entry_points=[MessageHandler(Filters.text, handle_command, pass_user_data=True)],
        # Состояние внутри диалога.
        states={
            # Напоминалка
            11: [MessageHandler(Filters.text, first_reminder_response, pass_user_data=True)],
            12: [MessageHandler(Filters.text, second_reminder_response, pass_user_data=True,
                                pass_job_queue=True,
                                pass_chat_data=True)],
            # Настройка напоминалки
            21: [MessageHandler(Filters.text, first_option_response, pass_user_data=True)],
            22: [MessageHandler(Filters.text, second_option_response, pass_user_data=True)],
            # Список дел
            31: [MessageHandler(Filters.text, first_to_do_list_response, pass_user_data=True)],
            32: [MessageHandler(Filters.text, add_to_do_list_response, pass_user_data=True)],
            33: [MessageHandler(Filters.text, delete_to_do_list_response, pass_user_data=True)]
        },
        # Точка прерывания диалога особо не используется
        fallbacks=[CommandHandler('stop', error)]
    )
    dp.add_handler(reminder_handler)
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


main()
