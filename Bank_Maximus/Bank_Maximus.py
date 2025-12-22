# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

"""
* Course Code  : AC51002 - Software Development
* Title   : Assignment 2 - Program 2 Banking application
* Developed By : Adiele Akachukwu
* Date Created : 29th November, 2024
*
* Bank Name - "Bank Maximus"
*
* 'Bank_Maximus' Python Application
"""

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Importing Libraries
import Banking ; # 'Banking' class
import os, sys, time, datetime, math  ; # Python libraries used in program

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Get the root directory for the location of python program
baseDirectory = os.path.dirname(os.path.abspath(__file__)) + "/Bank_Maximus/"
customersDirectory = baseDirectory + "/Customers/"
accountsDirectory = baseDirectory + "/Accounts/"
try:
    # Redundancy check to create directories if they do not exist
    os.makedirs(baseDirectory)
    os.makedirs(customersDirectory)
    os.makedirs(accountsDirectory)
except FileExistsError:
    # directory already exists
    pass

# Declaring global variables
currencySymbol = "£" ; returnVal = ''
todayDay = datetime.datetime.now().day  ; # Current day
todayMonth = datetime.datetime.now().month  ; # Current month
todayYear = datetime.datetime.now().year  ; # Current year

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Function to save bank account info to text files
def storeAccountInfo(accountObject):
    saveState = accountObject.saveAccountState(accountsDirectory)
    if (saveState):
        # Account updated successfully
        return accountObject
    else:
        # Failure in updating account data on text file
        print("\n***! Error: Account updated failed")
        return False

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Function to load bank account info from text files
def getAccountInfo(accountId):
    try:
        with open( accountsDirectory + accountId +".txt", "r", encoding="UTF-8" ) as openedFile:
            fileContent = openedFile.read()
            
            # Extract contents from file
            accountId, customerLoginId, accountType, currency, accountBalance, creationDate, accountStatus, \
                applyInterest, interestRate, overdraftAmount, mortgagePrincipal, mortgageTerm, repaymentAccount, \
                    mortgageInterestRate = fileContent.rstrip().split(",")
            
        if (accountType == '1') or (accountType == "savings account"):
            # Savings account
            accountObject = Banking.savingsAccount(accountId, customerLoginId, accountType, currency, accountBalance, creationDate, applyInterest)
            accountObject.accountStatus = accountStatus
            accountObject.interestRate = interestRate
        elif (accountType == '2') or (accountType == "current account"):
            # Current account
            accountObject = Banking.currentAccount(accountId, customerLoginId, accountType, currency, accountBalance, creationDate, applyInterest)
            accountObject.accountStatus = accountStatus
            accountObject.interestRate = interestRate
            accountObject.overdraftAmount = overdraftAmount
        elif (accountType == '3') or (accountType == "mortgage account"):
            # Mortgage account
            accountObject = Banking.mortgageAccount(accountId, customerLoginId, accountType, currency, accountBalance, creationDate, mortgagePrincipal, mortgageTerm, repaymentAccount)
            accountObject.accountStatus = accountStatus
            accountObject.mortgagePrincipal = mortgagePrincipal
            accountObject.mortgageTerm = mortgageTerm
            accountObject.repaymentAccount = repaymentAccount
            accountObject.mortgageInterestRate = mortgageInterestRate

        return accountObject
    except FileNotFoundError:
        # Handing possible exceptions
        return False

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Function to save customer info to text files
def storeCustomerInfo(customerObject):
    saveState = customerObject.saveCustomerState(customersDirectory)
    if (saveState):
        # Customer updated successfully
        return customerObject
    else:
        # Failure in updating customer data on text file
        print("\n***! Error: Customer updated failed")
        return False

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Function to load bank customer info from saved text files
def getCustomerInfo(customerLoginId):
    try:
        with open( customersDirectory + customerLoginId +".txt", "r", encoding="UTF-8" ) as openedFile:
            fileContent = openedFile.read()
            
            # Extract contents from file
            firstName, lastName, dateOfBirth, phone, email, occupation, customerLoginId, customerPassword, creationDate, accountsList, customerId = fileContent.rstrip().split(",")
            
            # Initializing object for customer class
            customerObject = Banking.customer(firstName, lastName, dateOfBirth, phone, email, occupation, customerLoginId, customerPassword, creationDate)
            customerObject.customerId = customerId
            customerObject.customerAccountsList = accountsList.split('|')
            
            return customerObject
    except FileNotFoundError:
        # Handing possible exceptions
        return False

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Function to view the state of all account for a bank customer
def viewAllAccountsForCustomer(customerObject):
    for account in customerObject.customerAccountsList:
        print("\n----------------------------------")
        accountId = account.split(".txt")[0]        
        accountObject = getAccountInfo(accountId)   ; # initializing account object for selected account
        if (returnVal != False):
            # Displaying the state of the account
            print(accountObject)
        else:
            print(f"\n***! Error: Account not found - {accountId}")
        print("----------------------------------")
            
# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Function to launch the account menu
def accountMenu(accountId):
    accountObject = getAccountInfo(accountId)   ; # initializing account object for selected account
    
    print("\n\n----------------------------------")
    print("Account Menu")
    print("----------------------------------\n")
    
    if (accountObject.accountType != "mortgage account"):
        # Generic account menu
        print("1 - View account balance")
        print("2 - Make a deposit")
        print("3 - Make a withdrawal")
        print("4 - View account state")
        print("# - Return to customer menu \n \n")
        inputValue = input(">>> ")
    else:
        # Variant of account menu for a mortgage account
        print("1 - View account state")
        print("# - Return to customer menu \n \n")
        inputValue = input(">>> ")
        
        if (inputValue == '1'):
            inputValue = '4'
        elif (inputValue == '#'):
            inputValue = '#'
        else:
            inputValue = ''
    
    try:
        match inputValue:
            # Handling multiple cases for inputs provided
            case '1':
                print("\n----------------------------------\n")
                accountObject = getAccountInfo(accountId)   ; # initializing account object for selected account
                if (accountObject != False):
                    accountBalance = accountObject.accountBalance
                    print(f"Your account balance is {currencySymbol}{accountBalance}")
                    print("----------------------------------")
                else:
                    print("\n***! Error: Account not found")
                
                time.sleep(1)   ; # System pause for 1 second
                accountMenu(accountId)  ; # Display account menu
                        
            case '2':
                print("\n----------------------------------\n")
                print("Enter amount to deposit (or '#' to return): ")
                inputValue = input(">>> ")
                
                try:
                    if (inputValue == '#'):
                        # Return to previous menu
                        pass
                    else:
                        try:
                            depositAmount = float(inputValue)                
                            accountObject = getAccountInfo(accountId)   ; # initializing account object for selected account
                            returnVal = accountObject.deposit(depositAmount)
                            if (returnVal == True):
                                # Deposit successful
                                print(f"\nDeposit of {currencySymbol}{depositAmount} was successful")
                                print(f"\nNew account balance is {accountObject.accountBalance}")

                                storeAccountInfo(accountObject)     ; # Update account data to text file
                        except ValueError:
                            # Handing possible exceptions
                            print("Invalid amount entered")
                except IndexError:
                    # Handing possible exceptions
                    print("\n***! Error: Invalid input")
                    
                time.sleep(1)   ; # System pause for 1 second
                accountMenu(accountId)  ; # Display account menu
                
            case '3':
                print("\n----------------------------------\n")
                print("Enter amount to withdraw (or '#' to return): ")
                inputValue = input(">>> ")
                
                try:
                    if (inputValue == '#'):
                        # Return to previous menu
                        pass
                    else:
                        try:
                            withdrawalAmount = float(inputValue)
                            accountObject = getAccountInfo(accountId)   ; # initializing account object for selected account
                            returnVal = accountObject.withdraw(withdrawalAmount)
                            if ( returnVal == True):
                                print(f"\nWithdrawal of {currencySymbol}{withdrawalAmount} was successful")
                                print(f"\nNew account balance is {accountObject.accountBalance}")
                                
                                storeAccountInfo(accountObject)     ; # Update account data to text file
                        except ValueError:
                            # Handing possible exceptions
                            print("Invalid amount entered")
                except IndexError:
                    # Handing possible exceptions
                    print("\n***! Error: Invalid input")
                
                time.sleep(1)   ; # System pause for 1 second
                accountMenu(accountId)  ; # Display account menu
                
            case '4':
                print("\n----------------------------------\n")
                accountObject = getAccountInfo(accountId)   ; # initializing account object for selected account
                if (accountObject != False):
                    # Displaying the state of the account
                    print(accountObject)
                    print("----------------------------------")
                else:
                    print("\n***! Error: Account not found")
                
                time.sleep(1)   ; # System pause for 1 second
                accountMenu(accountId)  ; # Display account menu

            case '#':
                # Return to previous menu
                print("\n----------------------------------\n")
                time.sleep(1)   ; # System pause for 1 second
            
            case _:
                print("\n***! Error: Invalid Input\n")
                time.sleep(1)   ; # System pause for 1 second
                accountMenu(accountId)  ; # Display account menu
    except IndexError:
        # Handing possible exceptions
        print("\n***! Error: Invalid input")

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Function to create a new account for a bank customer
def createAccount(customerObject):
    print("\n----------------------------------")
    print("\nTo open a new account, follow the below prompts and provide accurate details: ")
    time.sleep(1)   ; # System pause for 1 second
    
    accountStatus = ''
    
    existingAccountsList = next(os.walk(accountsDirectory), (None, None, []))[2]  # walking through the directory contents
    accountId = '213' + str(len(existingAccountsList) + 1).zfill(5)     ; # Generating unique id for account
    
    customerLoginId = customerObject.customerLoginId
    currency = "GBP"
    accountBalance = 0
    creationDate = str(todayDay) +'/'+ str(todayMonth) +'/'+ str(todayYear) ; # Formating the date

    print("\nEnter code to select account type:")
    print("   1 - Savings account")
    print("   2 - Current account")
    print("   3 - Mortgage account")
    accountType = input(">>> ")
    
    try:
        if (accountType == '1'):
            # Creating savings account
            print("\n----------------------------------")
            applyInterest = input("\nWould you like apply interest? (Y/N): ")
            
            # Initializing object for savingsAccount class
            accountObject = Banking.savingsAccount(accountId, customerLoginId, accountType, currency, accountBalance, creationDate, applyInterest)
            accountStatus = accountObject.accountStatus
        elif (accountType == '2'):
            # Creating Current account
            print("\n----------------------------------")
            applyInterest = input("\nWould you like apply interest? (Y/N): ")
            
            # Initializing object for currentAccount class
            accountObject = Banking.currentAccount(accountId, customerLoginId, accountType, currency, accountBalance, creationDate, applyInterest)
            accountStatus = accountObject.accountStatus
        elif (accountType == '3'):
            # Creating mortgage account
            print("\n----------------------------------")
            
            # Check if customer has existing accounts
            if ( len(customerObject.customerAccountsList) != 0):
                accountCount = 0 ; hasCurrentAccount = '' ; currentAccountsList = []
                
                for account in customerObject.customerAccountsList:
                # Looping through list of existing accounts
                    accountObject = getAccountInfo(account)
                    if (accountObject.accountType == "current account"):
                        # Building a new list for only the customers 'current accounts'
                        currentAccountsList.append(customerObject.customerAccountsList[accountCount])
                        hasCurrentAccount = 'Y' ; # Flag to set if customer has a current account
                    accountCount += 1   ; # incrementing the loop variable
                
                if (hasCurrentAccount == 'Y'):
                    # Execute when a current account exists
                    print("\nSelect one of the below current accounts as your 'Repayment Account' : \n")
                    accountCount = 1
                    for account in currentAccountsList:
                        # Looping through list of current accounts
                        print(f"{accountCount} - {account}")    ; # Display current accounts
                        accountCount += 1   ; # incrementing the loop variable
                        
                    print("\nEnter corresponding code to select an account : ")
                    inputValue = input(">>> ")
                    
                    try:
                        repaymentAccount = currentAccountsList[int(inputValue) - 1]
                    except IndexError:
                        # Handing possible exceptions
                        print("\n***! Error: Invalid input")
                else:
                    print("\n***! Kindly note, you must have at least one current account with us to proceed.")
                    print("\n***! Error: Account creation failed")
                    time.sleep(1)   ; # System pause for 1 second
                    return False
                
                if (repaymentAccount != ''):
                    mortgagePrincipal = input("\nEnter mortgage principal amount: ")
                    mortgageTerm = input("\nEnter mortgage term (years): ")
                    
                    # Initializing object for mortgageAccount class
                    accountObject = Banking.mortgageAccount(accountId, customerLoginId, accountType, currency, accountBalance, creationDate, mortgagePrincipal, mortgageTerm, repaymentAccount)
                    accountStatus = accountObject.accountStatus
                    
                    monthlyRepaymentAmount = math.trunc(100 * (accountObject.calculateRepaymentAmount() / 12) ) / 100   ; # formatting the amount value to 2 decimal points
                    print(f"\n\nNote: A monthly capital repayment amount of '{currencySymbol}{monthlyRepaymentAmount}' \nwould be deducted from your repayment account ({accountObject.repaymentAccount})")

                else:
                    print("\n***! Kindly note, you must have at least an existing current account with us to proceed.")
                    print("\n***! Error: Account creation failed")
                    time.sleep(1)   ; # System pause for 1 second
                    return False
                
            else:
                print("\n***! Kindly note, you must have at least an existing current account with us to proceed.")
                print("\n***! Error: Account creation failed")
                time.sleep(1)   ; # System pause for 1 second
                return False
        else:
            print("\n***! Error: Account creation failed")
            return False
    
    except IndexError:
        # Handing possible exceptions
        print("\n***! Error: Invalid input")
    
    
    if (accountStatus == "active"):
        returnVal = storeAccountInfo(accountObject)     ; # Update account data to text file
        time.sleep(1)   ; # System pause for 1 second
        return returnVal
    else:
        print("\n***! Error: Account creation failed")
        time.sleep(1)   ; # System pause for 1 second
        return False

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Function to launch the admin menu
def adminMenu():
    print("\n\n----------------------------------")
    print("Admin Menu")
    print("----------------------------------\n")
    print("1 - View Customers")
    print("2 - View Accounts")
    print("# - Return to Home menu \n \n")
    inputValue = input(">>> ")
    
    try:
        match inputValue:
            # Handling multiple cases for inputs provided
            case '1':
                print("\n----------------------------------\n")
                customersCount = 1
                fileNames = next(os.walk(customersDirectory), (None, None, []))[2]  # walking through the directory contents
                if (fileNames):
                    print("Customers: ")
                    for fileName in fileNames:
                        # Looping to display customer ids
                        customerLoginId = fileName.split(".txt")[0]
                        print(f"{customersCount} - {customerLoginId}")
                        customersCount += 1   ; # incrementing the loop variable 
                    
                    print("\nEnter corresponding code for your customer (or '#' to return): ")
                    inputValue = input(">>> ")
                    try:
                        if (inputValue == '#'):
                            # Return to previous menu
                            pass
                        else:
                            returnVal = getCustomerInfo(fileNames[int(inputValue) - 1].split(".txt")[0])   ; # initializing customer object for customer account
                            if (returnVal != False):
                                # Display state of customer selected
                                print("\n----------------------------------")
                                print(returnVal)
                            else:
                                print("\n***! Error: Customer file not found")
                    except IndexError:
                        # Handing possible exceptions
                        print("\n***! Error: Invalid input")
                else:
                    print("\n***! Error: No customer file found")

                print("\n----------------------------------")
                time.sleep(1)   ; # System pause for 1 second
                adminMenu()  ; # Display admin menu
                
            case '2':
                print("\n----------------------------------\n")
                accountsCount = 1
                fileNames = next(os.walk(accountsDirectory), (None, None, []))[2]  # walking through the directory contents
                if (fileNames):
                    print("Accounts:")
                    for fileName in fileNames:
                        # Looping to display account ids
                        accountId = fileName.split(".txt")[0]
                        print(f"{accountsCount} - {accountId}")
                        accountsCount += 1   ; # incrementing the loop variable 
                    
                    print("\nEnter corresponding code for your account (or '#' to return): ")
                    inputValue = input(">>> ")
                    try:
                        if (inputValue == '#'):
                            # Return to previous menu
                            pass
                        else:
                            returnVal = getAccountInfo(fileNames[int(inputValue) - 1].split(".txt")[0])
                            if (returnVal != False):
                                # Display state of account selected
                                print("\n----------------------------------")
                                print(returnVal)
                            else:
                                print("\n***! Error: Account not found")
                    except IndexError:
                        # Handing possible exceptions
                        print("\n***! Error: Invalid input")
                else:
                    print("\n***! Error: No account file found")

                
                print("\n----------------------------------")
                time.sleep(1)   ; # System pause for 1 second
                adminMenu()  ; # Display admin menu

            case '#':
                # Return to previous menu
                print("\n----------------------------------\n")
                time.sleep(1)   ; # System pause for 1 second
                homeMenu()  ; # Display home menu
            
            case _:
                print("\n***! Error: Invalid Input\n")
                time.sleep(1)   ; # System pause for 1 second
                adminMenu()  ; # Display admin menu
    except IndexError:
        # Handing possible exceptions
        print("\n***! Error: Invalid input")

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Function to initiate login for bank admin
def adminLogin():
    print("\n----------------------------------")
    idInput = input("Enter Admin ID: ")
    passwordInput = input("Enter Admin password: ")
    
    try:
        with open( baseDirectory +"admin.txt", "r", encoding="UTF-8" ) as openedFile:
            fileContent = openedFile.read()
            
            # Extract contents from file
            adminName, adminPassword = fileContent.rstrip().split(",")
            
            if (idInput.lower() == adminName.lower()) and (adminPassword.lower() == passwordInput.lower()):
                adminMenu()  ; # Display admin menu
            else:
                print("\n***! Error: Invalid Credentials")
                time.sleep(1)   ; # System pause for 1 second
                return False
    except FileNotFoundError:
        # Handing possible exceptions
        print("\n***! Error: Admin profile not setup")
        print("Kindly try again\n")
        
        # Redundancy to setup admin profile
        with open( baseDirectory +"admin.txt", "w", encoding="UTF-8" ) as openedFile:
            openedFile.write("admin,admin123")  ; # Write to update on the file
        
        time.sleep(1)   ; # System pause for 1 second    
        return False

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Function to launch the customer menu
def customerMenu(customerFile):
    # Extract contents from file
    firstName, lastName, dateOfBirth, phone, email, occupation, customerLoginId, customerPassword, creationDate, accountsList, customerId = customerFile.rstrip().split(",")
    
    # Initializing object for customer class
    loggedInCustomer = Banking.customer(firstName, lastName, dateOfBirth, phone, email, occupation, customerLoginId, customerPassword, creationDate)

    loggedInCustomer.customerId = customerId
    
    if (accountsList == ''):
        # For customers without existing account(s)
        loggedInCustomer.customerAccountsList = ''
    else:
        # For customers with existing account(s)
        loggedInCustomer.customerAccountsList = accountsList.split('|')
    numberOfAccounts = len(loggedInCustomer.customerAccountsList)
    
    print("\n\n----------------------------------")
    print(f"Hello {loggedInCustomer.firstName.title()},")
    print("----------------------------------\n")
    print("1 - Accounts list")
    print("2 - Open a new account")
    print("3 - View state of all accounts")
    print("# - Return to Home menu \n \n")
    inputValue = input(">>> ")
    
    try:
        match inputValue:
            # Handling multiple cases for inputs provided
            case '1':
                print("\n----------------------------------\n")
                if ( numberOfAccounts != 0):
                    print("Accounts:")
                    accountCount = 1
                    for account in loggedInCustomer.customerAccountsList:
                        # Loop through list and display existing accounts
                        print(f"{accountCount} - {account}")
                        accountCount += 1   ; # incrementing the loop variable
                    print("\nEnter corresponding code for your account (or '#' to return): ")
                    inputValue = input(">>> ")
                    try:
                        if (inputValue == '#'):
                            # Return to previous menu
                            pass
                        else:
                            # Launch account menu for the account selected
                            returnVal = accountMenu(loggedInCustomer.customerAccountsList[int(inputValue) - 1])
                    except IndexError:
                        # Handing possible exceptions
                        print("\n***! Error: Invalid input")
                else:
                    print("\n***! Error: No account file found")
                
                time.sleep(1)   ; # System pause for 1 second
                customerMenu(customerFile)  ; # Display customer menu
                
            case '2':
                print("\n----------------------------------\n")
                returnVal = createAccount(loggedInCustomer) ; # Launch function to create new account
                if(returnVal != False):
                    print("\nAccount created successfully\n")
                    
                    if ( numberOfAccounts == 0):
                        loggedInCustomer.customerAccountsList = returnVal.accountId
                    else:
                        loggedInCustomer.customerAccountsList = accountsList +'|'+ returnVal.accountId
                    
                    storeCustomerInfo(loggedInCustomer)     ; # Update customer data to text file
                    with open( customersDirectory + loggedInCustomer.customerLoginId +".txt", "r", encoding="UTF-8" ) as openedFile:
                        fileContent = openedFile.read()
                        time.sleep(1)   ; # System pause for 1 second
                        customerMenu(fileContent)  ; # Display customer menu
                else:
                    # Account creation failed, return to customer menu
                    time.sleep(1)   ; # System pause for 1 second
                    customerMenu(customerFile)  ; # Display customer menu
                
            case '3':
                # View state of all accounts for this customer
                print("\n----------------------------------\n")
                if ( numberOfAccounts != 0):
                    viewAllAccountsForCustomer(loggedInCustomer)
                else:
                    # Error when customer has no account to view
                    print("\n***! Error: No account file found")
                
                time.sleep(1)   ; # System pause for 1 second
                customerMenu(customerFile)  ; # Display customer menu

            case '#':
                # Return to previous menu
                print("\n----------------------------------\n")
                time.sleep(1)   ; # System pause for 1 second
                homeMenu()
            
            case _:
                print("\n***! Error: Invalid Input\n")
                time.sleep(1)   ; # System pause for 1 second
                customerMenu(customerFile)  ; # Display customer menu
    except IndexError:
        # Handing possible exceptions
        print("\n***! Error: Invalid input")

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Function to initiate login for the bank customer
def customerLogin():
    print("\n\n----------------------------------")
    idInput = input("Enter your Customer Login ID: ")
    passwordInput = input("Enter your Customer password: ")

    try:
        # Check if customer login exists
        with open( customersDirectory + idInput +".txt", "r", encoding="UTF-8" ) as openedFile:
            fileContent = openedFile.read()
            
            # Extract contents from file
            firstName, lastName, dateOfBirth, phone, email, occupation, customerLoginId, customerPassword, creationDate, accountsList, customerId = fileContent.rstrip().split(",")
            
            # Check if password provided is correct
            if (customerPassword == passwordInput):
                customerMenu(fileContent)  ; # Display customer menu
            else:
                print("\n***! Error: Invalid password")
                return False
    except FileNotFoundError:
        # Handing possible exceptions
        print("\n***! Error: Customer not found")
        return False

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Function to register a new customer
def registerCustomer():
    print("\n\n----------------------------------")
    print("Customer Registration")
    print("----------------------------------\n")
    
    print("\n----------------------------------")
    print("\nTo register as a new customer, follow the below prompts and provide accurate details: ")
    print("Note: All information are mandatory, hence all input are required \n")
    print("----------------------------------\n")
    time.sleep(1)   ; # System pause for 1 second
    
    registrationStatus = ''
    
    # Collect user inputs for details required in creating a new customer
    customerLoginId = input("\nEnter preferred log in ID: ")
    returnVal = getCustomerInfo(customerLoginId.lower())   ; # initializing customer object for customer account
    
    # Check if login id provided already exists
    if (returnVal != False):
        print("\n***! Error: This id already exists")
    else:
        firstName = input("\nEnter first name: ")
        lastName = input("\nEnter last name: ")
        
        dobDay = int(input("\nEnter Date of Birth - Day: "))
        # Check for valid day input
        if ( (dobDay < 1) or (dobDay > 31) ):
            print("\n***! Error: Invalid day inputted")
        else:
            dobMonth = int(input("\nEnter Date of Birth - Month: "))
            # Check for valid month input
            if ( (dobMonth < 1) or (dobMonth > 12) ):
                print("\n***! Error: Invalid Month inputted")
            else:
                dobYear = int(input("\nEnter Date of Birth - Day: "))
                # Check for valid year input
                if ( (len(str(dobYear)) < 0) or (len(str(dobYear)) > 4) or (dobYear > todayYear) ):
                    print("\n***! Error: Invalid year inputted")
                else:
                    dateOfBirth = str(dobDay) +'/'+ str(dobMonth) +'/'+ str(dobYear)
                    
                    phone = input("\nEnter phone: ")
                    email = input("\nEnter email: ")
                    # Check for valid mail input
                    if (email.count('@') != 1):
                        print("\n***! Error: Invalid email inputted")
                    else:
                        occupation = input("\nEnter occupation: ")
                        creationDate = str(todayDay) +'/'+ str(todayMonth) +'/'+ str(todayYear) ; # Formating the date
                        customerPassword = input("\nEnter preferred log in Password: ")
                        
                        if ( (firstName != '') and (lastName != '') and (dateOfBirth != '') and (phone != '') and (email != '') and (occupation != '') and (customerLoginId != '') and (customerPassword != '') and (creationDate != '') ):
                            # Initializing object for customer class
                            loggedInCustomer = Banking.customer(firstName, lastName, dateOfBirth, phone, email, occupation, customerLoginId, customerPassword, creationDate)
                            loggedInCustomer.generateCustomerId(customersDirectory)
                            registrationStatus = loggedInCustomer.status
                        else:
                            print("\n***! Empty information provided among inputs")
                            print("\n***! Error: Customer creation failed")
                
    if (registrationStatus == "Created"):
        fileName = customersDirectory  + loggedInCustomer.customerLoginId +".txt"  ; # File name for customer file
        
        fileContent = loggedInCustomer.firstName + "," + loggedInCustomer.lastName + "," + loggedInCustomer.dateOfBirth \
            + "," + loggedInCustomer.phone + "," + loggedInCustomer.email + "," + loggedInCustomer.occupation \
                + "," + loggedInCustomer.customerLoginId + "," + loggedInCustomer.customerPassword \
                    + "," + loggedInCustomer.creationDate + "," + str(loggedInCustomer.customerAccountsList) + "," + loggedInCustomer.customerId
        try:
            with open( fileName, "w", encoding="UTF-8" ) as openedFile:
                openedFile.write(fileContent)  ; # Write to update on the file
                print("\nCustomer registered successfully\n")
        except FileNotFoundError:
            # Handing possible exceptions
            print("\n***! Error: Customer creation failed")
    else:
        print("\n***! Error: Customer creation failed")
    time.sleep(1)   ; # System pause for 1 second

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Function to launch the home menu 
def homeMenu():
    print("\n\n----------------------------------")
    print("Welcome to 'Bank Maximus'")
    print("----------------------------------\n")
    print("1 - Login as existing customer")
    print("2 - Register as a new customer")
    print("3 - Switch to Admin Menu")
    print("# - Exit Application \n \n")
    inputValue = input(">>> ")
    
    try:
        match inputValue:
            # Handling multiple cases for inputs provided
            case '1':
                customerLogin() ; # Launch customer login
                time.sleep(1)   ; # System pause for 1 second
                homeMenu() ; # Display home menu
                
            case '2':
                registerCustomer() ; # Display 'register customer' section
                time.sleep(1)   ; # System pause for 1 second
                homeMenu() ; # Display home menu
                
            case '3':
                adminLogin() ; # Launch admin login
                time.sleep(1)   ; # System pause for 1 second
                homeMenu() ; # Display home menu
            
            case '#':
                # Exit program
                print("\n----------------------------------")
                print("\n***! Exiting !***\n")
                print("----------------------------------\n")
                time.sleep(2)   ; # System pause for 2 seconds
                sys.exit()  ; # Exit program
            
            case _:
                print("\n***! Error: Invalid Input\n")
                time.sleep(1)   ; # System pause for 1 second
                homeMenu() ; # Display home menu
    except IndexError:
        # Handing possible exceptions
        print("\n***! Error: Invalid input")

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Launch the home menu
homeMenu()

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------
