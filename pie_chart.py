# Gage McPursifull
# CS 361
# Creates a socket connection to gaia.cs.umass.edu, and sends a GET request to
# /wireshark-labs/HTTP-wireshark-file3.html. This program differs from small_get.py, in that it can handle a GET request
# of any size.
# Sources: Textbook - K&R: Chapter 2.7 TCPServer.py
# https://zetcode.com/python/socket/ - Echo client server example


import socket

HOST_1 = ''  # Using the IP address specified in the instructions
PORT_1 = 2113   # Using a port > 1023 as per HW instructions
HOST_2 = 'bigballer420.pythonanywhere.com'
PORT_2 = 80   # Port 80 is used for HTTP requests

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST_1, PORT_1))  # Sets up connection to specified host and port
    # .encode() is used to convert str to byte. Got an error when .encode() was not used
    server.listen(1)

    while True:

        connection, address = server.accept()  # Create a buffer of 1024 bytes to hold the response from GET request
        request = connection.recv(1024).decode()

        # for company in sport_list:
        info_to_parse = ""

        string = 'GET /?name=' + request + ' HTTP/1.1\r\nHost:bigballer420.pythonanywhere.com\r\n\r\n'
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as link:
            link.connect((HOST_2, PORT_2))  # Sets up connection to specified host and port
            # .encode() is used to convert str to byte. Got an error when .encode() was not used
            link.send(string.encode())

            response = link.recv(1024)  # Create a buffer of 1024 bytes to hold the response from GET request

            info_to_parse += response.decode()  # Append response to info_to_parse

        print(info_to_parse)
        print(request)
        parsed = {}
        rev = ""
        op_in = ""
        net_in = ""
        go = True

        index = info_to_parse.find("Revenue")
        index += len("Revenue")

        while go is True:

            # 92 is "\". Undefined ascii characters show up in the form \uXXXX.
            # These are things like the symbols for yen and pound sterling.
            # To skip these, add 6 to index whenever "\" is found
            if ord(info_to_parse[index]) == 92:
                index += 6
                continue

            # If a character is a number or '.', add it to rev
            if 47 < ord(info_to_parse[index]) < 58 or ord(info_to_parse[index]) == 45\
                    or ord(info_to_parse[index]) == 46:
                rev += info_to_parse[index]

            # If a character is m or b, it signifies the end of relevant numbers. m for million, b for billion.
            # Add letter to the string, then end loop by setting go to False
            if info_to_parse[index] == 'm' or info_to_parse[index] == 'M' \
                    or info_to_parse[index] == 'b' or info_to_parse[index] == 'B':
                rev += info_to_parse[index]
                parsed["Revenue"] = rev     # Create dictionary entry with the finished string "rev"
                go = False

            index += 1      # Increment index for next iteration of loop

        index = info_to_parse.find("Operating income")
        index += len("Operating income")

        while go is False:

            if ord(info_to_parse[index]) == 92:
                index += 6
                continue

            if 47 < ord(info_to_parse[index]) < 58 or ord(info_to_parse[index]) == 45 \
                    or ord(info_to_parse[index]) == 46:
                op_in += info_to_parse[index]

            if info_to_parse[index] == 'm' or info_to_parse[index] == 'M' \
                    or info_to_parse[index] == 'b' or info_to_parse[index] == 'B':
                op_in += info_to_parse[index]
                parsed["Operating Income"] = op_in     # Create dictionary entry with the finished string "op_in"
                go = True

            index += 1

        index = info_to_parse.find("Net income")
        index += len("Net income")

        while go is True:

            if ord(info_to_parse[index]) == 92:
                index += 6
                continue

            if 47 < ord(info_to_parse[index]) < 58 or ord(info_to_parse[index]) == 45 \
                    or ord(info_to_parse[index]) == 46:
                net_in += info_to_parse[index]

            if info_to_parse[index] == 'm' or info_to_parse[index] == 'M' \
                    or info_to_parse[index] == 'b' or info_to_parse[index] == 'B' or info_to_parse[index] == "(":
                net_in += info_to_parse[index]
                parsed["Net Income"] = net_in  # Create dictionary entry with the finished string "op_in"
                go = False

            index += 1

        for key, value in parsed.items():

            dec = value.find(".")
            if dec == -1:
                dec = len(value)-2
            zeros = 0

            if 'm' in value or 'M' in value:
                zeros = 6
                value = value.replace('m', '')
                value = value.replace('M', '')
            elif 'b' in value:
                zeros = 9
                value = value.replace('b', '')

            value = value.replace('(', '')

            while (len(value)-1) - dec < zeros:
                value += '0'

            value = value.replace('.', '')
            value = int(value)
            parsed[key] = value

        if request == 'asics':
            parsed['Net Income'] = 0
        pie_data = [parsed["Revenue"] - parsed['Operating Income'],
                    parsed['Operating Income'] - parsed['Net Income'], parsed['Net Income']]
        pie_labels = ["Operating Costs", "Other Expenses", "Net Income"]

        connection.send(str(pie_data).encode())
        connection.send(str(pie_labels).encode())

        connection.close()
