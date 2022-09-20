import requests
import csv

# load sentences
def load_sentences():
    sentences1 = {}  # initializing dict

    # opening file with list of sentences
    with open("English_sentences.csv", "r") as csvfile:
        tempcsv = csv.reader(csvfile)  # reading csv file
        i = 1

        # iterating through the file
        for row in tempcsv:
            name = "sentence_" + str(i)  # creating nested dict

            # filling nested dict with sentence text and sentence level
            sentences1[name] = {"text": row[0], "level": int(row[2])}

            # dealing with the non-breaking space 'B\xa0' problem in csv file
            sentences1[name]["text"] = \
                sentences1[name]["text"].replace(u"В\xa0", u" ")

            i += 1
    # print("Loaded sentences: ", len(sentences1))  # debug only
    # print("sample sentence: ", sentences1["sentence_1"])  # debug only

    return sentences1

# check bot active
def get_update(root_url: str, good_codes: tuple, token1: str):
    url = f"{root_url}{token1}/getUpdates"
    result = requests.get(url)
    if result.status_code in good_codes:
        print("all is ok")
        print(result.json())
        return result.json()
    else:
        print(f"request failed with error {result.status_code}")


def format_update(update: dict):
    user_id = update["result"][-1]["message"]["from"]["id"]
    chat_id = update["result"][-1]["message"]["chat"]["id"]
    text = update["result"][-1]["message"]["text"]
    # print(update)
    message_id = update["result"][-1]["update_id"]

    return {"user_id": user_id, "chat_id": chat_id, "text": text, "message_id": message_id}


def send_msg(root_url: str, good_codes: tuple, token1: str, chat_id: int, msg: object):
    url = f"{root_url}{token1}/sendMessage"
    result = requests.post(url, data={"chat_id": chat_id, "text": msg})
    if result.status_code in good_codes:
        print("message sent ok")
    else:
        print(f"request failed with error {result.status_code}")


def check_word(sentences_list: dict, word: str, usrlvl: int, chat_id: int, root_url, good_codes, token):
    found_msg = False
    for sentence in sentences_list:
        if word in sentence["text"]:
            found_msg = True
            if sentence["level"] == usrlvl:
                send_msg(root_url, good_codes, token, chat_id,
                         msg=sentence["text"])
            else:
                send_msg(root_url, good_codes, token, chat_id,
                         msg="I found sentence but your level doesn't match")

    if not found_msg:
        send_msg(root_url, good_codes, token, chat_id,
             msg=f"Sorry, no sentence with {word} found")

def validate_user(users: list, update: dict, usr_level: int):
    user_exist = False
    for user in users:
        if user["user_id"] == update["user_id"]:
            user_exist = True
    if not user_exist:
        user = {"user_id": update["user_id"], "chat_id": update["chat_id"],
                "usr_lvl": usr_level}
        users.append(user)
        # here to save user in db



        # print(users)
        print("user is added")


def main():
    root_url = "https://api.telegram.org/bot"
    token = "5457303465:AAHgmUNybFaABHK7xPXixk571hdzKfyitT8"
    good_codes = (200, 201, 202, 203, 204)
    sentences = load_sentences()
    users = []
    last_message_id = 0
    update = format_update(get_update(root_url, good_codes, token))
    chat_id = update["chat_id"]

    while True:
        update = format_update(get_update(root_url, good_codes, token))
        # check if start word
        if update["text"] == "/start" and last_message_id != update["message_id"]:
            last_message_id = update["message_id"]
            send_msg(root_url, good_codes, token, chat_id,
                     msg="Enter your English level (1 - Beginner, 2 - Intermediate, 3 - Advanced)")

        # ask for user level if not known
        if format_update(get_update(root_url, good_codes, token))["text"] in ("1", "2", "3") and last_message_id != update["message_id"]:
            last_message_id = update["message_id"]
            usr_level = int(update["text"])
            validate_user(users, update, usr_level)

            # after user level is processed, ask for keyword to search
            send_msg(root_url, good_codes, token, chat_id, msg="Enter the keyword")

        # asl
        if last_message_id != update["message_id"]:
            last_message_id = update["message_id"]
            for user in users:
                if user["user_id"] == update["user_id"]:
                    usr_level = user["usr_lvl"]
                    check_word(sentences, update["text"], usr_level, chat_id, root_url, good_codes, token,)


main()







