import random


def name_gen():
    """"""
    first_names = ["Mike", "Bobby", "Leo", "Damien", "Claudio", "Ed", "Kenzo", "Justin", "Bryan", "Casey",
                   "Maria", "Nina", "Corie", "Angela", "Jamie", "Crystal", "Suki", "Chris", "Sam", "Versan"]
    last_names = ["Portnoy", "Hill", "Daddario", "Echols", "Sanchez", "Kemper", "Tenma", "Long", "Cranston", "Anthony",
                  "Brink", "Fortner", "McBride", "Gossow", "Curtis", "Lake", "Park", "Benoit", "Lee", "Arche"]

    name = random.choice(first_names) + " " + random.choice(last_names)
    return name
