import Constants
# Данный файл отвечает за сообщения от handler_command


def responser(input_text):
    user_message = str(input_text).lower()

    if user_message == Constants.main_keyboard[1][1].lower():
        return [Constants.greeting, 1, 1]
    if user_message == Constants.main_keyboard[0][0].lower():
        return ['Введите то, что вам надо напомнить', 0, 0, 'main']
    if user_message == Constants.main_keyboard[0][1].lower():
        return ['Вот всё что я должен вам напомнить:', 0, 1, 'main']
    if user_message == Constants.main_keyboard[1][0].lower():
        return ['Ваш список дел:', 1, 0, 'main']

    if user_message == Constants.options_keyboard[0][0].lower():
        return['Напишите номер напоминания', 0, 'options']
    if user_message == Constants.options_keyboard[1][0].lower():
        return['Возвращаю...', 1, 0, 'options']

    if user_message == Constants.to_do_list_keyboard[0][0].lower():
        return ['Напишите то, что я должен добавить в список', 0, 0, 'to do list']
    if user_message == Constants.to_do_list_keyboard[0][1].lower():
        return ['Напишите номер дела', 0, 1, 'to do list']
    if user_message == Constants.to_do_list_keyboard[1][0].lower():
        return ['Возвращаю...', 1, 0, 'to do list']

    return ['Простите, я не понимаю.', -1, -1]
