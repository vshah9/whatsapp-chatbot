from flask import Flask
from flask import request
from twilio.twiml.messaging_response import MessagingResponse
import sqlite3
import re

app = Flask(__name__)


@app.route("/", methods=["POST"])
# chatbot logic
def bot():
    # user input
    user_msg = request.values.get('Body', '').lower()

    # creating object of MessagingResponse
    response = MessagingResponse()
    if re.search("Hi", user_msg, re.IGNORECASE) or re.search("Hello", user_msg, re.IGNORECASE) \
            or re.search("Hey", user_msg, re.IGNORECASE):
        response.message(
            "Hello welcome to Retrench Application \n Please Select from the below options "
            "\n 1. For recording Expense \n 2. For recording Income")
        user_insert(request.values.get('WaId', ''), request.values.get('ProfileName', ''))
    elif user_msg == "1":
        response.message("Please enter brief about your Expense in the below format \n $XX at XXX")
    elif user_msg == "2":
        response.message("Please enter brief info about your Income in the below format \n $XX from XXX")
    elif re.search("$", user_msg):
        transaction_insert(user_msg, response, request.values.get('WaId', ''))

    return str(response)


def user_insert(whatsapp_id, profile_name):
    try:
        sqlite_connection = sqlite3.connect("chatbot.db")
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT Id FROM UserDetails where WhatsAppId = ?", [whatsapp_id])
        record = cursor.fetchone()
        print(record)
        if record is None:
            print('inside userid none')
            cursor.execute("INSERT into UserDetails (Name,WhatsAppId) values (?,?)",
                           (profile_name, whatsapp_id))
            cursor.execute("COMMIT;")
            print("User inserted successfully.")
            cursor.execute("Select * from UserDetails")
        else:
            print("user found ", record[0])
        cursor.close()
    except sqlite3.Error as error:
        print('Error occurred - ', error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print('SQLite Connection closed')


def transaction_insert(user_msg, response, whatsapp_id):
    try:
        sqlite_connection = sqlite3.connect("chatbot.db")
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT Id FROM UserDetails where WhatsAppId = ?", [whatsapp_id])
        record = cursor.fetchone()
        print(record)
        if record is not None:
            if re.search("from", user_msg):
                cursor.execute("INSERT into TransactionDetails (UserId,IncomeOrExpense,TransactionDesc,DateTime) "
                               "values (?,?,?,datetime('now', 'localtime'))",
                               (record[0], 'Income', user_msg))
                cursor.execute("COMMIT;")
                print("Details inserted successfully.")
                response.message("Thank You! Your transaction is recorded.")
                cursor.close()
            elif re.search("at", user_msg):
                cursor.execute("INSERT into TransactionDetails (UserId,IncomeOrExpense,TransactionDesc,DateTime) "
                               "values (?,?,?,datetime('now', 'localtime'))",
                               (record[0], 'Expense', user_msg))
                cursor.execute("COMMIT;")
                print("Details inserted successfully.")
                response.message("Thank You! Your transaction is recorded.")
                cursor.close()
            else:
                response.message("Sorry! Please enter the text in required format.")

    except sqlite3.Error as error:
        print('Error occurred - ', error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print('SQLite Connection closed')


if __name__ == "__main__":
    app.run()
