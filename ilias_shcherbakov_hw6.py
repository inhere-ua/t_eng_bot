# Домашняя работа №6
#
# Тут все довольно просто - добавьте новые знания,
# о лямбдах и новых типах аргументах + тайпинге к текущему коду.


import csv
import re


def loadsentences():  # loading sentences from file
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


# user lang and keyword input with check
def user_input():
    lang_level = {"elementary": 1, "intermediate": 2, "advanced": 3}
    while True:
        # printing all available lang levels
        print("Welcome to lang bot. I have phrases "
              "for the following English levels:")
        for key in lang_level.keys():
            print(key)

        # ask for user lang input
        user_level = input("Enter your language level: ")

        # check user input to match lang_level with .lower() to ignore case
        if user_level.lower() in lang_level:
            user_level = lang_level[user_level]
            break

        # if misinput ask to re-enter
        print("Can't recognize your level. Choose again, please")

    # keyword with lower case to avoid case sensitivity
    user_word = input("Enter the word to get "
                      "the sentences with: ").lower()

    # setting user profile
    # 'hits_found' is the list of matched sentences, now empty
    user1 = {"lang_level": user_level, "keyword": user_word, "hits_found": []}

    return user1


def matchsentence(user_profile: dict = None, sentence_dict: dict = None):
    # now run the match process
    hits_found = []
    user_word = user_profile["keyword"]

    for key in sentence_dict.keys():

        # check sentence to meet the user level
        if sentence_dict[key]["level"] == user_profile["lang_level"]:

            # debug
            # print("level match ok")
            # print(sentence_dict[key]["text"].lower())

            # check sentence contain the keyword as the separate word
            # ignoring letter case
            target_sentence = re.search(rf"\b{user_word}\b",
                                        sentence_dict[key]["text"].lower(),
                                        re.IGNORECASE)

            # filling match sentences list
            if target_sentence is not None:
                # print("sentence match ok")    # debug only

                hits_found.append(sentence_dict[key]["text"])

    return hits_found


def print_results(user_profile: dict = None):
    # now get the hits list
    if len(user_profile["hits_found"]) < 1:

        # if no matches print sorry
        print("Sorry, no matching sentence with your"
              " keyword '{}' in my list.".format(user_profile["keyword"]))
    else:
        # now get the count of hits
        print("I have found {} matches in my dict. "
              "Here are they: \n".format(len(user_profile["hits_found"])))

        # print all the matches
        for item in user_profile["hits_found"]:
            print(item)
    return


def main():
    sentences = loadsentences()  # load sentences
    user = user_input()  # user input

    user["hits_found"] = matchsentence(user,
                                       sentences)  # find matching phrases
    print_results(user)  # print results


if __name__ == '__main__':
    main()  # run script
