import matplotlib.pyplot as plt

info_to_parse = ("Headquarters near Beaverton, Oregon|FormerlyBlue Ribbon Sports, Inc.(1964–1971)|TypePublic|Traded "
                 "asNYSE: NKE (Class B)DJIA componentS&P 100 componentS&P 500 component|"
                 "IndustryApparelAccessoriesSports equipment|FoundedJanuary 25, 1964; 57 years ago (1964-01-25)|"
                 "FoundersBill BowermanPhil Knight|HeadquartersBeaverton, Oregon, U.S.|Area servedWorldwide|"
                 "Key peoplePhil Knight(Chairman Emeritus)Mark Parker(Executive Chairman)John Donahoe"
                 "(President and CEO)|ProductsAthletic footwear & apparelAthletic & recreational productsSports "
                 "equipment|Revenue US$37.40 billion (2020)|Operating income US$3.12 billion (2020)|"
                 "Net income US$2.54 billion (2020)|Total assets US$31.34 billion (2020)|"
                 "Total equity US$8.06 billion (2020)|Number of employees75,400 (2020)|Websitenike.com")

parsed = {}
cnum = 0
str_pair = ["", ""]
list_index = 0

for letter in info_to_parse:

    if len(str_pair[list_index]) == 0:
        str_pair[list_index] += letter
        cnum += 1
        continue

    if list_index == 0:

        # If letter is capital and previous letter was lowercase:
        if (64 < ord(letter) < 91) and (96 < ord(str_pair[0][len(str_pair[0]) - 1]) < 123):
            list_index += 1

        # If letter is "$" and previous letter was not a "|" or a space.
        if ord(letter) == 36:
            list_index += 1

    if ord(letter) == 124:
        key = str_pair[0]
        value = str_pair[1]
        parsed[key] = value
        list_index = 0
        str_pair = ["", ""]
        continue

    str_pair[list_index] += letter
    cnum += 1

economic_data = {'Revenue': parsed['Revenue US'], 'Operating Income': parsed['Operating income US'],
                 'Net Income': parsed['Net income US']}

print(economic_data)

for key, value in economic_data.items():
    value = value.replace(" (2020)", "")
    value = value.replace("$", "")
    value = value.replace(".", "")
    value = value.replace(" billion", "0000000")
    value = value.replace(" million", "0000")
    value = int(value)
    economic_data[key] = value

print(economic_data)

pie_data = [economic_data["Revenue"] - economic_data['Operating Income'], economic_data['Operating Income'] -
            economic_data['Net Income'], economic_data['Net Income']]
pie_labels = ["Operating Costs", "Other Expenses", "Net Income"]

fig1, ax1 = plt.subplots()
ax1.pie(pie_data, labels=pie_labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()
