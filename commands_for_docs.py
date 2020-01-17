"""This code describes executing commands for some documents"""

# Catalog of documents
documents = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
]

# Shelfs for documents
directories = {
    '1': ['2207 876234', '11-2', '5455 028765'],
    '2': ['10006', '5400 028765', '5455 002299'],
    '3': []
}


def test_first_symbol_digits(symbol_string, digit_from, digit_to):
    """
    (string, int, int) -> boolean

    Function about belonging first symbol of string to one of digits from digit_from to digit_to

    """

    if len(symbol_string) > 0:
        if digit_from < 0 or digit_from > 9:
            return False

        if (symbol_string[0] >= str(digit_from)) and (symbol_string[0] <= str(digit_to)):
            return True
        else:
            return False
    else:
        return False


def test_string_digits(test_string):
    """
    (string) -> boolean

    Function about belonging symbols of string to one of digits from 0 to 9

    """

    result = True
    if len(test_string) > 0:
        for symbol in test_string:
            if symbol < '0' or symbol > '9':
                result = False
                break
    else:
        result = False
    return result


def input_number_document():
    """
    (None) -> string

    Function for input number of document and input validation

    """

    while True:
        number_document = input('Введите номер документа: ')

        if len(number_document) > 0:
            # input validation
            if test_first_symbol_digits(number_document, 0, 9):
                return number_document
            else:
                print("Номер документа должен начинаться с цифры (0..9).")
        else:
            print("Номер документа не должен быть пустым.")


def input_type_document():
    """
    (None) -> string

    Function for input type of document and input validation

    """
    while True:
        document_type = input('Введите тип документа, 0=passport, 1=invoice, 2=insurance (Пример: 1): ')

        # input validation
        if document_type == '0':
            return 'passport'
        elif document_type == '1':
            return 'invoice'
        elif document_type == '2':
            return 'insurance'
        else:
            print("Введено некорректное значение \"{0}\", а ожидается 0, 1 или 2.".format(document_type))


def input_name_owner():
    """
    (None) -> string

    Function for input document's owner name and input validation

    """

    while True:
        owner_name = input('Введите имя и фамилию владельца через пробел (Пример: Иван Иванов): ')

        # input validation
        if len(owner_name) > 0:
            if test_first_symbol_digits(owner_name, 0, 9):
                print("Имя владельца должно начинаться с буквы.")
            else:
                return owner_name
        else:
            print("Имя владельца не должно быть пустым.")


def input_number_shelf():
    """
    (None) -> string

    Function for input number of shelf, function not check existing of shelf

    """

    while True:
        shelf_number = input('Введите номер полки (Пример: 4): ')

        # input validation
        if len(shelf_number):
            if test_string_digits(shelf_number):
                return shelf_number
            else:
                print("Номер полки должен состоять только из цифр от 0 до 9.")
        else:
            print("Номер полки не должен быть пустым.")


def input_number_exist_shelf():
    """
    (None) -> string

    Function for input number of shelf, function check existing of shelf

    """
    while True:
        shelf_number = input_number_shelf()
        # Checking on existing such shelf
        if directories.get(shelf_number, -1) != -1:
            return shelf_number
            # break
        else:
            print("Введен несуществующий номер полки.")

        # Get document by number from catalog of documents


def get_document_by_number(document_number):
    """
    (string) -> {} or None

    Function searching document by number and returns dictionary of document.

    """

    for document in documents:
        if document['number'] == document_number:
            return document


# Get number of shelf by number of document from catalog of documents
def get_shelf_number_by_number_document(document_number):
    """
    (string) -> string or None

    Function searching document by number of document and returns shelf number where you can find it

    """

    for shelf_number in directories.keys():
        for item in directories[shelf_number]:
            if item == document_number:
                return shelf_number


def delete_document_from_shelfs(document_number):
    """
    (string) -> int or None

    Delete document by number of document from catalog of documents

    """

    # Delete this document from according shelf
    shelf_number = get_shelf_number_by_number_document(document_number)
    if shelf_number:
        directories[shelf_number].remove(document_number)
        return shelf_number


def delete_document_from_catalog(document_number):
    """
    (string) -> boolean

    Delete document with number of document from catalog of documents

    """

    document = get_document_by_number(document_number)
    if document:
        documents.remove(document)
        return True
    else:
        return False


def execute_command_add():
    """
    (None) -> None

    Function add document to catalog of documents and to shelf

    """
    # Ask user information about document
    while True:
        document_number = input_number_document()
        document = get_document_by_number(document_number)
        if document:
            print("Документ с номером \"{0}\" уже существует.".format(document_number))
        else:
            break

    document_type = input_type_document()
    owner_name = input_name_owner()
    shelf_number = input_number_exist_shelf()

    # Add information about document to documents
    document = dict()
    document['type'] = document_type
    document['number'] = document_number
    document['name'] = owner_name
    documents.append(document)
    print("Документ \"{0}\" добавлен в каталог документов.".format(document_number))

    # Add document to shelf
    shelf = directories[shelf_number]
    shelf.append(document_number)
    # print(directories)
    print("Документ \"{0}\" добавлен на полку \"{1}\".".format(document_number, shelf_number))


def execute_command_people():
    """
    (None) -> None

    Function return author of document by number

    """

    document_number = input_number_document()

    document = get_document_by_number(document_number)
    if document:
        author_name = document['name']

        if author_name:
            print("Автором документа с номером \"{0}\" является {1}.".format(document_number, author_name))
    else:
        print("Документ с номером \"{0}\" не найден.".format(document_number))


def execute_command_list():
    """
    (None) -> None

    Function print catalog of documents

    """

    # passport "2207 876234" "Василий Гупкин"
    if len(documents) > 0:
        print("Полный перечень документов каталога:")
        for document in documents:
            print('{0} \"{1}\" \"{2}\"'.format(document['type'], document['number'], document['name']))
    else:
        print("Каталог документов пуст.")


def execute_command_shelf():
    """
    (None) -> None

    Function returns number of shelf by number of document

    """
    document_number = input_number_document()
    shelf_number = get_shelf_number_by_number_document(document_number)
    if shelf_number:
        print("Документ с номером \"{0}\" находится на {1} полке.".format(document_number, shelf_number))
    else:
        print("Документ с номером \"{0}\" не найден ни на одной из полок.".format(document_number))


def execute_command_delete():
    """
    (None) -> None

    Function delete document from catalog of documents and from according shelf

    """

    document_number = input_number_document()

    shelf_number = delete_document_from_shelfs(document_number)
    if shelf_number:
        print("Документ \"{0}\" удален с полки \"{1}\".".format(document_number, shelf_number))
    else:
        print("Документ \"{0}\" не найден ни на одной из полок.".format(document_number))

    if delete_document_from_catalog(document_number):
        print("Документ \"{0}\" удален из каталога документов.".format(document_number))
    else:
        print("Документ \"{0}\" не найден в каталоге документов.".format(document_number))


def execute_command_move():
    """
    (None) -> None

    Function move document from one shelf to another

    """

    document_number = input_number_document()
    # Find this document in all shelfs
    shelf_number_old = get_shelf_number_by_number_document(document_number)

    if shelf_number_old:
        shelf_number_new = input_number_exist_shelf()
        if shelf_number_old != shelf_number_new:
            # Delete document from old shelf
            directories[shelf_number_old].remove(document_number)
            # Put document to new shelf
            directories[shelf_number_new].append(document_number)
            print(
                "Документ \"{0}\" перемещен с полки \"{1}\" на полку \"{2}\".".format(document_number, shelf_number_old,
                                                                                      shelf_number_new))
        else:
            print("Документ \"{0}\" и так находится на \"{1}\" полке.".format(document_number, shelf_number_new))
    else:
        print("Документ \"{0}\" не найден ни на одной из полок.".format(document_number))


def execute_command_add_shelf():
    """
    (None) -> None

    Function add new shelf

    """

    shelf_number = input_number_shelf()
    if not directories.get(shelf_number):
        directories[shelf_number] = []
        print("Добавлена полка номер \"{0}\".".format(shelf_number))
    else:
        print("Полка с номером \"{0}\" уже существует.".format(shelf_number))


def execute_command(command_name="p"):
    """
    (string) -> None

    Function organizes execute all commands

    """
    if command_name == "p":
        execute_command_people()
    elif command_name == "l":
        execute_command_list()
    elif command_name == "s":
        execute_command_shelf()
    elif command_name == "a":
        execute_command_add()
    elif command_name == "d":
        execute_command_delete()
    elif command_name == "m":
        execute_command_move()
    elif command_name == "as":
        execute_command_add_shelf()


def main():
    """
    (None) -> None

    Main function which organizes a dialog with user

    """

    while True:
        command = input('Введите команду (l=list, p=people, s=shelf, a=add, d=delete, m=move, as=add shelf q=quit): ')

        if command == 'q':
            print("Вы выбрали команду \"q\", следовательно выходим из программы.")
            break
        elif command in ('p', 'l', 's', 'a', 'd', 'm', 'as'):
            execute_command(command)
        else:
            print("Вы ввели неподдерживаемую команду: \"{0}\".".format(command))


# Point of entry to program
if __name__ == '__main__':
    main()
