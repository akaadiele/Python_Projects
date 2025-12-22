# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

"""
* Course Code  : AC51002 - Software Development
* Title   : Assignment 2 - Program 2 Banking application
* Developed By : Adiele Akachukwu
* Date Created : 29th November, 2024
*
* Bank Name - Bank Maximus
*
* 'Banking' Class File
"""

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Importing Libraries
import os, math  ; # Python libraries used in program

# Declaring global variables
currencySymbol = "£"

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
class customer():
    # Function to define what happens when a new object is created for this class
    def __init__(self, firstName, lastName, dateOfBirth, phone, email, occupation, customerLoginId, customerPassword, creationDate):
        # Initializing class 'self' variables
        self.firstName = firstName.lower()
        self.lastName = lastName.lower()
        self.dateOfBirth = dateOfBirth
        self.phone = phone
        self.email = email
        self.occupation = occupation.lower()
        self.customerLoginId = customerLoginId.lower()
        self.customerPassword = customerPassword
        self.creationDate = creationDate
        
        self.status = "Created"
        self.customerAccountsList = ''

    # Generating a unique id for bank customer 
    def generateCustomerId(self, customersDirectory):
        existingCustomersList = next(os.walk(customersDirectory), (None, None, []))[2]  # walking through the directory contents
        self.customerId = '1' + str(len(existingCustomersList) + 1).zfill(5)
        
    # Saving customer data to text file
    def saveCustomerState(self, customersDirectory):
        fileName = customersDirectory  + self.customerLoginId +".txt"  ; # File name for customer file
        
        fileContent = self.firstName + "," + self.lastName + "," + self.dateOfBirth \
            + "," + self.phone + "," + self.email + "," + self.occupation \
                + "," + self.customerLoginId + "," + self.customerPassword \
                    + "," + self.creationDate + "," + str(self.customerAccountsList) + "," + self.customerId
        try:
            with open( fileName, "w", encoding="UTF-8" ) as openedFile:
                openedFile.write(fileContent)  ; # Write to update on the file
                return True
        except FileNotFoundError:
            # Handing possible exceptions
            return False
            
    # Function to override the '__str__' function
    def __str__(self):
        # output = "\nHello " + self.firstName.title() +", here are your details: \n\n"
        output = "\nCustomer ID: " + str(self.customerId) 
        output += "\nName: " + self.firstName.title() +' '+ self.lastName.title() 
        output += "\nDate of Birth: " + self.dateOfBirth 
        output += "\nPhone: " + self.phone 
        output += "\nEmail: " + self.email 
        output += "\nOccupation: " + self.occupation.title() 
        output += "\nLogin Id: " + self.customerLoginId 
        output += "\nJoined: " + self.creationDate 
        output += "\nAccounts: " + str(self.customerAccountsList) 
        output += "\n"
        
        return output

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

class account():
    # Function to define what happens when a new object is created for this class
    def __init__(self, accountId, customerLoginId, accountType, currency, accountBalance, creationDate):
        # Initializing class 'self' variables
        self.accountId = accountId
        self.customerLoginId = customerLoginId
        self.accountType = accountType
        self.currency = currency
        self.accountBalance = float(accountBalance)
        self.creationDate = creationDate
        
        self.accountStatus = "active"
        
        if (self.accountBalance > 0):
            self.accountBalance = math.trunc(100 * self.accountBalance) / 100   ; # formatting the amount value to 2 decimal points
        elif (self.accountBalance == 0):
            self.accountBalance = 0.00

    # Function to execute a deposit on a bank account
    def deposit(self, depositAmount):
        try:
            # Checking the amount to be deposited
            if (depositAmount > 0):
                self.accountBalance = float(self.accountBalance) + depositAmount
                return True
            else:
                print("\n***! Invalid amount entered")
                return False
        except ValueError:
            # Handing possible exceptions
            print("\n***! Invalid amount entered")
            return False

    # Function to execute a withdrawal on a bank account
    def withdraw(self, withdrawalAmount):
        try:
            # Checking the amount to be withdrawn
            if (withdrawalAmount > 0):
                # Checking for available funds to deduct the withdrawal amount
                if (self.accountBalance >= withdrawalAmount):
                    self.accountBalance = float(self.accountBalance) - withdrawalAmount
                    return True
                else:
                    print("\n***! Insufficient funds")
                    return False
            else:
                print("\n***! Invalid amount entered")
                return False
        except ValueError:
            # Handing possible exceptions
            print("\n***! Invalid amount entered")
            return False

    # Saving account data to text file
    def saveAccountState(self, accountsDirectory):
        # Setting to blank for variables not needed in this account type
        applyInterest = interestRate = overdraftAmount = mortgagePrincipal = ''
        mortgageTerm = repaymentAccount = repaymentAccount = mortgageInterestRate = ''
        
        fileName = accountsDirectory  + self.accountId +".txt"  ; # File name for account file
        
        fileContent = self.accountId + "," + self.customerLoginId + "," + self.accountType \
            + "," + self.currency + "," + str(self.accountBalance) + "," + self.creationDate \
                + "," + self.accountStatus + "," + applyInterest + "," + interestRate \
                    + "," + overdraftAmount + "," + mortgagePrincipal + "," + mortgageTerm \
                        + "," + repaymentAccount + "," + mortgageInterestRate
        try:
            with open( fileName, "w", encoding="UTF-8" ) as openedFile:
                openedFile.write(fileContent)  ; # Write to update on the file
                return True
        except FileNotFoundError:
            # Handing possible exceptions
            return False

    # Function to override the '__str__' function
    def __str__(self):
        output = "\nAccount Id: " + self.accountId
        # output += "\nCustomer Login Id: " + self.customerLoginId
        output += "\nAccount Type: " + self.accountType.title()
        output += "\nAccount Balance: " + currencySymbol + str(self.accountBalance)
        output += "\nAccount Created On: " + self.creationDate 
        output += "\n"
        
        return output
    
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

class savingsAccount(account):
    # Function to define what happens when a new object is created for this class
    def __init__(self, accountId, customerLoginId, accountType, currency, accountBalance, creationDate, applyInterest):
        super().__init__(accountId, customerLoginId, accountType, currency, accountBalance, creationDate)
        
        # Initializing class 'self' variables
        self.accountType = "savings account"
        self.applyInterest = applyInterest.upper()
        if (self.applyInterest == "Y"):
            self.interestRate = 3
        else:
            self.interestRate = 0
        
    # Saving account data to text file for 'savings account'
    def saveAccountState(self, accountsDirectory):
        # Setting to blank for variables not needed in this account type
        overdraftAmount = mortgagePrincipal = mortgageTerm = ''
        repaymentAccount = mortgageInterestRate = ''
        
        fileName = accountsDirectory  + self.accountId +".txt"  ; # File name for account file
        
        fileContent = self.accountId + "," + self.customerLoginId + "," + self.accountType \
            + "," + self.currency + "," + str(self.accountBalance) + "," + self.creationDate \
                + "," + self.accountStatus + "," + self.applyInterest + "," + str(self.interestRate) \
                    + "," + overdraftAmount + "," + mortgagePrincipal + "," + mortgageTerm \
                        + "," + repaymentAccount + "," + mortgageInterestRate
        try:
            with open( fileName, "w", encoding="UTF-8" ) as openedFile:
                openedFile.write(fileContent)  ; # Write to update on the file
                return True
        except FileNotFoundError:
            # Handing possible exceptions
            return False

    # Function to calculate the interest amount for the current month
    def calculateInterestAmount(self):
        if (self.interestRate != 0):
            principal = float(self.accountBalance)     ;# Account balance
            rate = float(self.interestRate) / 100     ;# interest rate
            time = 1 / 12  ; # 1 month of 12 months in a year
            interestAmount = ( principal * rate * time )
            interestAmount = math.trunc(100 * interestAmount) / 100   ; # formatting the amount value to 2 decimal points
            return interestAmount
        else:
            interestAmount = 0.00
            return interestAmount
    
    # Function to override the '__str__' function
    def __str__(self):
        output = "\nAccount Id: " + self.accountId
        # output += "\nCustomer Login Id: " + self.customerLoginId
        output += "\nAccount Type: " + self.accountType.title()
        output += "\nAccount Balance: " + currencySymbol + str(self.accountBalance)
        
        # Display interest info only if interest is flagged as 'Y' and account balance is positive
        if ( (self.applyInterest == "Y") and (float(self.accountBalance) > 0) ):
            # output += "\nApply Interest?: " + self.applyInterest
            output += "\nCurrent Month's interest: " + currencySymbol + str(self.calculateInterestAmount())
        
        output += "\nAccount Created On: " + self.creationDate 
        output += "\n"
        
        return output

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

class currentAccount(account):
    # Function to define what happens when a new object is created for this class
    def __init__(self, accountId, customerLoginId, accountType, currency, accountBalance, creationDate, applyInterest):
        super().__init__(accountId, customerLoginId, accountType, currency, accountBalance, creationDate)
        
        # Initializing class 'self' variables
        self.accountType = "current account"
        self.applyInterest = applyInterest.upper()
        if (self.applyInterest == "Y"):
            self.interestRate = 2
        else:
            self.interestRate = 0
        
        self.overdraftAmount = 100
        
    
    # Function to execute a withdrawal on a bank account
    def withdraw(self, withdrawalAmount):
        try:
            # Checking the amount to be withdrawn
            if (withdrawalAmount > 0):
                # Checking for available funds to deduct the withdrawal amount
                currentBalance = float(self.accountBalance) + float(self.overdraftAmount) ; # including available overdraft in the available balance
                
                if (currentBalance >= withdrawalAmount):
                    self.accountBalance = float(self.accountBalance) - withdrawalAmount
                    return True
                else:
                    print("\n***! Insufficient funds")
                    print("***! Withdrawal exceeds available overdraft\n")
                    return False
            else:
                print("\n***! Invalid amount entered")
                return False
        except ValueError:
            # Handing possible exceptions
            print("\n***! Invalid amount entered")
            return False

    # Saving account data to text file for 'current account'
    def saveAccountState(self, accountsDirectory):
        # Setting to blank for variables not needed in this account type
        mortgagePrincipal = mortgageTerm = ''
        repaymentAccount = mortgageInterestRate = ''
        
        fileName = accountsDirectory  + self.accountId +".txt"  ; # File name for account file
        
        fileContent = self.accountId + "," + self.customerLoginId + "," + self.accountType \
            + "," + self.currency + "," + str(self.accountBalance) + "," + self.creationDate \
                + "," + self.accountStatus + "," + self.applyInterest + "," + str(self.interestRate) \
                    + "," + str(self.overdraftAmount) + "," + mortgagePrincipal + "," + mortgageTerm \
                        + "," + repaymentAccount + "," + mortgageInterestRate
        try:
            with open( fileName, "w", encoding="UTF-8" ) as openedFile:
                openedFile.write(fileContent)  ; # Write to update on the file
                return True
        except FileNotFoundError:
            # Handing possible exceptions
            return False

    # Function to calculate the interest amount for the current month
    def calculateInterestAmount(self):
        if (self.interestRate != 0):
            principal = float(self.accountBalance)     ;# Account balance
            rate = float(self.interestRate) / 100     ;# interest rate
            time = 1 / 12  ; # 1 month of 12 months in a year
            interestAmount = ( principal * rate * time )
            interestAmount = math.trunc(100 * interestAmount) / 100   ; # formatting the amount value to 2 decimal points
            return interestAmount
        else:
            interestAmount = 0.00
            return interestAmount
    
    # Function to override the '__str__' function
    def __str__(self):
        
        if ( float(self.accountBalance) > 0 ):
            availableOverdraft = float(self.overdraftAmount)
        else:
            availableOverdraft = float(self.overdraftAmount) + float(self.accountBalance)
        
        output = "\nAccount Id: " + self.accountId
        # output += "\nCustomer Login Id: " + self.customerLoginId
        output += "\nAccount Type: " + self.accountType.title()
        output += "\nAccount Balance: " + currencySymbol + str(self.accountBalance)
        output += "\nAvailable Overdraft: " + currencySymbol + str(availableOverdraft)
        
        # Display interest info only if interest is flagged as 'Y' and account balance is positive
        if ( (self.applyInterest == "Y") and (float(self.accountBalance) > 0) ):
            # output += "\nApply Interest?: " + self.applyInterest
            output += "\nCurrent Month's interest: " + currencySymbol + str(self.calculateInterestAmount())
        
        output += "\nAccount Created On: " + self.creationDate 
        output += "\n"
                
        return output

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

class mortgageAccount(account):
    # Function to define what happens when a new object is created for this class
    def __init__(self, accountId, customerLoginId, accountType, currency, accountBalance, creationDate, mortgagePrincipal, mortgageTerm, repaymentAccount):
        super().__init__(accountId, customerLoginId, accountType, currency, accountBalance, creationDate)
        
        # Initializing class 'self' variables
        self.accountType = "mortgage account"
        self.mortgagePrincipal = int(mortgagePrincipal)
        self.mortgageTerm = int(mortgageTerm)
        self.repaymentAccount = repaymentAccount
        
        if (self.mortgageTerm <= 2):
            self.mortgageInterestRate = 6
        else:
            self.mortgageInterestRate = 4
    
    # Function to calculate the mortgage interest amount for the tenure of the mortgage
    def calculateInterestAmount(self):
        principal = float(self.mortgagePrincipal)
        rate = float(self.mortgageInterestRate) / 100
        time = float(self.mortgageTerm)
        interestAmount = ( principal * rate * time )
        interestAmount = math.trunc(100 * interestAmount) / 100   ; # formatting the amount value to 2 decimal points
        return interestAmount

    def calculateRepaymentAmount(self):
        principal = float(self.mortgagePrincipal)
        interestAmount = float(self.calculateInterestAmount())
        time = float(self.mortgageTerm)
        
        repaymentAmount = ( (principal + interestAmount) / time)
        repaymentAmount = math.trunc(100 * repaymentAmount) / 100   ; # formatting the amount value to 2 decimal points
        return repaymentAmount
        
    # Saving account data to text file for 'mortgage account'
    def saveAccountState(self, accountsDirectory):
        # Setting to blank for variables not needed in this account type
        applyInterest = interestRate = overdraftAmount = ''
        
        fileName = accountsDirectory  + self.accountId +".txt"  ; # File name for account file
        
        fileContent = self.accountId + "," + self.customerLoginId + "," + self.accountType \
            + "," + self.currency + "," + str(self.accountBalance) + "," + self.creationDate \
                + "," + self.accountStatus + "," + applyInterest + "," + interestRate \
                    + "," + overdraftAmount + "," + str(self.mortgagePrincipal) + "," + str(self.mortgageTerm) \
                        + "," + self.repaymentAccount + "," + str(self.mortgageInterestRate)
        try:
            with open( fileName, "w", encoding="UTF-8" ) as openedFile:
                openedFile.write(fileContent)  ; # Write to update on the file
                return True
        except FileNotFoundError:
            # Handing possible exceptions
            return False

    # Function to override the '__str__' function
    def __str__(self):
        output = "\nAccount Id: " + self.accountId
        # output += "\nCustomer Login Id: " + self.customerLoginId
        output += "\nAccount Type: " + self.accountType.title()
        # output += "\nAccount Balance: " + currencySymbol + str(self.accountBalance)
        output += "\nMortgage Principal: " + currencySymbol + str(self.mortgagePrincipal)
        output += "\nMortgage Term : " + str(self.mortgageTerm) + "years"
        output += "\nMortgage Repayment Account: " + self.repaymentAccount
        output += "\nMortgage Rate: " + self.mortgageInterestRate + "%"
        output += "\nAccount Created On: " + self.creationDate
        
        # output += "\n\nNote: An interest amount of " + currencySymbol + str(self.calculateInterestAmount()) + " will be deducted (when interest is applied to savings accounts) "
        monthlyRepaymentAmount = math.trunc(100 * (self.calculateRepaymentAmount() / 12) ) / 100   ; # formatting the amount value to 2 decimal points
        output += "\n\nNote: A monthly capital repayment amount of '"+ currencySymbol + str(monthlyRepaymentAmount) +"' \nwould be deducted from your repayment account ("+ self.repaymentAccount +")"
        output += " \n"

        
        return output

# ---------------------------------------------------------------------------------------

