# Python libary used to communicate with postgres servers
import psycopg2

daysOfWeek = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
### GENERAL DB FUNCTIONS ###
# This function creates a connection to the server using the provided server configuration/connection details
def connectToDB():
    try:
        # Creates the connection
        conn = psycopg2.connect(
            database='GroupProject',
            user='postgres',
            password='password123',
            host= 'localhost', 
            port='5432'
        )
        # returns the connection object
        return conn
    # handles error on connection failure
    except (Exception, psycopg2.Error) as error:
        print("\033[91mError connecting to PostgreSQL database:\033[0m", error)

# Error checking done on caller side to allow custom error messages.
# NOTE: Must call this function in a try except block for proper error handling.
def runDBCommand(command):
    # Creates connection to the server.
    conn = connectToDB()
    # checks if connection was successful
    if conn:
        # creates server connection cursor
        cursor = conn.cursor()
        # Executes the passed in SQL command
        cursor.execute(command)
        # commits the current staged database changes to make the changes permament.
        conn.commit()
        # Get results of command
        try:
            # If command has a result, return result, otherwise return True
            results = cursor.fetchall()
            # Closes down the cursor and server connection
            cursor.close()
            conn.close()
            return results
        except (Exception, psycopg2.Error) as error:
            # Error will be caught by calling function to allow custom error messages
            pass
        # Closes down the cursor and server connection and return True, no result from command due to it not being a query.
        cursor.close()
        conn.close()

### HELPER/VALIDATION FUNCTIONS ###
# Checks if a user name exists. Usernames are unique across all account types
def validUserName(userName):
    # Users are not allowed to have the username 'NULL', otherwise it will mess up logic checks
    if (userName == "NULL"):
        return False
    
    command = f"""SELECT EXISTS (
                SELECT 1 FROM Members WHERE UserName = '{userName}'
                UNION ALL
                SELECT 1 FROM Trainers WHERE UserName = '{userName}'
                UNION ALL
                SELECT 1 FROM Staff WHERE UserName = '{userName}'
                );"""
    try:
        # If runDBCommand returns true for this query, that means that the username exists, so return True.
        if "true" in str(runDBCommand(command)).lower():
            return True
    except (Exception, psycopg2.Error) as error:
        # This ideally will never happen unless theres a big problem within the DB, since the query command should always work
        return f"DB ERROR: Username uniqueness query failed. Error: {error}"
    
    # If didnt already return True, then runDBCommand returned false, this means that the username doesn't exist, so return False.
    return False
    
def validRoutineName(routineName):
    command = f"""SELECT EXISTS (
                SELECT 1 FROM ExerciseRoutines
                JOIN Routines ON ExerciseRoutines.RoutineID = Routines.RoutineID
                WHERE LOWER(Routines.RoutineName) = '{routineName.lower()}'
                );"""
    try:
        # If runDBCommand returns true for this query, that means that the routine name exists in ExerciseRoutines, so return True.
        if "true" in str(runDBCommand(command)).lower():
            return True
    except (Exception, psycopg2.Error) as error:
        # This ideally will never happen unless theres a big problem within the DB, since the query command should always work
        return f"DB ERROR: Username uniqueness query failed. Error: {error}"
    
    # If didnt already return True, then runDBCommand returned false, this means that the routine name doesn't exist in ExerciseRoutines, so return False.
    return False

def validGoalName(goalName):
    command = f"""SELECT EXISTS (
                SELECT 1 FROM MemberGoals
                WHERE LOWER(MemberGoals.GoalType) = '{goalName.lower()}'
                );"""
    try:
        # If runDBCommand returns true for this query, that means that the routine name exists in ExerciseRoutines, so return True.
        if "true" in str(runDBCommand(command)).lower():
            return True
    except (Exception, psycopg2.Error) as error:
        # This ideally will never happen unless theres a big problem within the DB, since the query command should always work
        return f"DB ERROR: Goal Name query failed. Error: {error}"
    
    # If didnt already return True, then runDBCommand returned false, this means that the routine name doesn't exist in ExerciseRoutines, so return False.
    return False

def convertTimeToInt(time):
    #please note - this function converts your string time to the total amount of minutes
    hours, minutes = map(int, time.split(':'))
    return hours * 60 + minutes

def timeOverlap(startTimeNew, endTimeNew, startTimeOld, endTimeOld):
    #returns TRUE if there is a time overlap, false if there is no overlap
    startTimeNew = convertTimeToInt(startTimeNew)
    endTimeNew = convertTimeToInt(endTimeNew)
    startTimeOld = convertTimeToInt(startTimeOld)
    endTimeOld = convertTimeToInt(endTimeOld)
    
    if startTimeNew < endTimeOld and startTimeOld < endTimeNew:
        return True
    
    return False

def getEquipmentName(equipmentID):
    command = f"SELECT EquipmentName FROM Equipment WHERE EquipmentID = {equipmentID}"
    try:
        name = runDBCommand(command)
        if name:
            return name[0][0]
        else:
            return None
        
    except (Exception, psycopg2.Error) as error:
        print(f"DB error: {error}")
        return None

def getEquipmentID(name):
    command = f"SELECT EquipmentID FROM Equipment WHERE EquipmentName = '{name}'"
    try:
        name = runDBCommand(command)
        if name:
            return name[0][0]
        else:
            return None
        
    except (Exception, psycopg2.Error) as error:
        print(f"DB error: {error}")
        return None
    
def getUserPassword(userName):
    command = f"""SELECT Password FROM Members WHERE UserName = '{userName}'
                UNION ALL
                SELECT Password FROM Trainers WHERE UserName = '{userName}'
                UNION ALL
                SELECT Password FROM Staff WHERE UserName = '{userName}';"""
    try:
        # If runDBCommand returns false for this query, that means that the username doesn't exist, so return True.
        password = runDBCommand(command)
        if password != None:
            return password[0][0]
    except (Exception, psycopg2.Error) as error:
        # This ideally will never happen unless theres a big problem within the DB, since the query command should always work
        return f"DB ERROR: User password query failed. Error: {error}"
    
def getUserType(userName):
    types = ['Members', 'Trainers', 'Staff']

    for type in types:
        command = f"SELECT EXISTS (SELECT 1 FROM {type} WHERE UserName = '{userName}');"
        try:
            # If runDBCommand returns false for this query, that means that the username doesn't exist, so print error.
            if "true" in str(runDBCommand(command)).lower():
                return type
        except (Exception, psycopg2.Error) as error:
            # This ideally will never happen unless theres a big problem within the DB, since the query command should always work
            return f"DB ERROR: User type query failed. Error: {error}"
        
    print("\033[91mDB ERROR: user name does not exist.\033[0m") # This should idealy never print, since the calling function confirms that the user exists first.

def getMemberGoal(userName, goalName):
    command = f"""SELECT * FROM MemberGoals 
            JOIN Members ON MemberGoals.MemberID = Members.MemberID
            WHERE Members.UserName = '{userName}' AND LOWER(GoalType) = '{goalName.lower()}'; 
            """
    try:      
        goal = runDBCommand(command)
        if goal != None:
            return goal
    except (Exception, psycopg2.Error) as error:
        # This ideally will never happen unless theres a big problem within the DB, 
        # since the query command should always work since input is validated prior to call
        print(f"\033[91mError fetching goal: {error}\033[0m")

def getTrainerID(userName):
    command = f"""SELECT TrainerID 
                FROM Trainers 
                WHERE UserName = '{userName}'; 
                """
    try:
        trainerID = runDBCommand(command)
        if trainerID != None:
            return trainerID[0][0]
    except (Exception, psycopg2.Error) as error:
        # This ideally will never happen unless theres a big problem within the DB, 
        # since the query command should always work since input is validated prior to call
        return f"DB ERROR: TrainerID lookup from username failed. Error: {error}"

def getMemberID(userName):
    command = f"""SELECT MemberID 
                FROM Members 
                WHERE UserName = '{userName}'; 
                """
    try:
        memberID = runDBCommand(command)
        if memberID != None:
            return memberID[0][0]
    except (Exception, psycopg2.Error) as error:
        # This ideally will never happen unless theres a big problem within the DB, 
        # since the query command should always work since input is validated prior to call
        return f"DB ERROR: MemberID lookup from username failed. Error: {error}"

def getStaffID(userName):
    command = f"""SELECT StaffID 
                FROM Staffs 
                WHERE UserName = '{userName}'; 
                """
    try:
        StaffID = runDBCommand(command)
        if StaffID != None:
            return StaffID[0][0]
    except (Exception, psycopg2.Error) as error:
        # This ideally will never happen unless theres a big problem within the DB, 
        # since the query command should always work since input is validated prior to call
        return f"DB ERROR: MemberID lookup from username failed. Error: {error}"
    
def getRoutineID(routineName):
    command = f"""SELECT RoutineID 
                FROM Routines 
                WHERE LOWER(RoutineName) = '{routineName}'; 
                """
    try:
        routineID = runDBCommand(command)
        if routineID != None:
            return routineID[0][0]
    except (Exception, psycopg2.Error) as error:
        # This ideally will never happen unless theres a big problem within the DB, 
        # since the query command should always work since input is validated prior to call
        return f"DB ERROR: RoutineID lookup from routine name failed. Error: {error}"

### MEMBER FUNCTIONS ###

# This function adds the new member into the members table in the database
def registerMember(firstName, lastName,email,phone,address,DOB,userName,password):
    command = f"INSERT INTO Members (Password,UserName,FirstName,LastName,Email,Phone,Address,DateOfBirth,RegistrationDate)\
    \nVALUES('{password}','{userName}','{firstName}','{lastName}','{email}','{phone}','{address}','{DOB}',CURRENT_DATE)"
    try:
        runDBCommand(command)        
        # If doesn't error, it successfully added it, since input is validated prior to call
        print("\033[92mMember account successfully created!\033[0m")
        return True
    except (Exception, psycopg2.Error) as error:
        print("\033[91mFailed to create new Member account. Error: \033[0m", error)

# This function updates the value for a specified field and member.
def updateMemberInformation(updateSQLEntry, updateValue, loggedInUserName):
    command = f"UPDATE Members SET {updateSQLEntry} = '{updateValue}' WHERE UserName = '{loggedInUserName}'"
    try:
        runDBCommand(command)        
        # If doesn't error, it successfully updated it, since input is validated prior to call
        print(f"\033[92mMember {updateSQLEntry} successfully updated!\033[0m")
    except (Exception, psycopg2.Error) as error:
        print(f"\033[91mFailed to update Member's {updateSQLEntry}. Error: \033[0m", error)

def getExerciseRoutines():
    command = f"""SELECT Routines.RoutineName, Exercises.ExerciseName  
                FROM ExerciseRoutines
                JOIN Routines ON ExerciseRoutines.RoutineID = Routines.RoutineID
                JOIN Exercises ON ExerciseRoutines.ExerciseID = Exercises.ExerciseID
                ORDER BY Routines.RoutineName, Exercises.ExerciseName"""
    try:
        return runDBCommand(command)        
    except (Exception, psycopg2.Error) as error:
        print(f"\033[91mFailed to get exercise routines. Error: \033[0m", error)

def getFavouriteRoutines(userName):
    command = f"""SELECT DISTINCT Routines.RoutineName, Exercises.ExerciseName
                FROM FavouriteRoutines
                JOIN Members ON FavouriteRoutines.MemberID = Members.MemberID
                JOIN ExerciseRoutines ON FavouriteRoutines.RoutineID = ExerciseRoutines.RoutineID
                JOIN Routines ON ExerciseRoutines.RoutineID = Routines.RoutineID
                JOIN Exercises ON ExerciseRoutines.ExerciseID = Exercises.ExerciseID
                WHERE Members.UserName = '{userName}'"""
    try:
        return runDBCommand(command)        
    except (Exception, psycopg2.Error) as error:
        print(f"\033[91mFailed to get favourite exercise routines. Error: \033[0m", error)

def addFavouriteRoutine(userName, routineName):
    memberID = getMemberID(userName)
    routineID = getRoutineID(routineName.lower())

    # Error checking on returned memberID and routineID, error is printed in getter functions
    if ("ERROR" in str(memberID) or "ERROR" in str(routineID)):
        return
    
    # Adds the favourite routine if the routine doesn't already exist for that memberID
    command = f"""INSERT INTO FavouriteRoutines (MemberID, RoutineID)
                VALUES ({memberID}, {routineID})
                ON CONFLICT DO NOTHING;  
                """
    try:
        runDBCommand(command)
        # If doesn't error, it successfully added it, since input is validated prior to call
        print(f"\033[92mSuccessfully added '{routineName}' routine to favourites!\033[0m")
    except (Exception, psycopg2.Error) as error:
        print(f"\033[91mFailed to add '{routineName}' routine to favourites. Error: \033[0m", error)

def removeFavouriteRoutine(userName, routineName):
    memberID = getMemberID(userName)
    routineID = getRoutineID(routineName.lower())
    
    # Error checking on returned memberID and routineID, error is printed in getter functions
    if ("ERROR" in str(memberID) or "ERROR" in str(routineID)):
        return

    command = f"""DELETE FROM FavouriteRoutines 
                WHERE MemberID = '{memberID}' AND RoutineID = '{routineID}';
                """
    try:
        runDBCommand(command)
        # If doesn't error, it successfully removed it, since input is validated prior to call
        print(f"\033[92mSuccessfully removed '{routineName}' routine from favourites!\033[0m")
    except (Exception, psycopg2.Error) as error:
        print(f"\033[91mFailed to remove '{routineName}' routine from favourites. Error: \033[0m", error)

def displayFavouriteRoutines(userName):
    favouriteRoutines = getFavouriteRoutines(userName)
    if favouriteRoutines:
        print("\033[33m-Favourite Exercise Routines-\033[0m")
        uniqueFavRoutines = {}
        # Create dictionary of unique routines, since returned data from DB has duplicate routine names due to the nature of linking tables.
        for routine, exercise in favouriteRoutines:
            if routine not in uniqueFavRoutines:
                uniqueFavRoutines[routine] = []
            uniqueFavRoutines[routine].append(exercise)

        for key in uniqueFavRoutines:
            print(f"Routine Name: {key}")
            for exercise in uniqueFavRoutines[key]:
                print(f"    {exercise}")

def displayAllExerciseRoutines():
    routines = getExerciseRoutines()
    if routines:
        print("\033[33m-All Exercise Routines-\033[0m")
        prevRoutine = routines[0][0]
        print(f"Routine Name: {prevRoutine}")
        for routine, exercise in routines:            
            if (routine != prevRoutine):
                print(f"Routine Name: {routine}")
            else:
                print(f"    {exercise}")
            prevRoutine = routine

def displayMemberAchievements(userName):
    achievements = None
    command = f"""SELECT AchievementType, DateAchieved  
                FROM MemberAchievements
                JOIN Members ON MemberAchievements.MemberID = Members.MemberID
                WHERE Members.UserName = '{userName}';"""
    try:
        achievements = runDBCommand(command)        
    except (Exception, psycopg2.Error) as error:
        print(f"\033[91mFailed to get member achievements. Error: \033[0m", error)

    if achievements:
        print(f"\033[33m-Achievements for {userName}-\033[0m")
        for achievementType, dateAchieved in achievements:
            print(f"{achievementType}! Achieved: {dateAchieved}.")
    else:
        print(f"{userName} has no recorded achievements.")

def displayMemberHealthMetrics(userName):
    metrics = None
    command = f"""SELECT MetricName, MetricValue, DateRecorded
                FROM MemberHealthMetrics
                JOIN Members ON MemberHealthMetrics.MemberID = Members.MemberID
                WHERE Members.UserName = '{userName}';"""
    try:
        metrics = runDBCommand(command)  
    except (Exception, psycopg2.Error) as error:
        print(f"\033[91mFailed to get member health metrics. Error: \033[0m", error)

    if metrics:
        print(f"\033[33m-Health Metrics for {userName}-\033[0m")
        for metricName, metricValue, dateRecorded in metrics:
            print(f"{metricName}: {metricValue} (Recorded: {dateRecorded})") 
    else:
        print(f"{userName} has no recorded health metrics.")

def displayMemberGoals(userName):
    goals = None
    command = f"""SELECT GoalType, CurrentValue, TargetValue, StartDate, TargetDate FROM MemberGoals 
                JOIN Members ON MemberGoals.MemberID = Members.MemberID
                WHERE Members.UserName = '{userName}';
                """
    try:
        goals = runDBCommand(command)        
    except (Exception, psycopg2.Error) as error:
        print(f"\033[91mDB failed to get Member's goals. Error: \033[0m", error)
        return

    if goals:
        print(f"\033[33m-Goals for {userName}-\033[0m")
        for goal in goals:
            print("-" * 40)  # Optional separator between goals            
            print("Goal Type:", goal[0])
            print("Current Value:", goal[1])
            print("Target Value:", goal[2])
            print("Start Date:", goal[3])
            print("Target Completion Date:", goal[4])
        return True
    else:
        print(f"{userName} has no goals recorded.")
        return False


def addMemberGoal(userName,goalType,currentVal,targetVal,startDate,targetDate):
    command = f"""INSERT INTO MemberGoals (MemberID, GoalType, CurrentValue, TargetValue, StartDate, TargetDate)
                VALUES ((SELECT MemberID FROM Members WHERE UserName = '{userName}'), '{goalType}', '{currentVal}', '{targetVal}', '{startDate}', '{targetDate}'); 
                """
    try:
        runDBCommand(command)
        # If doesn't error, it successfully added it, since input is validated prior to call
        print(f"\033[92mGoal '{goalType}' added successfully for {userName}!\033[0m")
    except (Exception, psycopg2.Error) as error:
        print(f"\033[91mFailed to add goal '{goalType}' for {userName}. Error: \033[0m", error)


def removeMemberGoal(userName, goalType):
    command = f"""DELETE FROM MemberGoals
                WHERE MemberID = (SELECT MemberID FROM Members WHERE UserName = '{userName}')
                AND LOWER(GoalType) = '{goalType.lower()}';
                """
    try:
        runDBCommand(command)
        # If doesn't error, it successfully removed it, since input is validated prior to call
        print(f"\033[92mSuccessfully removed goal '{goalType}' for {userName}!\033[0m")
    except (Exception, psycopg2.Error) as error:
        print(f"\033[91mFailed to remove goal '{goalType}' for {userName}.  Error: \033[0m", error)

def addMemberAchievement(userName,goalName,achievementDate):
    goal = getMemberGoal(userName,goalName)
    achievement = None

    if goal != None:
        goalName = goal[0][2]
        goalCurrentValue = goal[0][3]
        goalTargetValue = goal[0][4]
        achievement = goalName + ", " + goalCurrentValue + " -> " + goalTargetValue

    command = f"""INSERT INTO MemberAchievements (MemberID, AchievementType, DateAchieved)
                VALUES ((SELECT MemberID FROM Members WHERE UserName = '{userName}'), '{achievement}', '{achievementDate}');
                """
    try:
        runDBCommand(command)
        # If doesn't error, it successfully added it, since input is validated prior to call
        print(f"\033[92mAchievement '{achievement}' added successfully for {userName}!\033[0m")
    except (Exception, psycopg2.Error) as error:
        print(f"\033[91mFailed to add achievement '{achievement}' for {userName}. Error: \033[0m", error)

def addMemberHealthMetrics(userName,metricName,metricValue,dateRecorded):
    command = f"""INSERT INTO MemberHealthMetrics (MemberID, MetricName, MetricValue, DateRecorded)
                VALUES ((SELECT MemberID FROM Members WHERE UserName = '{userName}'), '{metricName}', '{metricValue}', '{dateRecorded}');
                """
    try:
        runDBCommand(command)
        # If doesn't error, it successfully added it, since input is validated prior to call
        print(f"\033[92mHealth metric '{metricName}' added successfully for {userName}!\033[0m")
    except (Exception, psycopg2.Error) as error:
        print(f"\033[91mFailed to add health metric '{metricName}' for {userName}. Error: \033[0m", error)

def scheduleMemberPTSession():
    #Show available PT sessions, get user input on which one theyd like to register for
    print('function not yet implemented.')

def rescheduleMemberPTSession():
    print('function not yet implemented.')

def cancelMemberPTSession():
    print('function not yet implemented.')

def scheduleMemberGroupFitness():
    #Show available fitness classes, get user input on which one theyd like to register for
    print('function not yet implemented.')

def unscheduleMemberGroupFitness():
    print('function not yet implemented.')

### TRAINER FUNCTIONS ###
# This function adds the new trainer into the Trainers table in the database
def registerTrainer(firstName,lastName,email,phone,address,DOB,userName,password,certifications):
    command = f"INSERT INTO Trainers (Password,UserName,FirstName,LastName,Email,Phone,Address,DateOfBirth,Certifications,RegistrationDate)\
    \nVALUES('{password}','{userName}','{firstName}','{lastName}','{email}','{phone}','{address}','{DOB}','{certifications}',CURRENT_DATE)"
    try:
        runDBCommand(command)        
        print("\033[92mTrainer account successfully created!\033[0m")
        return True
    except (Exception, psycopg2.Error) as error:
        print("\033[91mFailed to create new Trainer account. Error: \033[0m", error)

# Function adds/updates a trainer's availability
def setAvailableTrainingTimes(userName):
    trainerId = getTrainerID(userName)
    # get day of the week and time range
    dayOfWeek = input("\nEnter the day of the week: ")
    startTime = input("\nEnter start time of availability: ")
    endTime = input("\nEnter end time of availability: ")

    # connect to db
    conn = connectToDB()
    try:
        if conn:
            cursor = conn.cursor()

            # check if the the trainer currently has availability on this day
            check = (f"SELECT AvailabilityID FROM TrainerAvailability\nWHERE TrainerID = '{trainerId}' AND DayOfWeek = '{dayOfWeek}'")
            cursor.execute(check)
            availability = cursor.fetchone()

            # if trainer has availability on this day, update start time and end time
            if availability:
                updateAvailability = (f"UPDATE TrainerAvailability\
                                      \nSET StartTime = '{startTime}', EndTime = '{endTime}'\
                                      \nWHERE AvailabilityID = '{availability[0]}'")
                cursor.execute(updateAvailability)
                print("Availability updated successfully.")
            
            else:
                # if trainer does not have availability this day, insert new entry into table
                insertAvailability = (f"INSERT INTO TrainerAvailability (TrainerID, DayOfWeek, StartTime, EndTime)\
                                      \nVALUES ('{trainerId}', '{dayOfWeek}', '{startTime}', '{endTime}')")
                cursor.execute(insertAvailability)
                print("Availability added successfully")

            # commit transaction and close cursor and connection
            conn.commit()
            cursor.close()
            conn.close()
    
    except (Exception, psycopg2.Error) as error:
        print("\033[91mError setting available training times:\033[0m", error)

# Function removes the availability from the TrainerAvailability with the matching trainerID and dayOfWeek
def removeAvailableTime(userName):
    trainerId = getTrainerID(userName)
    # get desired day of the week from user
    dayOfWeek = input("\nEnter the day of the week: ").lower()

    # connect to DB
    conn = connectToDB()
    try:
        if conn:
            # create cursor
            cursor = conn.cursor()
            # check if trainer with trainerId parameter has availability on dayOfWeek
            check = (f"SELECT AvailabilityID FROM TrainerAvailability\
                     \nWHERE TrainerID = '{trainerId}' AND LOWER(DayOfWeek) = '{dayOfWeek}'")
            cursor.execute(check)
            availability = cursor.fetchone()

            if availability:
                # remove availability entry
                remove = (f"DELETE FROM TrainerAvailability\
                          \nWHERE AvailabilityID = '{availability[0]}'")
                cursor.execute(remove)
                print(f"Availability on {dayOfWeek} has been removed successfully.")
            else:
                print(f"\nTrainer does not have availibility on {dayOfWeek}.")
            
            # commit commands and close connections
            conn.commit()
            cursor.close()
            conn.close()

    except(Exception, psycopg2.Error) as error:
        print("\033[91mError removing availability.\033[0m", error)

def viewMemberProfile(userName):
    trainerId = getTrainerID(userName)
    firstName = input("Enter member's first name: ")
    lastName = input("Enter member's last name: ")
    
    #may need to retrieve member ID depending on member function implementation

    print(f"Name: {firstName} {lastName}: \n")
    # displayMemberHealthMetrics(firstName, lastName)
    # displayMemberGoals(firstName, lastName)
    # displayMemberAchievements(firstName, lastName)
    # displayExerciseRoutines(firstName, lastName)
    # displayFavouriteRoutines(firstName, lastName)
    
def createExerciseRoutine():
    # prompt user for routine name
    routineName = input("\nEnter the name of the new routine: ")

    try:
        # connect to db
        conn = connectToDB()

        if conn:
            cursor = conn.cursor()

            # Insert routineName into Routines table
            cursor.execute("""INSERT INTO Routines (RoutineName)\nVALUES (%s)""", (routineName,))
            conn.commit()

            # retrieve routineid for newly added routine
            cursor.execute("SELECT LASTVAL()")
            routineId = cursor.fetchone()[0]

            print("\033[33mExerciseID - ExerciseName\033[0m")
            # List exerciseId and exerciseNames from the Exercises table
            cursor.execute("SELECT ExerciseID, ExerciseName FROM Exercises")
            exercises = cursor.fetchall()
            for exercise in exercises:
                print(f"{exercise[0]} - {exercise[1]}")

            # Prompt user to choose exercises
            chosenExercises = []
            exerciseId = None
            while exerciseId != 0:
                exerciseId = int(input("Enter ExerciseID to add (0 to exit): "))
                if exerciseId != 0:
                    chosenExercises.append(exerciseId)
            
            # Add rows to the ExerciseRoutines table
            for exerciseId in chosenExercises:
                cursor.execute("""INSERT INTO ExerciseRoutines (RoutineID, ExerciseID)
                               \nVALUES (%s, %s)""", (routineId, exerciseId))
            
            # Commit the transaction
            conn.commit()
            print("Exercise routine created successfully.")

            # Close cursor and connection
            cursor.close()
            conn.close()

    except (Exception, psycopg2.Error) as error:
        print("\033[91mError creating exercise routine:\033[0m", error)

def displayTrainerNames():
    try:
        command = """SELECT TrainerID, FirstName, LastName FROM Trainers"""
        trainers = runDBCommand(command)

        if trainers:
            print("Trainers:")
            for trainer in trainers:
                print(f"{trainer[1]} {trainer[2]}, ID: {trainer[0]}")
        else:
            print("No trainers found.")
        return len(trainers)
    except (Exception, psycopg2.Error) as error:
        print(f"DB error: {error}")
        return None


### STAFF FUNCTIONS ###
# This function adds the new staff into the Staff table in the database
def registerStaff(firstName,lastName,email,phone,address,DOB,userName,password,jobTitle):
    command = f"INSERT INTO Staff (Password,UserName,FirstName,LastName,Email,Phone,Address,DateOfBirth,JobTitle,RegistrationDate)\
    \nVALUES('{password}','{userName}','{firstName}','{lastName}','{email}','{phone}','{address}','{DOB}','{jobTitle}',CURRENT_DATE)"
    try:
        runDBCommand(command)        
        print("\033[92mStaff account successfully created!\033[0m")
        return True
    except (Exception, psycopg2.Error) as error:
        print("\033[91mFailed to create new Staff account. Error: \033[0m", error)    

def bookARoom(roomID, startTime, endTime, date):
    try:
        command = f"""SELECT StartDateTime, EndDateTime FROM RoomBookings
                      WHERE RoomID = {roomID}
                      AND dayOfBooking = '{date}'"""
        bookings = runDBCommand(command)
        
        if bookings:
            for row in bookings:
                startTimeOld, endTimeOld = row
                #checks if either first start/end times are overlapped the second start/end times
                if timeOverlap(startTime, endTime, startTimeOld, endTimeOld):
                    print("Cannot create booking. This booking overlaps with an existing booking.")
                    return False
        
        #insert the new booking
        command2 = f"""INSERT INTO RoomBookings (RoomID, dayOfBooking, StartDateTime, EndDateTime)
                             VALUES ({roomID}, '{date}', '{startTime}', '{endTime}')"""
        runDBCommand(command2)

        print("Booking success for room " + roomID + " at " + date + ", from " + startTime + " until " + endTime + ".")
    except (Exception, psycopg2.Error) as error:
        print(f"DB error: {error}")
    
    return True
 
def displayRooms():
    rooms = None
    command = f"""SELECT * FROM Rooms;"""
    try:
        rooms = runDBCommand(command)        
    except (Exception, psycopg2.Error) as error:
        print(f"\033[91mDB failed to get rooms. Error: \033[0m", error)
        return None
    if rooms:
        print("\nAvaliable Rooms:")
        for room in rooms:

            #try catch to get room avaliability 
            try:
                command2 = f"""SELECT dayOfBooking, StartDateTime, EndDateTime 
                           FROM RoomBookings
                           WHERE RoomID = {room[0]}"""
                bookedTimes = runDBCommand(command2)
            except (Exception, psycopg2.Error) as error:
                print(f"\033[91mDB failed to get room bookings. Error: \033[0m", error)
                return
            
            print(f"Room #{room[0]}, {room[1]}. Max Capacity: {room[2]}")
            if bookedTimes:
                print(f"     Room available any time outside of:", end="")
                for index, (bookedDay, startTime, endTime) in enumerate(bookedTimes):
                    if index == 0:
                        print(f" {startTime}-{endTime} on {bookedDay}", end="")
                    else:
                        print(f", {startTime}-{endTime} on {bookedDay}", end="")
                print()#for new line
            else:
                print("     Room available all times.")
    else:
        print("No rooms found.")
    #returns amount of rooms
    return len(rooms)

def displayEquipmentStatus():
    status = None
    command = f"""SELECT *FROM Equipment;"""
    try:
        status = runDBCommand(command)        
    except (Exception, psycopg2.Error) as error:
        print("failed to fetch equipment status", error)
        return

    if status:
        print("State of Equipment:")
        for equipment in status:        
            print("Equipment: " + equipment[1] + ", ID: " + str(equipment[0]) + ", and needs maintenance? " + str(equipment[2]))
    else:
        print("No equipment status available.")
    input("Press Enter to return to Staff commands.")

def addClassSchedule(trainerID, classID, roomID,date, startTime, endTime):
    try:

        dayOfWeek = daysOfWeek[date - 1]

        print("dayOfweek: " + dayOfWeek)
        command = f"""INSERT INTO ClassSchedules (TrainerID, ClassID, RoomID, DayOfWeek, StartTime, EndTime)
                     VALUES ('{trainerID}', '{classID}', '{roomID}', '{dayOfWeek}', '{startTime}', '{endTime}')"""
        runDBCommand(command)
        print("Class scheduled successfully.")
        return True

    except (Exception, psycopg2.Error) as error:
        print(f"DB error: {error}")
        return False

def paymentTransaction(memberName, dateToday, amount, purchaseType):
    command = f"""INSERT INTO Payments (MemberID, InvoiceDate, Amount, ProductPurchased) 
             VALUES ('{getMemberID(memberName)}', '{dateToday}', '{amount}', '{purchaseType}')"""
    try:
        runDBCommand(command)
        print("\033[92mPayment successfuly processed!\033[0m")
        return True
    except (Exception, psycopg2.Error) as error:
        print("\033[91mFailed to process payment. Error: \033[0m", error)               
        return False
    
def addEquipment(name, needsMaintenance):
    command = f"""INSERT INTO Equipment (EquipmentName, NeedsMaintenance)
                VALUES ('{name}', {needsMaintenance});"""
    runDBCommand(command)
    print("Equipment successfully added.")

def addEquipmentMaintenanceRequest(equipmentName, equipmentMaintenanceDesc, maintenanceDate):
    equipmentID = getEquipmentID(equipmentName)
    if equipmentID is not None:
        try:
            command = f"""INSERT INTO EquipmentMaintenanceRequests (EquipmentID, Description, MaintenanceDate)
                          VALUES ( '{equipmentID}', '{equipmentMaintenanceDesc}', '{maintenanceDate}')"""
            runDBCommand(command)
            input("Equipment maintenance request successfully sent for " + equipmentName +". Press enter to return to staff commands.")
            return True
        except (Exception, psycopg2.Error) as error:
            print(f"DB error: {error}")
    else:
        return False

def displayEquipmentMaintenanceRequests():



    try:
        command = """SELECT EquipmentID, Description, MaintenanceDate
        FROM EquipmentMaintenanceRequests
        """
        requests = runDBCommand(command)

        if requests:
            for row in requests:
                eIDs = row[0]
                eDesc = row[1]
                maintenanceDate = row[2]
                print(getEquipmentName(eIDs) + ", reason for maintenance: " + eDesc +". Maintenance date: " + str(maintenanceDate))
        else:
            print("No maintenance requests found.")

    except (Exception, psycopg2.Error) as error:
        print(f"DB error: {error}")
        print("ERROR: No maintenance requests could be found.")
    input("Press any key to return to staff commands.\n")

def displayClasses():
    try:
        command = """SELECT ClassID, ClassName, MaxCapacity FROM Classes"""
        classes = runDBCommand(command)
        
        if classes:
            print("Available Classes:")
            for classData in classes:
                classID, className, maxCap = classData
                print(f"Class ID: {classID}, Name: {className}, Max Capacity: {maxCap}")
        else:
            print("No classes found.")
        return len(classes)
    except (Exception, psycopg2.Error) as error:
        print(f"DB error: {error}")
        return None

