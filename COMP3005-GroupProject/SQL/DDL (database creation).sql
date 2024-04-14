CREATE TABLE Members (
    MemberID SERIAL PRIMARY KEY,
    Password VARCHAR(50) NOT NULL,
    UserName VARCHAR(50) NOT NULL UNIQUE,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(50) NOT NULL,
    Phone VARCHAR(50), 
    Address VARCHAR(50),
    DateOfBirth DATE NOT NULL,
    RegistrationDate DATE NOT NULL
);

CREATE TABLE Trainers (
    TrainerID SERIAL PRIMARY KEY,
    Password VARCHAR(50) NOT NULL, 
    UserName VARCHAR(50) NOT NULL UNIQUE,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(50) NOT NULL,
    Phone VARCHAR(50),
    Address VARCHAR(50),
    DateOfBirth DATE NOT NULL,
    Certifications TEXT,
	RegistrationDate DATE NOT NULL
);

CREATE TABLE Staff (
    StaffID SERIAL PRIMARY KEY,
    Password VARCHAR(50) NOT NULL, 
    UserName VARCHAR(50) NOT NULL UNIQUE,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(50) NOT NULL,
    Phone VARCHAR(50) NOT NULL,
    Address VARCHAR(50) NOT NULL,
    DateOfBirth DATE NOT NULL,
    JobTitle VarChar(50) NOT NULL,
	RegistrationDate DATE NOT NULL
);

CREATE TABLE Exercises (
    ExerciseID SERIAL PRIMARY KEY,
    ExerciseName VARCHAR(50) NOT NULL
);

CREATE TABLE Routines (
    RoutineID SERIAL PRIMARY KEY,
    RoutineName VARCHAR(50) NOT NULL 
);

CREATE TABLE Rooms (
	RoomID SERIAL PRIMARY KEY,
	RoomName VARCHAR(50) NOT NULL,
	MaxCapacity INTEGER
);

CREATE TABLE Equipment (
	EquipmentID SERIAL PRIMARY KEY,
	EquipmentName VARCHAR(50) NOT NULL,
	NeedsMaintenance BOOLEAN DEFAULT FALSE
);

--
-- LINKING TABLES 
-- 

CREATE TABLE MemberHealthMetrics (
	MemberMetricID SERIAL PRIMARY KEY,
	MemberID INTEGER NOT NULL,
    MetricName VARCHAR(50) NOT NULL,
	MetricValue VARCHAR(50) NOT NULL,
	DateRecorded DATE NOT NULL,
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);

CREATE TABLE MemberGoals (
    GoalID SERIAL PRIMARY KEY,
    MemberID INTEGER NOT NULL,
    GoalType VARCHAR(50) NOT NULL, 
    CurrentValue VARCHAR(50),
    TargetValue VARCHAR(50),
    StartDate DATE,
    TargetDate DATE,
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);

CREATE TABLE MemberAchievements (
	AchievementID SERIAL PRIMARY KEY,
	MemberID INTEGER NOT NULL,
	AchievementType VARCHAR(150) NOT NULL,
	DateAchieved DATE NOT NULL,
	FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);

CREATE TABLE Classes (
	ClassID SERIAL PRIMARY KEY,
	TrainerID INTEGER NOT NULL,
	ClassName VARCHAR(50) NOT NULL,
	MaxCapacity INTEGER,
	FOREIGN KEY (TrainerID) REFERENCES Trainers(TrainerID) 
);

CREATE TABLE TrainerAvailability (
	AvailabilityID SERIAL PRIMARY KEY,
	TrainerID INTEGER NOT NULL,
	DayOfWeek VARCHAR(50) NOT NULL,
	StartTime VARCHAR(50) NOT NULL,
	EndTime VARCHAR(50) NOT NULL,
  	FOREIGN KEY (TrainerID) REFERENCES Trainers(TrainerID)
);

CREATE TABLE PTSessionRegistrations (
    SessionID SERIAL PRIMARY KEY,
	TrainerID INTEGER NOT NULL,
    MemberID INTEGER NOT NULL,
	RoomID INTEGER NOT NULL,
    SessionDate DATE NOT NULL,
	SessionTime TIMESTAMP NOT NULL,
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID),
	FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID),
    FOREIGN KEY (TrainerID) REFERENCES Trainers(TrainerID)
);

CREATE TABLE ClassSchedules (
    ScheduleID SERIAL PRIMARY KEY,
    TrainerID INTEGER NOT NULL, 
    ClassID INTEGER NOT NULL,
    RoomID INTEGER NOT NULL,
    DayOfWeek VarChar(20) NOT NULL,
    StartTime VARCHAR(20) NOT NULL,
	EndTime VARCHAR(20) NOT NULL,
    FOREIGN KEY (TrainerID) REFERENCES Trainers(TrainerID),
    FOREIGN KEY (ClassID) REFERENCES Classes(ClassID),
    FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID)
);

CREATE TABLE ClassRegistrations (
    RegistrationID SERIAL PRIMARY KEY,
    MemberID INTEGER NOT NULL,
    ScheduleID INTEGER NOT NULL,
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID),
    FOREIGN KEY (ScheduleID) REFERENCES ClassSchedules(ScheduleID)
);

CREATE TABLE RoomBookings (
    BookingID SERIAL PRIMARY KEY,
    RoomID INTEGER NOT NULL,
    dayOfBooking VarChar(20) NOT NULL,
    StartDateTime VarChar(20) NOT NULL,
    EndDateTime VarChar(20) NOT NULL,
    FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID) 
);

CREATE TABLE ExerciseRoutines (
    ExerciseRoutineID SERIAL PRIMARY KEY,
    RoutineID INTEGER NOT NULL,
    ExerciseID INTEGER NOT NULL,
    FOREIGN KEY (RoutineID) REFERENCES Routines(RoutineID),
    FOREIGN KEY (ExerciseID) REFERENCES Exercises(ExerciseID)
);

CREATE TABLE FavouriteRoutines (
    FavouriteRoutineID SERIAL PRIMARY KEY,
    MemberID INTEGER NOT NULL,
    RoutineID INTEGER NOT NULL,
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID),
    FOREIGN KEY (RoutineID) REFERENCES Routines(RoutineID)
);

CREATE TABLE EquipmentMaintenanceRequests (
    MaintenanceID SERIAL PRIMARY KEY,
    EquipmentID INTEGER NOT NULL,
	Description TEXT,
    MaintenanceDate DATE,
    FOREIGN KEY (EquipmentID) REFERENCES Equipment(EquipmentID) 
);

CREATE TABLE Payments (
    paymentID SERIAL PRIMARY KEY,
    MemberID INTEGER NOT NULL,
    InvoiceDate DATE NOT NULL,
    Amount NUMERIC NOT NULL,
    ProductPurchased VARCHAR(150),
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID) 
);
