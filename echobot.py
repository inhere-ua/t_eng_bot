def prepare_data():
    """
	Данные, которые у нас имеются в начале работы:
	1. Список пользователей нашего бота
	"""
    users = [
        {
            "user_id": 777,
            "username": "Freg",
            "user_level": 2},
        {
            "user_id": 383,
            "username": "Oleg",
            "user_level": 1},
        {
            "user_id": 918,
            "username": "Anna",
            "user_level": 3}
    ]

    # 2. Набор предложений
    sentences = [
        {"text": "When my time comes \n Forget the wrong that I’ve done.",
         "level": 1},
        {"text": "In a hole in the ground there lived a hobbit.",
         "level": 2},
        {
            "text": "The sky the port was the color of television, tuned to a dead channel.",
            "level": 1},
        {"text": "I love the smell of napalm in the morning.",
         "level": 0},
        {
            "text": "The man in black fled across the desert, and the gunslinger followed.",
            "level": 0},
        {"text": "The Consul watched as Kassad raised the death wand.",
         "level": 1},
        {"text": "If you want to make enemies, try to change something.",
         "level": 2},
        {
            "text": "We're not gonna take it. \n Oh no, we ain't gonna take it \nWe're not gonna take it anymore",
            "level": 1},
        {
            "text": "I learned very early the difference between knowing the name of something and knowing something.",
            "level": 2}
    ]
    return users, sentences


def userrequest():
    # 3. Сообщение с сервера, где указано от юзера с каким ID прилетел запрос и какое слово он ищет
    req_from_server = {"user_id": 777, "text": "change"}

    return req_from_server


""" 
Здесь ваш код. 
Используйте наработки предущей практической и последних занятий, чтоб завернуть его в функции

На выходе мы должны получить словарь вида
{user_id: 123, text: "blah-blah-blah \n ... \n anothe blah-blah-blah"}, 
где:
text - это одна большая строка, в которой содержаться английские предложения (либо сообщение, что результат не найден)
user_id - это id юзера, от которого нам прилетело сообщение, и на который мы же отправляем ответ
"""


# Результирующее сообщение должно готовиться функций типа prepare_message (название можете выбрать сами)
def prepare_message(user: dict = None, sentence: dict = None,
                    request: dict = None):
    userlevel = None
    msg = {"user_id": request["user_id"], "text": []}

    # get user level by user_id
    for i in user:
        if i["user_id"] == msg["user_id"]:
            userlevel = i["user_level"]
        # print(userlevel)

    # filter sentences
    for i in range(0, len(sentence)):
        if request["text"] in sentence[i]["text"]:
            if sentence[i]["level"] == userlevel:
                msg["text"].append(sentence[i]["text"])
            else:
                print("I found sentence but your level doesn't match")

    return msg


# Завершаем вот здесь
def send_message(msg):
    # Вместо принта, а будущем ,у нас будет логика отправки сообщения на сервера Телеграм
    print(msg)


def main():
    user_db, sentences_db = prepare_data()
    user_request = userrequest()
    message = prepare_message(user=user_db, sentence=sentences_db,
                              request=user_request)
    send_message(message)


main()
