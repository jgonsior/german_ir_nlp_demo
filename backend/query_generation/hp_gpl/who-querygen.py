import json
import format_json
import pandas as pd

harry_potter_characters = [
    "Harry Potter", 
    #"Hermine Granger", 
    "Ronald Weasley", "Albus Dumbledore", 
    #"Severus Snape", 
    #"Rubeus Hagrid",
    "Sirius Black", 
    #"Remus Lupin",
      "Minerva McGonagall", "Draco Malfoy", "Tom Riddle", "Bellatrix Lestrange",
    "Neville Longbottom", "Luna Lovegood", 
    #"Ginevra Weasley", 
    "Fred Weasley", "George Weasley","Percy Weasley",
    "Arthur Weasley", "Molly Weasley", "Cedric Diggory","Cho Chang", "Nymphadora Tonks", "Lucius Malfoy",
    "Narzissa Malfoy",
    "Peter Pettigrew",
    "Alastor Moody",
    "Fleur Delacour",
    "Viktor Krum",
    "Dolores Umbridge",
    "Argus Filch",
    "Gilderoy Lockhart",
    #"Cornelius Fudge",
    "Horace Slughorn",
    "Rita Kimmkorn",
    #"Sybill Trelawney",
    "Filius Flitwick",
    "Poppy Pomfrey",
    "Pomona Sprout",
    "Aberforth Dumbledore",
    #"Andromeda Tonks",
    "Edward Tonks",
    "Lavender Brown",
    "Parvati Patil",
    "Padma Patil",
    #"Dean Thomas",
    "Seamus Finnigan",
    "Oliver Wood",
    "Angelina Johnson",
    "Katie Bell",
    "Alicia Spinnet",
    "Marietta Edgecombe",
    "Vincent Crabbe",
    "Gregory Goyle",
    #"Pansy Parkinson",
    "Blaise Zabini",
    "Dobby",
    "Kreacher",
    "Griphook",
    "Winky",
    "Rosmerta",
    "Bathilda Bagshot",
    "Xenophilius Lovegood",
    "Scorpius Malfoy",
    #"Astoria Malfoy",
    #"Hannah Abbott",
    #"Susan Bones",
    "Terry Boot",
    "Michael Corner",
    "Ernest Macmillan",
    "Justin Finch-Fletchley",
    "Zacharias Smith",
    "Anthony Goldstein",
    "Roger Davies",
    "Cormac McLaggen",
    #"Romilda Vane",
    "Mundungus Fletcher",
    #"Fenrir Greyback",
    "Corban Yaxley",
    "Thorfinn Rowle",
    "Travers",
    "Antonin Dolohow",
    "Alecto Carrow",
    "Amycus Carrow",
    "Nott",
    "Regulus Black",
    "Aragog",
    "Seidenschnabel",
    "Fawkes",
    "Nagini",
    #"Bane",
    "Firenze",
    "Grawp",
    "Hedwig",
    "Errol",
    "Pigwidgeon",
    #"Krummbein",
    #"Mrs. Norris",
    #"Trevor",
    "Myrte Warren", 
    "Lee Jordan",
    "Peeves",
    "Nicholas de Mimsy-Porpington",
    "Helena Ravenclaw",
    "Der Fette Mönch",
    "Der Blutige Baron", 
    #"Cuthbert Binns",
    "Rolanda Hooch", 
    "Phineas Nigellus Black",
    "Petunia Dursley", 
    "Vernon Dursley",
    "Dudley Dursley",
    #"Magdalena Dursley",
    #"Rufus Scrimgeour",
    "Amelia Bones", 
    "Bartemius Crouch Junior",
    "Bartemius Crouch Senior",
    "Ludovic Bagman", 
    "Igor Karkaroff",
    "Olympe Maxime",
    "Augustus Rookwood",
    "Walden Macnair", 
    "Stanley Shunpike"
]

# patterns to filter out paragraph which don't answer "Who"-question
text_to_avoid = [   "Dieser Artikel stammt ursprünglich aus dem Harry Potter Wiki", 
                    "[- WEITERLEITUNG", 
                    "[- REDIRECT", 
                    "Er ist nicht vollständig Arbeit des Harry-Potter-Lexikons.",
                    "Zumindest einige Inhalte in diesem Artikel werden abgeleitet aus Informationen, die in der letzten vorgestellten Aktualisierung von \"Pottermore\"",
                    "Dieser Artikel ist über ",
                    "Dieser Artikel behandelt"   
                 ]

def get_last_id(dir: str):
    """ 
    generate qgen-queries.json file from jsonl, easier to get last element
    get last question id
    
    Arguments:
        dir -- directory of qgen-queries.json file

    Returns:
       get last id of question
    """
    format_json.jsonl_to_json(f"{dir}/qgen-queries.jsonl")
    with open(f"{dir}/qgen-queries.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    last = data[-1]["_id"][4:]    
    return int(last)


def whoqgen(dir: str):
    """
        manually create "Who"-questions and add to training data, because current models didn't do well on them
        creates who-questions.jsonl and qrels.tsv 
        and then manually add to training data

        TODO: Filter out "Who"
        -questions generated by qgen.py's, the matched answer is wrong
    """
    questions = []
    #question_answer_tuple = []

    # DEBUGGING
    #question_answer_tuple_text = []

    with open(f"{dir}/corpus.jsonl", "r", encoding="utf-8") as f:
        id = get_last_id(dir) + 1
        check_id = 0
        # DEBUGGING
        #character_skipped = harry_potter_characters.copy()

        for paragraph in f:
            data = json.loads(paragraph)
            # not every answer to "Who"-question is answered in the first paragraph, so filter out these paragraph 
            # and remember the paragraph ID of wikiPage 
            # (e.g. 42669-0 -> wikiPage_ID: 42669, paragraph_ID: 0)
            if (any(item in data["text"] for item in text_to_avoid) or (data["text"] == "\"\"")) and (data["title"] in harry_potter_characters):
                check_id += 1
                continue

            if (f"-{check_id}" in data["_id"]) and (data["title"] in harry_potter_characters):
                question = {}
                question["_id"] = f"genQ{id}"

                id +=1
                check_id = 0

                question["text"] = f"Wer ist {data['title']}?"

                questions.append(question)
                #for tsv file
                #question_answer_tuple.append((question["_id"], data["_id"], 1))

                # DEBUGGING
                #question_answer_tuple_text.append((data["title"], question["text"], data["text"]))
                #character_skipped.remove(data["title"])

    with open(f"{dir}/who-questions.jsonl", "w", encoding="utf-8") as f:
        for question in questions:
            f.write(json.dumps(question) + "\n")

    #create tsv file for positive scoring
    # columns = ["query-id", "corpus-id", "score"]
    # df = pd.DataFrame(question_answer_tuple, columns=columns)
    # df.to_csv(f"{dir}/qrels-character.tsv", sep="\t", index=False)


if __name__ == "__main__":
    dir = "hp-malte-translate"
    whoqgen(dir)

    # need to manually insert "Who-questions" (and qrels-character.tsv) data into 
    # qgen-queries.jsonl (and qgen-qrels/train.tsv)

    # DEBUGGING
    # for tpl in question_answer_tuple_text:
    # print(tpl)
    # print()  # Add an empty line between tuples

    # print(len(harry_potter_characters))
    # print(len(question_answer_tuple_text))

    # #print(len(harry_potter_characters))
    # #print(len(character_skipped))
    # print(character_skipped)
