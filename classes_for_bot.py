from collections import UserDict
from datetime import datetime
import pickle


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    pass


class Phone(Field):
    @Field.value.setter
    def value(self, value):
        if len(value) < 10 or len(value) > 12:
            raise ValueError("Phone must contains 10 symbols.")
        if not value.isnumeric():
            raise ValueError('Wrong phones.')
        self._value = value


class Birthday(Field):
    @Field.value.setter
    def value(self, value):
        today = datetime.now().date()
        birth_date = datetime.strptime(value, '%Y-%m-%d').date()
        if birth_date > today:
            raise ValueError("Wrong input")
        self._value = value


class Record:
    def __int__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def get_info(self,):
        phone_info = ''
        birthday_info = ''
        for phone in self.phones:
            phone_info += f'{phone.value}, '
        if self.birthday:
            birthday_info = f' Birthday : {self.birthday.value}'
        return f'{self.name.value} : {phone_info}{birthday_info}'

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def delete_phone(self, phone):
        for record_phone in self.phones:
            if record_phone.value == phone:
                self.phones.remove(record_phone)
                return True
        return False

    def change_phones(self, phones):
        for phone in phones:
            if not self.delete_phone(phone):
                self.add_phone(phone)

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def days_to_birthday(self):
        if not self.birthday:
            raise ValueError("birthday not found for this contact")

        today = datetime.now().date()
        birthday = datetime.strptime(self.birthday.value, '%Y-%m-%d').date()
        next_birthday_year = today.year

        if today.month >= birthday.month and today.day > birthday.day:
            next_birthday_year += 1

        next_birthday = datetime(
            year=next_birthday_year,
            month=birthday.month,
            day=birthday.day
        )

        return (next_birthday.date() - today).days


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.load_from_file()

    def add_record(self, record):
        self.data[record.name.value] = record

    def get_all_record(self):
        return self.data

    def has_record(self, name):
        return bool(self.data.get(name))

    def get_record(self, name) -> Record:
        return self.data.get(name)

    def remove_record(self, name):
        del self.data[name]

    def search(self, value):
        if self.has_record(value):
            return self.get_record(value)

        for record in self.get_all_record().values():
            for phone in record.phones:
                if phone.value == value:
                    return record
        raise ValueError('contact not found')

    def save_to_file(self):
        with open('contacts_book.bin', 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self):
        try:
            with open('contacts_book.bin', 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            pass
