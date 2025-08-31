import time
import util


URL = "http://127.0.0.1:5000"
AUTH = ""


def get_user_input(user_name, to):
    message = input(f"Send message to {to}: ")
    if not message:
        exit(0)
    return {
        'from': user_name,
        'content': message
    }


if __name__ == "__main__":
    send_to = input(f"Send message to?: ")
    mail = get_user_input("Lina", send_to)
    util.push_message(URL, AUTH, send_to, mail)
    while True:
        time.sleep(3)
        mails, _ = util.pull_message(URL, AUTH, "Lina")
        if mails:
            for mail in mails:
                print(mail['content'])
            mail = get_user_input("Lina", send_to)
            util.push_message(URL, AUTH, send_to, mail)
