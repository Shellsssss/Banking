##############################
# ₹₹₹₹₹ BANKING SYSTEM ₹₹₹₹₹ #
##############################

import mysql.connector
import datetime

db = mysql.connector.connect(host = 'localhost', user = 'root', password = 'catsheLL.999', database = 'banking')
cur = db.cursor()

def id_generator(prev_id, attribute_name, table_name):
    sql = 'select max(%s) from %s'% (attribute_name, table_name)
    cur.execute(sql)
    for i in cur:
        if i[0] != None:
            prev_id = i[0]
    new_id = prev_id + 1
    return new_id

def id_check(table_name, attribute, id):
    sql = 'select * from %s where %s = %s' % (table_name, attribute, id)
    cur.execute(sql)
    row = None
    for i in cur:
        row = i
    return row

def password_check(acc_id, password):
    sql = 'select * from accounts where acc_id = %s'% acc_id
    cur.execute(sql)
    for i in cur:
        if i[-1] == password:
            print(i[-2])
        else:
            print('Password incorrect')

def get_acc_holder_id(acc_id):
    sql = 'select user_id from accounts where acc_id = %s'% acc_id
    cur.execute(sql)
    for i in cur:
        user_id = i[0]
        return user_id

def transaction(ledger_id, acc_id, user_id, date, txn, deposit, withdrawal, new_balance):
    try:
        ledger_sql = 'insert into ledger values("%s", "%s", "%s", "%s", "%s", %s, %s, %s)'% (ledger_id, acc_id, user_id, date, txn, deposit, withdrawal, new_balance)
        acc_sql = 'update accounts set balance = %s where acc_id = %s'% (new_balance, acc_id)
        cur.execute(ledger_sql)
        cur.execute(acc_sql)
        db.commit()
    except Exception as e:
        print("Error occured: ", e)
        print('Transaction failed.')
        return
    # try:

    #     db.commit()
    # except Exception as e:
    #     print("Error occured: ", e)
    else:
        print('Transaction successful.')

# to see list of tables
def list_tables():
    sql = 'show tables'
    cur.execute(sql)
    for i in cur:
        print(i)

# to create a user
def create_user_helper():
    new_id = id_generator(1500, 'user_id', 'customer_profile')
    today = datetime.date.today()

    name = input('Enter name: ')
    address = input('Enter address: ')
    dob = input('Enter date of birth (YYYY-MM-DD): ')
    gender = input('Enter gender (M/F/other): ').upper()
    aadhar = input('Enter aadhar number: ')
    pan = input('Enter PAN number: ')

    create_user(new_id, name, today, address, dob, gender, aadhar, pan)

def create_user(id, name, regd_date, address, dob, gender, aadhar, pan):
    try:
        sql = 'insert into customer_profile values("%s", "%s", "%s", "%s", "%s","%s","%s","%s")' % (id, name, regd_date, address, dob, gender, aadhar, pan)
        cur.execute(sql)
        db.commit()
    except Exception as e:
        print('Error occured: ', e)
    else:
        print('User created successfully.')
        print('Your User Id is:', id)
        read_user(id)

def read_user_helper():
    user_id = int(input('Enter User ID: '))
    row = id_check('customer_profile', 'user_id', user_id)
    if row == None:
        print('This User ID does not exist. Please enter a valid User ID.')
        return
    read_user(user_id)

def read_user(id):
    row = id_check('customer_profile', 'user_id', id)
    print(row)

# to create an account
def create_acc_helper():
    user_id = int(input('Enter User ID: '))
    row = id_check('customer_profile', 'user_id', user_id)
    if row == None:
        print('This User ID does not exist. Please enter a valid User ID.')
        return
    
    new_id = id_generator(2000, 'acc_id', 'accounts')
    today = datetime.date.today()

    type = input('Enter type of account (sb/ca/fd/rd): ')
    balance = int(input('Enter opening balance: '))
    password = input('Enter password (maximum 50 characters): ')

    create_acc(new_id, user_id, type, today, balance, password)

def create_acc(acc_id, user_id, type, date, balance, password):
    try:
        sql = 'insert into accounts values("%s", "%s", "%s", "%s", "%s", "%s")' % (acc_id, user_id, type, date, balance, password)
        cur.execute(sql)
        db.commit()
    except Exception as e:
        print("Error occured: ", e)
    else:
        print('Account created successfully.')
        print('Your Account ID is:', acc_id)
        read_acc(acc_id)

def read_acc_helper():
    acc_id = int(input('Enter your Account ID: '))
    row = id_check('accounts', 'acc_id', acc_id)
    if row == None:
        print('This Account ID does not exist. Please enter a valid Account ID.')
        return
    read_acc(acc_id)

# TODO: show user details also
def read_acc(acc_id):
    sql = 'select * from accounts where acc_id = "%s"' % (acc_id,)
    cur.execute(sql)
    for i in cur:
        print(i)

# To show accounts of a user
def read_user_acc():
    user_id = int(input('Enter User ID: '))
    row = id_check('customer_profile', 'user_id', user_id)
    if row == None:
        print('This User ID does not exist. Please enter a valid User ID.')
        return
    
    sql = 'select * from accounts where user_id = %s'% user_id
    cur.execute(sql)
    flag = 0
    for i in cur:
        flag = 1
        print(i)
    
    if flag == 0:
        print('No accounts found for given user.') 

# To check balance of an account
def check_balance_helper():
    acc_id = int(input('Enter your Account ID: '))
    row = id_check('accounts', 'acc_id', acc_id)
    if row == None:
        print('This Account ID does not exist. Please enter a valid Account ID.')
        return
    
    print('The balance for account number %s is: ₹%s' % (acc_id, check_balance(acc_id)))
    
def check_balance(id):
    sql = 'select balance from accounts where acc_id = %s'% id
    cur.execute(sql)
    for i in cur:
        balance = i[0]
        return balance

# To deposit cash in an account
def cash_deposit():
    acc_id = int(input("Enter Account's ID for cash deposit: "))
    row = id_check('accounts', 'acc_id', acc_id)
    if row == None:
        print('This Account ID does not exist. Please enter a valid Account ID.')
        return

    deposit = int(input('Enter amount to be deposited (If you wish to cancel, enter "0"): '))
    while deposit == 0:
        confirmation = input('Do you wish to cancel? yes/no: ')
        if confirmation.upper() == 'YES':
            return
        else: 
            deposit = int(input('Enter amount to be deposited: '))

    ledger_id =  id_generator(100, 'ledger_id', 'ledger')
    user_id = get_acc_holder_id(acc_id)
    today = datetime.date.today()
    txn = 'deposit'
    withdrawal = 'null'
    balance = check_balance(acc_id) + deposit

    transaction(ledger_id, acc_id, user_id, today, txn, deposit, withdrawal, balance)

# To withdraw cash from an account
def cash_withdraw():
    acc_id = int(input("Enter Account's ID for cash withdrawal: "))
    row = id_check('accounts', 'acc_id', acc_id)
    if row == None:
        print('This Account ID does not exist. Please enter a valid Account ID.')
        return
    
    withdrawal = int(input('Enter amount to be withdrawn (If you wish to cancel, enter "0"): '))

    while withdrawal == 0:
        confirmation = input('Do you wish to cancel? yes/no: ')
        if confirmation.upper() == 'YES':
            return
        else: 
            withdrawal = int(input('Enter amount to be withdrawn: '))

    old_balance = check_balance(acc_id)
    if old_balance < withdrawal:
        print('Insufficient balance.')
        return

    ledger_id =  id_generator(100, 'ledger_id', 'ledger')
    user_id = get_acc_holder_id(acc_id)
    today = datetime.date.today()
    txn = 'withdrawal'
    deposit = 'null'
    new_balance = old_balance - withdrawal

    transaction(ledger_id, acc_id, user_id, today, txn, deposit, withdrawal, new_balance)

# To transfer from one account to another
def transfer():
    withdrawal_id = int(input('Enter Account ID from which cash is to be withdrawn: '))
    row = id_check('accounts', 'acc_id', withdrawal_id)
    if row == None:
        print('This Account ID does not exist. Please enter a valid Account ID.')
        return

    deposit_id = int(input('Enter Account ID to which cash is to be deposited: '))
    while deposit_id == withdrawal_id:
        print('Cannot transfer funds to the same account')
        deposit_id = int(input('Enter Account ID to which cash is to be deposited: '))
    
    row = id_check('accounts', 'acc_id', deposit_id)
    if row == None:
        print('This Account ID does not exist. Please enter a valid Account ID.')
        return
    
    amount = int(input('Enter amount to be withdrawn (If you wish to cancel, enter "0"): '))

    while amount == 0:
        confirmation = input('Do you wish to cancel? yes/no: ')
        if confirmation.upper() == 'YES':
            return
        else: 
            amount = int(input('Enter amount to be withdrawn: '))

    old_balance_deposit = check_balance(deposit_id)
    old_balance_withdrawal = check_balance(withdrawal_id)
    if old_balance_withdrawal < amount:
        print('Insufficient balance.')
        return
    
    ledger_id_withdrawal = id_generator(100, 'ledger_id', 'ledger')
    ledger_id_deposit = ledger_id_withdrawal + 1
    user_id_withdrawal = get_acc_holder_id(withdrawal_id)
    user_id_deposit = get_acc_holder_id(deposit_id)
    txn_withdrawal = 'withdrawal'
    txn_deposit = 'deposit'
    deposit = 'null'
    withdrawal = 'null'
    new_balance_withdrawal = old_balance_withdrawal - amount
    new_balance_deposit = old_balance_deposit + amount
    today = datetime.date.today()

    transaction(ledger_id_withdrawal, withdrawal_id, user_id_withdrawal,
                 today, txn_withdrawal, deposit, amount, 
                 new_balance_withdrawal)
    transaction(ledger_id_deposit, deposit_id, user_id_deposit, 
                today, txn_deposit, amount, withdrawal, 
                new_balance_deposit)

# To check the activity of an account
def acc_activity():
    acc_id = int(input("Enter Account ID: "))
    row = id_check('accounts', 'acc_id', acc_id)
    if row == None:
        print('This Account ID does not exist. Please enter a valid Account ID.')
        return
    
    sql = 'select * from ledger where acc_id = %s'% acc_id
    cur.execute(sql)
    for i in cur:
        print(i)

def bank():
    print('1. Create User.')
    print('2. Create Account.')
    print("3. Show User's details.")
    print("4. Show Account's details.")
    print('5. Show accounts linked to a user.')
    print('6. Show Passbook of an Account.')
    print('7. Check balance of an Account.')
    print('8. Cash Deposit.')
    print('9. Cash Withdrawal.')
    print('10. Transfer transaction.')
    print('11. EXIT')
    print()

    choice = int(input('Choose a number: '))

    match choice:
        case 1:
            create_user_helper()
        case 2:
            create_acc_helper()
        case 3:
            read_user_helper()
        case 4:
            read_acc_helper()
        case 5:
            read_user_acc()
        case 6:
            acc_activity()
        case 7:
            check_balance_helper()
        case 8:
            cash_deposit()
        case 9:
            cash_withdraw()
        case 10:
            transfer()
        case 11:
            return 0
        case default:
            print('Please enter a valid number.')
    
    print()
    print()
    return 1

flag = 1
while flag:
    try:
        flag = bank()
    except Exception as e:
        print('Error occurred: ', e)


print('Thank you for banking with us.')