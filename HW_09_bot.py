from classes_for_bot import AddressBook, Record
contacts_dict = AddressBook()


def error_handler(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'This contact doesnt exist, please try again'
        except ValueError as exception:
            return exception.args[0]
        except IndexError:
            return 'This contact cannot be added, it exists already'
        except TypeError:
            return 'Unknown command, please try again'
    return inner


@error_handler
def add_user(args):
    name, phone = args
    if name in contacts_dict:
        raise ValueError('This user already exist')
    record = Record(name)
    for ph in phone:
        record.add_phone(ph)

    contacts_dict.add_record(record)
    return f"User {name}: {phone} added"


@error_handler
def change_phone(args):
    name, phone = args
    record = contacts_dict[name]
    record.change_phones(phone)
    return f"User {name} have a new phone number, old was: {record}"


@error_handler
def show_number(args):
    user = args[0]
    phone = contacts_dict[user]
    return f"{user}: {phone}"


def show_all(_):
    result = ""
    for name, phone in contacts_dict.items():
        result += f"{name}: {phone} \n"
    return result


@error_handler
def del_phone(name):
    name = name.strip()
    contacts_dict.remove_record(name)
    return 'Contact was deleted'


@error_handler
def del_phone_func(data):
    name, phone = data.strip().split(' ')
    record = contacts_dict[name]
    if record.delete_phone(phone):
        return f'Phone {phone} for {name} contact deleted.'
    return f'{name} contact does not have this number'


@error_handler
def add_birthday(data):
    name, date = data.strip().split(' ')
    record = contacts_dict[name]
    record.add_birthday(date)
    return f'For {name} you add Birthday {date}'


@error_handler
def days_to_birthday(name):
    name = name.strip()
    record = contacts_dict[name]
    return f"Days to next birthday of this {name} will be in {record.days_to_birthday()}."


def hello(_):
    return "How can I help you?"


def exit(_):
    return "Good bye!"


HANDLERS = {
    "hello": hello,
    "good_bye": exit,
    "close": exit,
    "exit": exit,
    "add": add_user,
    "change": change_phone,
    "show_all": show_all,
    "phone": show_number,
    "del_phone": del_phone,
    "del_phone_func": del_phone_func,
    "birthday": add_birthday,
    "days_to_birthday": days_to_birthday
}


@error_handler
def parser_input(user_input):
    cmd, *args = user_input.split()
    try:
        handler = HANDLERS[cmd.lower()]
    except KeyError:
        if args:
            cmd = f"{cmd} {args[0]}"
            args = args[1:]
        handler = HANDLERS[cmd.lower(), "Unknown command"]
    return handler, args


def main():
    while True:
        user_input = input("Enter command> ")
        handler, *args = parser_input(user_input)
        result = handler(*args)
        if not result:
            print("Good bye!")
            break
        print(result)


if __name__ == "__main__":
    main()

