import matplotlib.pyplot as plt
import socket

HOST = '173.255.242.108'
PORT = 2113   # Port 80 is used for HTTP requests


def get_info(store):
    response_count = 0
    # List of valid companies to use in link.send()
    # [adidas, asics, athleta, callaway, canterbury, lululemon athletica, nike, puma, sondico, under armour]
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as link:
        link.connect((HOST, PORT))  # Sets up connection to specified host and port
        # .encode() is used to convert str to byte. Got an error when .encode() was not used
        link.send(store.encode())

        while True:

            response = link.recv(1024)  # Create a buffer of 1024 bytes to hold the response from GET request

            if not response:
                break

            if response_count == 0:
                # Decode to turn bytes back to str
                pie_data = eval(response.decode())

            if response_count == 1:
                pie_labels = eval(response.decode())

            response_count += 1
        return [pie_data, pie_labels]


if __name__ == '__main__':

    pie_data = get_info("nike")[0]
    pie_labels = get_info("nike")[1]
    print(pie_data)
    print(pie_labels)

    fig1, ax1 = plt.subplots()
    ax1.pie(pie_data, labels=pie_labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()
