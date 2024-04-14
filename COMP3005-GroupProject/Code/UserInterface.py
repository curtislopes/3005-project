import DBUtils
from datetime import datetime

# Session Globals
loggedInUserName = "NULL"

def validInput(input,startNum,lastNum):
    try:
        # If the input is not an int, it will error, thus returning false. 
        # If the date is an int, and within the specified range, it's valid.
        # Otherwise return False.
        if startNum <= int(input) <= lastNum:
            return True
        else:
            return False
    except (Exception) as error:
        return False
    
def validDBInput(input,over150CharsDisallowed=False, over20CharsDisallowed=False):    
    if over150CharsDisallowed:
        # If input is over 150, return false
        if len(input) > 150:
            return False    
    elif over20CharsDisallowed:
        # If input is over 20, return false
        if len(input) > 20:
            return False
    # Default varchar length is 50 in DB. If input is over 50, return false. 
    elif len(input) > 50:
        return False
    # Otherwise return True
    return True

def validTime(time):
    #NOTE: this function takes a string time input! not int ! that is why there is a try except
    try:
        #splits hours and minutes up
        hours, minutes = time.split(':')
        
        #ensure hours and minutes have 2 characters, to ensure data consistency.
        if len(hours) < 2 or len(minutes) < 2:
            return False
        
        #converts them to ints to work with
        hours = int(hours)
        minutes = int(minutes)
        
        #checks if hours and minutes are in acceptable range
        if 0 <= hours <= 23 and 0 <= minutes <= 59:
            return True
        else:
            return False
    except ValueError:
        return False

def validDate(date):
    try:
        # Tries to convert date into datetime object. 
        # If date is invalid (i.e. month/day outside of range) it errors and returns false.
        # Otherwise its a valid date
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validateNumberInput(num):
    #tries to case the number as a float. if it cannot, then except is entered.
    try:
        num = float(num)
        return True
    except ValueError:
        return False

def mainMenu():
    # Log out any logged in users when main menu accessed.
    global loggedInUserName
    loggedInUserName = "NULL"

    # LAC = Liam + Aaron + Curtis. Can be changed lmao
    print("\033[33mTHANK YOU FOR CHOOSING LAC HEALTH AND FITNESS CLUB!\033[0m")
    print("We hope you enjoy our Fitness Club Management service!")
    action = input("Please select an option:\
                \nEnter 1 for Login\
                \nEnter 2 for Signup\
                \nEnter 3 to Exit\
                \nEntry Choice: ")

    # Loop until valid entry is selected
    while(not validInput(action,1,3)):
        action = input("\033[91mError. Please enter a valid option: \033[0m")

    if (action == '1'):
        login()           
    elif (action == '2'):
        signup()
    elif (action == '3'):
        print("\033[33mThank you for using the LAC Health and Fitness Club Accounts Service!\033[0m")
        exit()

def login():
    global loggedInUserName # Initialize use of global variable in this function
    userName = input("Please enter your user name: ")
    while (DBUtils.validUserName(userName) == False):
        userName = input("\n\033[91mUser name not registered! Please Register if you haven't already by entering 'Q', OR Please enter your user name again: \033[0m") 
        if (userName.lower() == 'q'):
            mainMenu()

    password = input("Please enter your password: ")
    usersPassword = DBUtils.getUserPassword(userName)
    while(password != usersPassword):
        password = input("\033[91mError, Incorrect password. Press Q to exit, OR enter your password again: \033[0m")
        if (password.lower() == 'q'):
            mainMenu()

    print(f"\033[92mLogin successful! Welcome back {userName}!\033[0m")
    loggedInUserName = userName

    userType = DBUtils.getUserType(userName)
    if (userType == 'Members'):
        displayMemberCommands()
    elif (userType == 'Trainers'):
        displayTrainerCommands() 
    elif (userType == 'Staff'):
        displayStaffCommands()

def signup():
    print("\n\033[92mWelcome to Account Creation!\033[0m")
    accountType = input("\033[33mPlease select which account type you would like to create.\033[0m\
                        \nEnter 1 for Member\
                        \nEnter 2 for Personal Trainer\
                        \nEnter 3 for Staff (password required)\
                        \nEnter 4 to return to main menu\
                        \nEntry Choice: ")
    
    while(not validInput(accountType,1,4)):
        accountType = input("\033[91mError. Please enter a valid option: \033[0m")

    # Member account setup
    if (accountType == '1'):
        memberSignup()
    # Personal Trainer account setup
    elif (accountType == '2'):
        trainerSignup()
    # Staff account setup
    elif (accountType == '3'):
        staffSignup()
    # Return to main menu
    elif (accountType == '4'):
        mainMenu()

def memberSignup():
    firstName = input("Enter your first name: ")
    lastName = input("Enter your last name: ")
    email = input("Enter your email address: ")
    phoneNum = input("Enter your phone number (optional): ")
    address = input("Enter your address (optional): ")
    dateOfBirth = input("Enter your date of birth (YYYY-MM-DD): ")
    while(not validDate(dateOfBirth)):
        dateOfBirth = input("\033[91mError, date of birth format incorrect. Try again with the format YYYY-MM-DD: \033[0m")
    userName = input("Enter your user name: ")
    while(DBUtils.validUserName(userName)):
        userName = input("\033[91mError, user name already taken.\nPlease Enter a different user name: \033[0m")
    password = input("Enter your password: ")
    repassword = input("Please re-enter your password: ")

    # Loop until passwords match
    while(password != repassword):
        password = input("\033[91mError: passwords did not match, please enter password: \033[0m")
        repassword = input("Please re-enter your password: ")
    
    # Log in user if registration succeeds.
    if (DBUtils.registerMember(firstName,lastName,email,phoneNum,address,dateOfBirth,userName,password)):     
        global loggedInUserName # Initialize use of global variable so it can be modified
        loggedInUserName = userName
        print(f"Welcome {firstName}!")
        displayMemberCommands()

def trainerSignup():
    firstName = input("Enter your first name: ")
    lastName = input("Enter your last name: ")
    email = input("Enter your email address: ")
    phoneNum = input("Enter your phone number (optional): ")
    address = input("Enter your address (optional): ")
    dateOfBirth = input("Enter your date of birth (YYYY-MM-DD): ")
    while(not validDate(dateOfBirth)):
        dateOfBirth = input("\033[91mError, date of birth format incorrect. Try again with the format YYYY-MM-DD: \033[0m")
    userName = input("Enter your user name: ")
    while(DBUtils.validUserName(userName)):
        userName = input("\033[91mError, user name already taken.\nPlease Enter a different user name: \033[0m")
    certifications = input("Enter a comma seperated list of the names of your official certifications: ")
    password = input("Enter your password: ")
    repassword = input("Please re-enter your password: ")

    # Loop until passwords match
    while(password != repassword):
        password = input("\033[91mError: passwords did not match, please enter password: \033[0m")
        repassword = input("Please re-enter your password: ")

    # Log in user if registration succeeds.
    if (DBUtils.registerTrainer(firstName,lastName,email,phoneNum,address,dateOfBirth,userName,password,certifications)):     
        global loggedInUserName # Initialize use of global variable so it can be modified
        loggedInUserName = userName
        print(f"Welcome {firstName}!")
        displayTrainerCommands()

def staffSignup():
    HRPassword = input("\033[33mPlease enter the password provided to you by your HR representative to register a staff account: \033[0m")
    if (HRPassword != "LACStaff!"):
        print("\033[91mError, incorrect password. Exiting staff account creation.\033[0m")    
        mainMenu()        
    else:
        firstName = input("Enter your first name: ")
        lastName = input("Enter your last name: ")
        email = input("Enter your email address: ")
        phoneNum = input("Enter your phone number: ")
        address = input("Enter your address: ")
        dateOfBirth = input("Enter your date of birth (YYYY-MM-DD): ")
        while(not validDate(dateOfBirth)):
            dateOfBirth = input("\033[91mError, date of birth format incorrect. Try again with the format YYYY-MM-DD: \033[0m")
        userName = input("Enter your user name: ")
        while(DBUtils.validUserName(userName)):
            userName = input("\033[91mError, user name already taken.\nPlease Enter a different user name: \033[0m")
        jobTitle = input("Enter your job title: ")
        password = input("Enter your password: ")
        repassword = input("Please re-enter your password: ")

        # Loop until passwords match
        while(password != repassword):
            password = input("\033[91mError: passwords did not match, please enter password: \033[0m")
            repassword = input("Please re-enter your password: ")

        # Log in user if registration succeeds.
        if (DBUtils.registerStaff(firstName,lastName,email,phoneNum,address,dateOfBirth,userName,password,jobTitle)):     
            global loggedInUserName # Initialize use of global variable so it can be modified
            loggedInUserName = userName
            print(f"Welcome {firstName}!")
            displayStaffCommands()

def displayMemberCommands():
    command = input("\033[33mMember commands:\033[0m\
                \nEnter 1 to schedule a personal trainer session\
                \nEnter 2 to register for a group fitness class\
                \nEnter 3 to enter goals interface\
                \nEnter 4 to enter exercise routines interface\
                \nEnter 5 to enter health metrics interface\
                \nEnter 6 to display achievements\
                \nEnter 7 to update profile information\
                \nEnter 8 to log out\
                \nEntry Choice: ")
    
    # Loop until valid entry is selected
    while(not validInput(command,1,8)):
        command = input("\033[91mError. Please enter a valid option: \033[0m")
    if (command == '1'):
        DBUtils.scheduleMemberPTSession()
        displayMemberCommands()
    elif (command == '2'):
        DBUtils.scheduleMemberGroupFitness()
        displayMemberCommands()
    elif (command == '3'):
        goalsInterface()
    elif (command == '4'):
        exerciseRoutinesInterface()
    elif (command == '5'):
        healthMetricsInterface()
    elif (command == '6'):
        DBUtils.displayMemberAchievements(loggedInUserName)
        input("\033[33mPress enter to return to commands.\033[0m") 
        displayMemberCommands()
    elif (command == '7'):
        updateInfo = updateMemberInfoInterface()
        updateSQLEntry = updateInfo[0]
        updateValue = updateInfo[1]
        print(f"updateSQLEntry: {updateSQLEntry}")
        print(f"updateValue: {updateValue}")
        if (updateSQLEntry != "NULL" and updateValue != "NULL"):
            DBUtils.updateMemberInformation(updateSQLEntry,updateValue,loggedInUserName)
            displayMemberCommands()
        else:
            print("\033[91mError. Unable to update member information.\033[0m")   
    elif (command == '8'):
        mainMenu()

def exerciseRoutinesInterface():
    option = input("\033[33mExercise Routine commands:\033[0m\
        \nEnter 1 to display all exercise routines\
        \nEnter 2 to display favourite routines\
        \nEnter 3 to add a favourite routine\
        \nEnter 4 to remove a favourite routine\
        \nEnter 5 to go back to member commands\
        \nEntry Choice: ")
    # Loop until valid entry is selected
    while(not validInput(option,1,5)):
        option = input("\033[91mError. Please enter a valid option: \033[0m")
    
    if(option == '1'):
        DBUtils.displayAllExerciseRoutines()
        input("\033[33mPress enter to return to commands.\033[0m")
        exerciseRoutinesInterface()
    elif(option == '2'):
        DBUtils.displayFavouriteRoutines(loggedInUserName)
        input("\033[33mPress enter to return to commands.\033[0m")
        exerciseRoutinesInterface()
    elif(option == '3'):        
        allRoutines = DBUtils.getExerciseRoutines()
        favouritedRoutines = DBUtils.getFavouriteRoutines(loggedInUserName)
        allRoutineNames = []  
        favouritedRoutineNames = []
        # Extract unique routine names
        for routine, exercise in allRoutines:
            if (routine not in allRoutineNames):
                allRoutineNames.append(routine)
        for routine, exercise in favouritedRoutines:
            if (routine not in favouritedRoutineNames):
                favouritedRoutineNames.append(routine)

        nonFavouritedRoutinesNames = []
        for routine in allRoutineNames:
            if routine not in favouritedRoutineNames:
                nonFavouritedRoutinesNames.append(routine)

        print("\033[33m-All Unfavourited Routines-\033[0m")
        for routine in nonFavouritedRoutinesNames:
            print(routine)
            
        favRoutine = input("Enter routine name to add to favourites: ")

        if (not DBUtils.validRoutineName(favRoutine)):
            favRoutine = input("\033[91mError, entered routine name does not exist.\nEnter routine name as it appears to add to favourites: \033[0m")

        DBUtils.addFavouriteRoutine(loggedInUserName, favRoutine)
        exerciseRoutinesInterface()
    elif(option == '4'):        
        favouritedRoutines = DBUtils.getFavouriteRoutines(loggedInUserName)
        favouritedRoutineNames = []

        # Extract unique routine names
        for routine, exercise in favouritedRoutines:
            if (routine not in favouritedRoutineNames):
                favouritedRoutineNames.append(routine)

        print("-All Favourited Routines-")
        for routine in favouritedRoutineNames:
            print(routine)
            
        favRoutine = input("Enter routine name to remove from favourites: ")

        if (not DBUtils.validRoutineName(favRoutine)):
            favRoutine = input("\033[91mError, entered routine name does not exist.\nEnter routine name as it appears to add to favourites: \033[0m")

        DBUtils.removeFavouriteRoutine(loggedInUserName, favRoutine)
        exerciseRoutinesInterface()
    elif(option == '5'):
        displayMemberCommands()

def healthMetricsInterface():
    metricSelection = input("\033[33mSelect a Health Metrics option:\033[0m\
    \nEnter 1 to display your health metrics log\
    \nEnter 2 to add a health metric\
    \nEnter 3 to go back to member commands\
    \nEntry Choice: ")

    # Loop until valid entry is selected
    while(not validInput(metricSelection,1,3)):
        metricSelection = input("\033[91mError. Please enter a valid option: \033[0m")

    if (metricSelection == '1'):
        DBUtils.displayMemberHealthMetrics(loggedInUserName)
        input("\033[33mPress enter to return to commands.\033[0m") 
        healthMetricsInterface()
    elif (metricSelection == '2'):
        metricName = input("Enter Metric Name: ")
        metricValue = input("Enter Metric Value: ")
        dateRecorded = datetime.today().strftime('%Y-%m-%d')
        DBUtils.addMemberHealthMetrics(loggedInUserName,metricName,metricValue,dateRecorded)
        healthMetricsInterface()
    elif (metricSelection == '3'):
        displayMemberCommands()

def goalsInterface():
    goalSelection = input("\033[33mSelect a Goals option:\033[0m\
        \nEnter 1 to display your goals\
        \nEnter 2 to mark a goal as complete\
        \nEnter 3 to add a goal\
        \nEnter 4 to delete a goal\
        \nEnter 5 to go back to member commands\
        \nEntry Choice: ")
    
    # Loop until valid entry is selected
    while(not validInput(goalSelection,1,5)):
        goalSelection = input("\033[91mError. Please enter a valid option: \033[0m")
    
    if (goalSelection == '1'):
        DBUtils.displayMemberGoals(loggedInUserName)
        input("\033[33mPress enter to return to commands.\033[0m") 
        goalsInterface()
    elif (goalSelection == '2'):
        # If member has goals to display
        if (DBUtils.displayMemberGoals(loggedInUserName)):
            goalName = input("Please enter a goal name to mark as an achievement from the list above: ")
            if (DBUtils.validGoalName(goalName)):
                achievementDate = datetime.today().strftime('%Y-%m-%d')
                DBUtils.addMemberAchievement(loggedInUserName,goalName,achievementDate)
                DBUtils.removeMemberGoal(loggedInUserName,goalName)
        goalsInterface()
    elif (goalSelection == '3'):
        goalType = input("Enter Goal Name: ")
        currentVal = input("Enter Current Value: ")
        targetVal = input("Enter Target Value: ")
        startDate = datetime.today().strftime('%Y-%m-%d')
        targetDate = input("Enter Target Date for Goal Achievement (YYYY-MM-DD): ")
        while(not validDate(targetDate)):
            targetDate = input("\033[91mError, Target Date format incorrect. Try again with the format YYYY-MM-DD: \033[0m")
        DBUtils.addMemberGoal(loggedInUserName,goalType,currentVal,targetVal,startDate,targetDate)
        goalsInterface()
    elif (goalSelection == '4'):
        # If member has goals to display
        if (DBUtils.displayMemberGoals(loggedInUserName)):        
            goalName = input("Please enter a goal name to remove from the list above: ")
            if (DBUtils.validGoalName(goalName)):
                DBUtils.removeMemberGoal(loggedInUserName,goalName)
        goalsInterface()
    elif (goalSelection == '5'):
        displayMemberCommands()

def updateMemberInfoInterface():
    updateValue = "NULL"
    updateSQLEntry = "NULL"

    updateSelection = input("\033[33mSelect a field to modify:\033[0m\
        \nEnter 1 to reset password\
        \nEnter 2 to modify user name\
        \nEnter 3 to modify first name\
        \nEnter 4 to modify last name\
        \nEnter 5 to modify email address\
        \nEnter 6 to modify phone number\
        \nEnter 7 to modify address\
        \nEnter 8 to modify date of birth\
        \nEnter 9 to go back\
        \nEntry Choice: ")
    # Loop until valid entry is selected
    while(not validInput(updateSelection,1,9)):
        updateSelection = input("\033[91mError. Please enter a valid option: \033[0m")

    if (updateSelection == '1'):
        updateSQLEntry = "Password"
        password = input("Enter your current password: ")
        oldPassword = DBUtils.getUserPassword(loggedInUserName)
        while(password != oldPassword):
            password = input("\033[91mError, incorrect password. Please enter password again: \033[0m")

        password = input("Enter your new password: ")
        repassword = input("Please re-enter your new password: ")
        # Loop until passwords match
        while(password != repassword):
            password = input("\033[91mError: passwords did not match, please enter password: \033[0m")
            repassword = input("Please re-enter your password: ")

        updateValue = password
    elif (updateSelection == '2'):
        updateSQLEntry = "UserName"
        userName = input("Enter your updated user name: ")
        while(DBUtils.validUserName(userName)):
            userName = input("\033[91mError, user name already taken.\nPlease Enter a different user name: \033[0m")
        updateValue = userName
    elif (updateSelection == '3'):
        updateSQLEntry = "FirstName"
        updateValue = input("Enter your updated first name: ")  
    elif (updateSelection == '4'):
        updateSQLEntry = "LastName"
        updateValue = input("Enter your updated last name: ")
    elif (updateSelection == '5'):
        updateSQLEntry = "Email"
        updateValue = input("Enter your updated email address: ")
    elif (updateSelection == '6'):
        updateSQLEntry = "Phone"
        updateValue = input("Enter your updated phone number: ")
    elif (updateSelection == '7'):
        updateSQLEntry = "Address"
        updateValue = input("Enter your updated address: ")
    elif (updateSelection == '8'):
        updateSQLEntry = "DateOfBirth"
        dateOfBirth = input("Enter your date of birth (YYYY-MM-DD): ")
        while(not validDate(dateOfBirth)):
            dateOfBirth = input("\033[91mError, date of birth format incorrect. Try again with the format YYYY-MM-DD: \033[0m")
        updateValue = dateOfBirth
    elif (updateSelection == '9'):
        displayMemberCommands()

    return updateSQLEntry,updateValue

def displayTrainerCommands():
    command = input("\033[33mTrainer commands:\033[0m\
                \nEnter 1 to set or update training availibility\
                \nEnter 2 to remove current availability\
                \nEnter 3 to view a member's profile\
                \nEnter 4 to create a new exercise routine\
                \nEnter 5 to log out\
                \nEntry Choice: ")
    
     # Loop until valid entry is selected
    while(not validInput(command,1,5)):
        command = input("\033[91mError. Please enter a valid option: \033[0m")
    if (command == '1'):
        DBUtils.setAvailableTrainingTimes(loggedInUserName)
    elif (command == '2'):
        DBUtils.removeAvailableTime(loggedInUserName)
    elif (command == '3'):
        DBUtils.viewMemberProfile(loggedInUserName)   
    elif (command == '4'):
        DBUtils.createExerciseRoutine()
    elif (command == '5'):
        mainMenu()

def getDayOfWeek(date):
    date = date.weekday()
    return date

#staff-related interface functions :
def displayStaffCommands():
    command = input("Staff commands:\
                \nEnter 1 to book a room\
                \nEnter 2 to display the status of the equipment\
                \nEnter 3 to alter class schedule\
                \nEnter 4 to process payment transaction\
                \nEnter 5 to add Equipment to the gym\
                \nEnter 6 to request equipment maintenance\
                \nEnter 7 to view equipment maintenance requests\
                \nEnter 8 to log out\
                \nEntry Choice: ")
    # Loop until valid entry is selected
    while(not validInput(command,1,8)):
        command = input("Error. Please enter a valid option: ")
    if (command == '1'):
        bookRoomInterface()
        displayStaffCommands()   
    elif (command == '2'):
        DBUtils.displayEquipmentStatus()
        displayStaffCommands()
    elif (command == '3'):
        addClassScheduleInterface()
        displayStaffCommands()
    elif (command == '4'):
        paymentTransactionInterface()
        displayStaffCommands()
    elif (command == '5'):
        addEquipmentInterface()
        displayStaffCommands()
    elif (command == '6'):
        requestEquipmentMaintenanceInterface()
        displayStaffCommands()
    elif (command == '7'):
        DBUtils.displayEquipmentMaintenanceRequests()
        displayStaffCommands()
    elif (command == '8'):
        mainMenu() 

def bookRoomInterface():

    numRooms = DBUtils.displayRooms()

    roomID = input("\nPlease enter the number of the room you'd like to book: ")
    while(not validInput(roomID,1,numRooms)):
        roomID = input("Error. Invalid input.\nPlease enter the number of the room you'd like to book: ")

    date = input("\nPlease enter the date at which you'd like your booking (formatting: YYYY-MM-DD): ")
    while(not validDate(date)):
        date = input("\nError. Invalid input.\nPlease enter the date at which you'd like your booking (formatting: YYYY-MM-DD): ")
    
    startTime = input("\nPlease enter the time at which you'd like to start your booking (formatting: HH:MM, 24-hour time): ")
    while(not validTime(startTime)):
        startTime = input("\nError. Invalid input. \nPlease enter the time at which you'd like to start your booking (formatting: HH:MM, 24-hour time): ")
    
    endTime = input("\nPlease enter the time at which you'd like to end your booking (formatting: HH:MM, 24-hour time): ")
    while(not validTime(endTime)):
        endTime = input("\nError. Invalid input. \nPlease enter the time at which you'd like to end your booking (formatting: HH:MM, 24-hour time): ")
    
    success = DBUtils.bookARoom(roomID,startTime,endTime,date)

    if not success:
        userIn = input("Would you like to like to try to make another booking? (Y/N): ")
        if(userIn == 'Y'):
            bookRoomInterface()
    #for new line
    print()

def addClassScheduleInterface():

    numClasses = DBUtils.displayClasses()
    classID = input("\nPlease enter the number of the class you'd like to schedule: ")
    while(not validInput(classID,1,numClasses)):
        classID = input("Error. Invalid input.\nPlease enter the number of the class you'd like to schedule: ")
    print()

    numTrainers =  DBUtils.displayTrainerNames()
    trainerID = input("\nPlease enter the trainer's ID: ")
    while(not validInput(trainerID,1,numTrainers)):
        trainerID = input("Error. Invalid input.\nPlease enter the class trainer's ID: ")
    print()

    numRooms = DBUtils.displayRooms()
    roomID = input("\nPlease enter the number of the room you'd like to book: ")
    while(not validInput(roomID,1,numRooms)):
        roomID = input("Error. Invalid input.\nPlease enter the number of the room you'd like to book: ")
    print()

    date = input("\nPlease enter the date at which you'd like to schedule your class (formatting: YYYY-MM-DD): ")
    while(not validDate(date)):
        date = input("\nError. Invalid input.\nPlease enter the date at which you'd like to schedule your class (formatting: YYYY-MM-DD): ")
    

    startTime = input("\nPlease enter the time at which you'd like to start your class (formatting: HH:MM, 24-hour time): ")
    while(not validTime(startTime)):
        startTime = input("\nError. Invalid input. \nPlease enter the time at which you'd like to start your class (formatting: HH:MM, 24-hour time): ")
    
    endTime = input("\nPlease enter the time at which you'd like to have your class end (formatting: HH:MM, 24-hour time): ")
    while(not validTime(endTime)):
        endTime = input("\nError. Invalid input. \nPlease enter the time at which you'd like to have your class end (formatting: HH:MM, 24-hour time): ")
    dayOfWeek = date
    dayOfWeek  = datetime.strptime(dayOfWeek , '%Y-%m-%d')
    dayOfWeek  = int(dayOfWeek .strftime('%w'))  # Convert the day of the week string to an integer
    
    success = DBUtils.addClassSchedule(trainerID,classID,roomID,dayOfWeek ,startTime,endTime)

    if not success:
        userIn = input("Would you like to like to try to make another class schedule? (Y/N): ")
        if(userIn == 'Y'):
            bookRoomInterface()
    else:
        DBUtils.bookARoom(roomID,startTime,endTime,date)
    #for new line
    print()

def paymentTransactionInterface():
    memberName = input("Enter the name of the member paying: ")
    while (not DBUtils.validUserName(memberName)):
        memberName = input("Member not found. Enter the name of the member paying: ")

    dateToday = datetime.today().strftime('%Y-%m-%d')

    amount= input("Please enter the amount of the transaction: (ex. 4000, 29.99): ")
    while (not validateNumberInput(amount)):
        amount= input("Invalid input. Please enter the amount of the transaction: (ex. 4000, 29.99): ")
    
    purchaseType = input("Please enter the product purchased: ")

    success = DBUtils.paymentTransaction(memberName,dateToday,amount,purchaseType)

    if not success:
        userIN = input("Error: Unable to process payment. Would you like to try again? (Y/N): ")
        if userIN =='Y':
            paymentTransactionInterface()
    input("Press enter to return to staff commands.")
    #for line break
    print()

def addEquipmentInterface():
    equipName = input("Enter the name of the equipment being added: ")
    equipMaintenance = input("Does the equipment need maintenance? (Y/N): ")
    while equipMaintenance not in ['Y', 'N']:
            equipMaintenance = input("Invalid input. Does the equipment need maintenance? (Y/N): ")
    if  equipMaintenance == 'Y':
        DBUtils.addEquipment(equipName, True)
    elif equipMaintenance == 'N':
        DBUtils.addEquipment(equipName, False)
    
    #for new line
    print("")

def requestEquipmentMaintenanceInterface():
    equipName = input("Enter the name of the equipment needing maintenance: ")
    equipMaintenance = input("Describe the issue with the equipment: ")
    maintenanceDate = input("Enter the date of repair: (Format: YYYY-MM-DD): ")
    while(not validDate(maintenanceDate)):
        maintenanceDate = input("Invalid input. Enter the date of repair: (Format: YYYY-MM-DD): ")

    success = DBUtils.addEquipmentMaintenanceRequest(equipName, equipMaintenance, maintenanceDate)
   
    if not success:
        userIN = input("Error: could not find equipment in the database. Would you like to try again? (Y/N): ")
        if userIN =='Y':
            requestEquipmentMaintenanceInterface()

    #for new line
    print()

# Starts the interface
mainMenu()