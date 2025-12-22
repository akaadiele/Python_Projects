# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

"""
* Course Code  : AC51002 - Software Development
* Title   : Assignment 1 - Functional Programming
* Developed By : Adiele Akachukwu
* Date Created : Monday, November 4, 2024
"""

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Importing Libraries
import os, sys, time

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Declaring Global Variables:
currentTime = 0 ; operatingHoursLimit = 50 ; workingHoursStart = 900 ; workingHoursStop = 1700

# #5
# Specified items for production
itemsCatalog = { "Bags": 30, "Shirts": 50, "Trousers": 50, "Shoes": 20, "Jackets": 70 }

# Get the root directory for the location of python program
baseDirectory = os.path.dirname(os.path.abspath(__file__)) + "/DundeeZest_Files/"
productionDataDirectory = baseDirectory + "/Production_Data/"
try:
    # Redundancy check to create directories if they do not exist
    os.makedirs(baseDirectory)
    os.makedirs(productionDataDirectory)
except FileExistsError:
    # directory already exists
    pass

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------
# Defining Functions to be used during execution


# Resetting data stored on files
def resetData():
    # #9
    # Walk through directory, building a list with the file names within the directory
    fileNames = next(os.walk(productionDataDirectory), (None, None, []))[2]  # [] if no file
    for fileName in fileNames:
        with open( productionDataDirectory  + fileName, "w", encoding="UTF-8" ) as openedFile:
            openedFile.write("")  ;  # Reset Production Data for each operator
        
    updateOperatingHours(0,0)  ;  # Reset Operating Hours

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Initiating service maintenance
def triggerServiceMaintenance():
    # #8
    print("\n\nService Required")
    
    # Walk through directory, building a list with the file names within the directory
    fileNames = next(os.walk(productionDataDirectory), (None, None, []))[2]  # [] if no file
    for fileName in fileNames:
        with open( productionDataDirectory  + fileName, "r", encoding="UTF-8" ) as openedFile:
            if (openedFile != ''):
                # Display saved production data for each operator
                # #10
                print("------------------------------------------\n")
                print("Production data for Operator - " + str( fileName.split(".txt")[0] ) + "\n")
                
                for line in openedFile:
                    itemNames , itemsPerHour , previousHoursWorked , previousTotalPerItem , previousTotalAllItems = line.rstrip().split(",")
                    print(itemNames +": "+ previousTotalPerItem)    ; # Formatting the output for production data to be displayed
                
                print("\nTotal Items: " + previousTotalAllItems)    ; # Displaying info total items

    # #9
    resetData()     ; # Call function to reset previously saved production data

    print("------------------------------------------\n")
    print("\n***System shutting down for maintenance***\n")

    # #11
    time.sleep(10)  ; # 10 seconds hold
    sys.exit()  ; # End program for maintenance

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Reading Operator Data stored on file
def retrieveOperatorData(operatorId):
    # #7
    try:
        with open( productionDataDirectory  + str(operatorId) +".txt", "r", encoding="UTF-8" ) as openedFile:
            for line in openedFile:
                # Splitting content in each line and store in variables
                itemNames , itemsPerHour , previousHoursWorked , previousTotalPerItem , previousTotalAllItems = line.rstrip().split(",")
    except FileNotFoundError:
        previousHoursWorked = 0

    return int(previousHoursWorked)

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Updating Operator Data on file
def updateOperatorData(operatorId, operatingHours, previousHoursWorked):
    # #6
    if (previousHoursWorked != ""):
        operatingHours += previousHoursWorked
    
    itemNames = list(itemsCatalog.keys())   ; # Build iterable list of the item names from dictionary
    itemsPerHour = list(itemsCatalog.values())   ; # Build iterable list of the items quantity per hour from dictionary
    totalItems = 0
    fileContent = "Items,Quantity Produced per Hour,Hours Worked,Total (per item),Total (all items)"    ; # Include a header line for the file

    for i in range(0, len(itemsCatalog)):
        # Add new line for each product details
        totalItems += itemsPerHour[i] * operatingHours
        fileContent += ( "\n" + str(itemNames[i]) + "," + str(int(itemsPerHour[i])) + "," + str(int(operatingHours)) + "," + str(int(itemsPerHour[i] * operatingHours)) + "," + str(int(totalItems)) )

    # Write to file
    fileName = productionDataDirectory  + str(operatorId) +".txt"
    with open( fileName, "w", encoding="UTF-8" ) as openedFile:
        openedFile.write(fileContent)  ; # Write to update on the file

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Reading Operating Hours stored on file
def retrieveOperatingHours():
    # #3
    try:
        with open(baseDirectory + "/Operating_Hours_Log.txt", "r", encoding="UTF-8") as openedFile:
            fileContent = openedFile.read()     ; # Read previous operating hours saved
            operatingHours = int(fileContent)
    except FileNotFoundError:
        operatingHours = 0

    return operatingHours

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Updating Operating Hours on file
def updateOperatingHours(operatingHours, hoursWorked):
    # #4
    # Calculate updated operating hours
    operatingHours += hoursWorked

    with open( baseDirectory + "/Operating_Hours_Log.txt", "w", encoding="UTF-8" ) as openedFile:
        openedFile.write(str(int(operatingHours)))  ; # Write to update on the file
    
    return operatingHours

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Operator login and Initiate production process 
def logIn(clockInTime):
    operatorId = (input("\nEnter your assigned User Id: ")).upper()
    print(f"\nWelcome, {operatorId}." )
    print(f"\nYour clock-in time for today is {clockInTime[0:2]}:{clockInTime[2:4]}",end="\n",)

    retrieveOperatorData(operatorId)

    hoursWorked = (int(workingHoursStop) - int(clockInTime)) / 100
    currentProductionTime = int(clockInTime) + 100

    # Loop through operating hours
    while currentProductionTime < int(workingHoursStop):
        # #2
        print(f"[Time: {str(currentProductionTime)[0:2]}:{str(currentProductionTime)[2:4]}] ... Production is progress")
        
        currentOperatingHours = retrieveOperatingHours() + ( (currentProductionTime - int(clockInTime)) / 100)
        if (currentOperatingHours >= operatingHoursLimit):
            # Check for maintenance conditions
            hoursWorked = (currentProductionTime - int(clockInTime)) / 100
            updateOperatorData(operatorId, hoursWorked, retrieveOperatorData(operatorId))
            updateOperatingHours(retrieveOperatingHours(), hoursWorked)
            print("!!!\n") ; time.sleep(1)
            triggerServiceMaintenance()
        
        currentProductionTime += 100
    # Loop ends

    print(f"\n   ... Production Concluded ...")

    return operatorId, hoursWorked

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

# Begin operations
while (currentTime >= 0000) and (currentTime < 2400):
# Loop through 24hour cycle
    # Formatting the time to string and left justified with zeros to complete 4 characters
    currentTimeFmt = str(currentTime).zfill(4)
    
    print(f"\n[Time: {currentTimeFmt[0:2]}:{currentTimeFmt[2:4]}]")

    # Check if the current time falls within working hours
    if (int(currentTime) >= int(workingHoursStart)) and (int(currentTime) < int(workingHoursStop)):
        # System comes Online, ready to use
        # #1
        print("System online ... \n----------------------------------")
        print("Enter the appropriate command and press the 'ENTER' key: ")
        print("   *** 'START' - Begin production ***")
        print("   *** 'EXIT' - End production ***")
        print("   *** Any other input or leave blank - Skip to next check-in hour ***")
        commandInput = input(">>> ")
        
        currentOperatingHours = retrieveOperatingHours()
            
        if commandInput.upper() == "START":
            # Production processes for an operator
            operatorId, hoursWorked = logIn(currentTimeFmt)
            updateOperatingHours(currentOperatingHours, hoursWorked)
            updateOperatorData(operatorId, hoursWorked, retrieveOperatorData(operatorId))

            currentTime += hoursWorked * 100
        elif commandInput.upper() == "EXIT":
            # Close program on request
            sys.exit()
        else:
            # Skip to next hour
            currentTime += 100

        if (currentOperatingHours >= operatingHoursLimit):
            # Check for maintenance conditions
            print("!!!\n") ; time.sleep(1)
            triggerServiceMaintenance()
    else:
        # System offline,
        print("The system is currently offline \n----------------------------------")
        currentTime += 100  ;# Skip to next hour

    if (currentTime > 2300): 
        currentTime = 0     ; # Reset clock for new day/production cycle
    
    time.sleep(1)
# Loop ends

# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------