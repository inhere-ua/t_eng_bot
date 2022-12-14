import requests
import json


class Bot:
    root_url = "https://api.telegram.org/bot"

    def __init__(self, token = "5457303465:AAHgmUNybFaABHK7xPXixk571hdzKfyitT8"):
        self.token = token
        self.last_msg_id = 0


    def getUpdate(self):
        url = f"{self.root_url}{self.token}/getUpdates"

        try:
            self._req_res = requests.get(url)

        except Exception as e:
            print(f"Get update failed due to '{e}' error")


        # check the bot status
        if self._req_res.status_code in self.good_codes:
            self._req_json = self._req_res.json()

        else:
            print(f"request failed with error {self._req_res.status_code}")


    # send message function
    def SendMsg(self, root_url: str, good_codes: tuple, token1: str,
                 chat_id: int, msg: object):
        url = f"{root_url}{token1}/sendMessage"

        self._req_res = requests.post(url, data={"chat_id": chat_id, "text": msg})

        # check messange sent status
        if self._req_res.status_code in good_codes:
            print("message sent ok")

        else:
            print(f"request failed with error {self._req_res.status_code}")


    # parse available sentences for keyword
    def CheckWord(self, word: str, usrlvl: int, chat_id: int,
                   root_url, good_codes, token):

        found_msg = False  # found message flag

        # iterating through the database
        for key in self.sentencedb.keys():
            if word in self.sentencedb[key]["text"]:
                found_msg = True  # once found any match, flag is set True

                # check if user level matches sentence level
                if self.sentencedb[key]["level"] == usrlvl:
                    Bot().SendMsg(chat_id=chat_id,
                             msg=self.sentencedb[key]["text"])
                else:
                    Bot().SendMsg(chat_id=chat_id,
                             msg="I found sentence but your level doesn't match")

        # return no matches result to user
        if not found_msg:
            Bot().SendMsg(root_url, good_codes, token, chat_id,
                     msg=f"Sorry, no sentence with {word} found")

        # ask user for another keywork to search
        Bot().SendMsg(root_url, good_codes, token, chat_id,
                 msg=f"Enter another keyword, please")


class User:


    def __init__(self, userdb_path = 'E:\\db.csv'):
        self.userdbpath = userdb_path

        with open(self.userdbpath, "r") as file:
            self.userdb = json.loads(file.read())

    def ValidateUser(self, users: list, update: dict, usr_level: int):
        user_exist = False

        for user in users:
            if user["user_id"] == update["user_id"]:
                user_exist = True

        if not user_exist:
            user = {"user_id": update["user_id"],
                    "chat_id": update["chat_id"],
                    "usr_lvl": usr_level}
            users.append(user)


    def AddUser(self):
        self.userdb.append()


    # save database
    def SaveDB(self):
        try:
            with open(self.userdbpath, "w") as file:
                json.dump(self.userdb, file, indent=4)
        except Exception as e:
            print("Failed to save")


class Parser:

    def __init__(self):
        self.sentencedb = {}

    # load sentences
    def LoadSentences(self):

        # opening file with list of sentences
        with open("English_sentences.csv", "r") as csvfile:
            tempcsv = csv.reader(csvfile)  # reading csv file
            i = 1

            # iterating through the file
            for row in tempcsv:
                name = "sentence_" + str(i)  # creating nested dict

                # filling nested dict with sentence text and sentence level
                self.sentencedb[name] = {"text": row[0], "level": int(row[2])}

                # dealing with the 'B\xa0' non-breaking space problem in csv file
                self.sentencedb[name]["text"] = \
                    self.sentencedb[name]["text"].replace(u"??\xa0", u" ")

                i += 1

    # extract user_id, chat_id, message_id and message text from update
    def FormatUpdate(self, update: dict):

        user_id = update["result"][-1]["message"]["from"]["id"]
        chat_id = update["result"][-1]["message"]["chat"]["id"]
        text = update["result"][-1]["message"]["text"]

        # print(update)
        message_id = update["result"][-1]["update_id"]

        return {"user_id": user_id, "chat_id": chat_id,
                "text": text, "message_id": message_id}






# run main program
def main():

    # get updates if any
    update = format_update(get_update(root_url, good_codes, token))
    chat_id = update["chat_id"]

    while True:
        update = format_update(get_update(root_url, good_codes, token))

        # check if start word is typed
        if update["text"] == "/start" and last_message_id != update["message_id"]:
            last_message_id = update["message_id"]
            send_msg(root_url, good_codes, token, chat_id,
                     msg="Enter your English level (1 - Beginner, "
                         "2 - Intermediate, 3 - Advanced)")

        # ask for user level if not known
        if format_update(get_update(root_url, good_codes, token))["text"] \
                in ("1", "2", "3") and last_message_id != update["message_id"]:
            last_message_id = update["message_id"]
            usr_level = int(update["text"])
            validate_user(users, update, usr_level)

            # ask for keyword input
            send_msg(root_url, good_codes, token, chat_id,
                     msg="Enter the keyword")

        else:
            send_msg(root_url, good_codes, token, chat_id,
                     msg="Wrong level received.")

            send_msg(root_url, good_codes, token, chat_id,
                     msg="Enter your English level (1 - Beginner, "
                         "2 - Intermediate, 3 - Advanced)")

        # if user input received
        if last_message_id != update["message_id"]:
            last_message_id = update["message_id"]
            for user in users:
                if user["user_id"] == update["user_id"]:
                    usr_level = user["usr_lvl"]
                    check_word(sentences, update["text"], usr_level, chat_id,
                               root_url, good_codes, token,)


good_codes = (200, 201, 202, 203, 204)



main()



temp_bot = echobot()
temp_bot.getUpdate()
