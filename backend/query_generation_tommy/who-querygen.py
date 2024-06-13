import json
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

questions = []
question_answer_tuple = []
question_answer_tuple_text = []

text_to_avoid = [   "Dieser Artikel stammt ursprünglich aus dem Harry Potter Wiki", 
                    "[- WEITERLEITUNG", 
                    "[- REDIRECT", 
                    "Er ist nicht vollständig Arbeit des Harry-Potter-Lexikons.",
                    "Zumindest einige Inhalte in diesem Artikel werden abgeleitet aus Informationen, die in der letzten vorgestellten Aktualisierung von \"Pottermore\"",
                    "Dieser Artikel ist über ",
                    "Dieser Artikel behandelt"   
                 ]

with open("hp-ger/corpus.jsonl", "r", encoding="utf-8") as file:
    id = 0
    check_id = 0
    character_skipped = harry_potter_characters.copy()
    for paragraph in file:
        data = json.loads(paragraph)
        if (any(item in data["text"] for item in text_to_avoid) or data["text"] == "\"\"") and data["title"] in harry_potter_characters:
            check_id += 1
            continue

        if f"-{check_id}" in data["_id"] and data["title"] in harry_potter_characters:
            question = {}
            question["_id"] = f"genQ{id}"

            id +=1
            check_id = 0

            question["text"] = f"Wer ist {data['title']}?"
            question["metadata"] = {}

            questions.append(question)
            question_answer_tuple.append((question["_id"], data["_id"], 1))

            question_answer_tuple_text.append((data["title"], question["text"], data["text"]))

            character_skipped.remove(data["title"])

with open("hp-ger/who-questions.jsonl", "w", encoding="utf-8") as file:
    for question in questions:
        file.write(json.dumps(question) + "\n")


columns = ["query-id", "corpus-id", "score"]
df = pd.DataFrame(question_answer_tuple, columns=columns)
df.to_csv("hp-ger/qrels-character.tsv", sep="\t", index=False)

for tpl in question_answer_tuple_text:
    print(tpl)
    print()  # Add an empty line between tuples

print(len(harry_potter_characters))
print(len(question_answer_tuple_text))

#print(len(harry_potter_characters))
#print(len(character_skipped))
print(character_skipped)

