def log_functions(func):
    def wrapper(*args):
        status = None
        try:
            status = func(*args)
        finally:
            args = [arg for arg in args if str(arg).find('FinanceManager') == -1]
            print(f'Лог: {func.__name__} вызвана с аргументами {args} и результатом {status[1]}')
        return status[0]
    return wrapper


class FinanceManager:
    def __init__(self):
        self.__balance = 0.0
        self.__transactions = []

    @log_functions
    def add_transaction(self, type, amount, category):
        try:
            self.__transactions.append({'type': type, 'amount': float(amount), 'category': category})
            self.__balance += float(amount) * (1 if type.lower() == 'доход' else -1)
            return [None, True]
        except:
            return [None, False]

    @log_functions
    def get_transactions(self):
        return [self.__transactions, True]

    @log_functions
    def get_balance(self):
        return [self.__balance, True]

    def save_data(self):
        try:
            with open('data.txt', 'w', encoding='UTF-8') as f:
                text = f'balance:{self.__balance}\n'
                for trans in self.get_transactions():
                    text += f'{trans["type"].lower()},{trans["amount"]},{trans["category"].lower()}\n'
                f.write(text)
            return True
        except:
            return False

    def load_data(self):
        try:
            with open('data.txt', 'r', encoding='UTF-8') as f:
                rows = f.readlines()
                data = [float(rows[0][rows[0].find(':')+1:]), []]
                rows.pop(0)
                for row in rows:
                    first_point, second_point = row.find(','), row.rfind(',')
                    data[1].append({'type': row[:first_point], 'amount': float(row[first_point+1:second_point-1]), 'category': row[second_point+1:]})
                self.__balance = data[0]
                self.__transactions = data[1]
            return True
        except:
            return False

    def run(self):
        try:
            print('Файл успешно загружен.' if self.load_data() else 'Возникли проблемы при загрузке файла, возможно он не существует или пуст.', end='\n\n')
            while (answer := int(input('Меню:\n1. Добавить доход/расход\n2. Показать баланс и транзакции\n3. Сохранить и выйти\nВведите номер команды: '))) and answer != 3:
                if answer == 1:
                    while (type := input('Введите тип операции (доход/расход): ').lower()) and type not in ['доход', 'расход']:
                        print('Да нет такого типа')
                    while (amount := float(input('Введите сумму: '))) and (self.get_balance() - amount >= 0 and type == 'расход'):
                        print('Да не может у тебя сумма быть текстом или расход превышать твой текущий баланс.')
                    transaction = {'type': type, 'amount': amount, 'category': input('Введите категорию: ')}
                    self.add_transaction(*transaction.values())
                    print(f'Добавлена операция: {transaction}\n')
                elif answer == 2:
                    transactions = self.get_transactions()
                    transactions_in_str = ''
                    if len(transactions) != 0:
                        for trans in transactions:
                            transactions_in_str += f'[{"+" if trans["type"].lower() == "доход" else "-"}] Тип: {trans["type"].capitalize()} | Сумма: {trans["amount"]} | Категория: {trans["category"]}\n'
                    else:
                        transactions_in_str = 'У вас ещё не было никаких операций.\n'
                    print(f'Баланс: {self.get_balance()}\n{transactions_in_str}')
                else:
                    print('Нет такого номера команды.\n')
            print('Данные успешно сохранены.' if self.save_data() else 'Возникла проблема при сохранения файла.')
        except ValueError:
            print('У ТЕБЯ ТОЛЬКО 3 КОМАНДЫ! ТОЛЬКО 3!')
            self.run()
        except RecursionError:
            print('ты совсем глупый?')
            self.run()