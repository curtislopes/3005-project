INSERT INTO Members (Password, UserName, FirstName, LastName, Email, Phone, Address, DateOfBirth, RegistrationDate)
VALUES
    ('password1', 'JohnDoe', 'John', 'Doe', 'john.doe@email.com', '613-123-4567', '123 Main Street', '1985-05-20', CURRENT_DATE),
    ('password2', 'AlexWilliams', 'Alex', 'Williams', 'alex.williams@email.com', '613-987-6543', '456 Elm Street', '1990-01-15', CURRENT_DATE),
	('password3', 'LiamLetourneau', 'Liam', 'Letourneau', 'liam.letourneau@email.com', '613-111-2222', '100 Win Street', '2001-01-01', CURRENT_DATE),
	('password4', 'AaronLetourneau', 'Aaron', 'Letourneau', 'aaron.letourneau@email.com', '613-333-4444', '200 Win Street', '2003-01-10', CURRENT_DATE),
	('password5', 'CurtisLopes', 'Curtis', 'Lopes', 'curtis.lopes@email.com', '613-555-6666', '300 Win Street', '2003-01-20', CURRENT_DATE);

INSERT INTO Trainers (Password, UserName,  FirstName, LastName, Email, Phone, Address, DateOfBirth, Certifications, RegistrationDate)
VALUES 
    ('trainer1', 'EmilyDavis', 'Emily', 'Davis', 'emily.davis@email.com', '519-321-6547', '789 Oak Street', '1980-10-05', 'ACSM Certified, CPR', CURRENT_DATE),
    ('trainer2', 'JohnMiller', 'John', 'Miller', 'john.miller@email.com', '613-555-1212', '101 Pine Street', '1975-08-18', 'NSCA Certified, ACE CPT', CURRENT_DATE),
	('trainer3', 'KyleBanks', 'Kyle', 'Banks', 'kyle.banks@email.com', '249-124-1123', '110 Pine Street', '1975-08-30', 'NASM Certified, CPR', CURRENT_DATE);

INSERT INTO Staff (Password, UserName,  FirstName, LastName, Email,  Phone, Address, DateOfBirth, JobTitle, RegistrationDate)
VALUES
    ('staff1', 'OliviaTaylor', 'Olivia', 'Taylor', 'olivia.taylor@email.com', '555-456-7890', '321 Broad Street', '1988-02-21', 'Receptionist', CURRENT_DATE),
    ('staff2', 'MichaelBrown', 'Michael', 'Brown', 'michael.brown@email.com', '555-789-3210', '654 Maple Street','1978-06-14', 'Manager', CURRENT_DATE),
	('staff3', 'ChrisTurcot', 'Chris', 'Turcot', 'chris.turcot@email.com', '555-937-1235', '103 Bank Street','1999-06-14', 'Janitor', CURRENT_DATE);

INSERT INTO Exercises (ExerciseName) 
VALUES ('Lat Pulldown'), ('Seated Chest Press'), ('Leg Press'), ('Shoulder Press'), ('Leg Extension'), ('Hamstring Curl'), ('Seated Calf Raise'), ('Tricep Pushdown'), ('Bicep Curl Machine'), ('Seated Row'), ('Abdominal Crunch Machine'), ('Smith Machine Squat'), ('Hamstring Curl Machine'), ('Pec Deck Fly'), ('Hack Squat'), ('Incline Dumbbell Press'), ('Assisted Pull-up Machine'), ('Treadmill'), ('Rope Swings'), ('Spin Bike'); 

INSERT INTO Routines (RoutineName)
VALUES ('Push Day'), ('Pull Day'), ('Leg Day'), ('Cardio Day');

INSERT INTO Rooms (RoomName, MaxCapacity)
VALUES ('Studio Room', 20), ('Yoga Room', 40), ('Cardio Room', 50), ('Weight Room', 100);

INSERT INTO Equipment (EquipmentName, NeedsMaintenance)
VALUES
    ('Treadmill', FALSE),
    ('Elliptical Trainer', FALSE),
    ('Stationary Bike', FALSE),
    ('Leg Press Machine', TRUE),
    ('Chest Press Machine', FALSE),
    ('Shoulder Press Machine', FALSE),
    ('Lat Pulldown Machine', FALSE),
    ('Seated Cable Row Machine', TRUE),
    ('Bicep Curl Machine', FALSE),
    ('Tricep Pushdown Machine', TRUE),
    ('Calf Raise Machine', FALSE),
    ('Abdominal Crunch Machine', FALSE),
    ('Smith Machine', FALSE),
    ('Dumbbell Rack', FALSE);

--
-- INSERTING INTO LINKING TABLES 
--

INSERT INTO MemberHealthMetrics (MemberID, MetricName, MetricValue, DateRecorded)
VALUES
   -- Member 1
   (1, 'Weight', '175 lbs', CURRENT_DATE - INTERVAL '1 week'),
   (1, 'Body Fat Percentage', '22%', CURRENT_DATE - INTERVAL '1 week'),
   (1, 'Resting Heart Rate', '65 BPM', CURRENT_DATE - INTERVAL '1 week'),
   (1, 'Blood Pressure', '125/80 mmHg', CURRENT_DATE - INTERVAL '1 week'),
   (1, 'BMI', '25.5', CURRENT_DATE - INTERVAL '1 week'),
   -- Member 2
   (2, 'Weight', '180 lbs', CURRENT_DATE - INTERVAL '1 month'), 
   (2, 'Body Fat Percentage', '18%', CURRENT_DATE - INTERVAL '1 month'), 
   (2, 'Resting Heart Rate', '72 BPM', CURRENT_DATE - INTERVAL '1 month'), 
   (2, 'Blood Pressure', '130/85 mmHg', CURRENT_DATE - INTERVAL '1 month'), 
   (2, 'BMI', '26.2', CURRENT_DATE - INTERVAL '1 month'), 
   -- Member 3
   (3, 'Weight', '195 lbs', CURRENT_DATE - INTERVAL '3 weeks'),
   (3, 'Body Fat Percentage', '25%', CURRENT_DATE - INTERVAL '3 weeks'),
   (3, 'Resting Heart Rate', '75 BPM', CURRENT_DATE - INTERVAL '3 weeks'),
   (3, 'Blood Pressure', '115/75 mmHg', CURRENT_DATE - INTERVAL '3 weeks'),
   (3, 'BMI', '23.8', CURRENT_DATE - INTERVAL '3 weeks'),
   -- Member 4
   (4, 'Weight', '190 lbs', CURRENT_DATE - INTERVAL '1 week'),
   (4, 'Body Fat Percentage', '20%', CURRENT_DATE - INTERVAL '1 week'),
   (4, 'Resting Heart Rate', '68 BPM', CURRENT_DATE - INTERVAL '1 week'),
   (4, 'Blood Pressure', '120/80 mmHg', CURRENT_DATE - INTERVAL '1 week'),
   (4, 'BMI', '27.1', CURRENT_DATE - INTERVAL '1 week'), 
   -- Member 5
   (5, 'Weight', '200 lbs', CURRENT_DATE - INTERVAL '2 months'),
   (5, 'Body Fat Percentage', '22%', CURRENT_DATE - INTERVAL '2 months'),
   (5, 'Resting Heart Rate', '60 BPM', CURRENT_DATE - INTERVAL '2 months'),
   (5, 'Blood Pressure', '135/85 mmHg', CURRENT_DATE - INTERVAL '2 months'),
   (5, 'BMI', '24.5', CURRENT_DATE - INTERVAL '2 months'); 

INSERT INTO MemberGoals (MemberID, GoalType, CurrentValue, TargetValue, StartDate, TargetDate)
VALUES
    (1, 'Weight Loss', '180lbs', '170lbs', CURRENT_DATE, CURRENT_DATE + INTERVAL '6 months'),
    (2, 'Strength Gain', '150 lbs bench press', '185 lbs bench press', CURRENT_DATE, CURRENT_DATE + INTERVAL '3 months'),
    (3, 'Build Muscle', '15 inch biceps', '16 inch biceps', CURRENT_DATE, CURRENT_DATE + INTERVAL '4 months'),
    (4, 'Improve Flexibility', 'Half Splits', 'Full Splits', CURRENT_DATE, CURRENT_DATE + INTERVAL '3 months'),
    (5, 'Increase Endurance', 'Run 5k', 'Run 10k', CURRENT_DATE, CURRENT_DATE + INTERVAL '2 months');
	
INSERT INTO MemberAchievements (MemberID, AchievementType, DateAchieved)
VALUES
    (1, 'Weight Loss, 200lbs -> 190lbs', CURRENT_DATE - INTERVAL '1 month'),
    (2, 'Strength Gain, 120 lbs bench press -> 150 lbs bench press', CURRENT_DATE - INTERVAL '2 weeks'),
    (3, 'Build Muscle, 14 inch biceps -> 15 inch biceps', CURRENT_DATE - INTERVAL '2 weeks'),
    (4, 'Improve Flexibility, Half Splits -> Full Splits', CURRENT_DATE - INTERVAL '1 month'),
    (5, 'Increase Endurance, Run 3K -> Run 5k', CURRENT_DATE - INTERVAL '1 month');

INSERT INTO Classes (TrainerID, ClassName, MaxCapacity)
VALUES (1, 'Yoga', 15), (2, 'Strength Training', 20), (3, 'Spin Class', 25);

INSERT INTO TrainerAvailability (TrainerID, DayOfWeek, StartTime, EndTime)
VALUES
    -- Trainer 1 Availabilities
    (1, 'Monday', '9:00 AM', '12:00 PM'), 
    (1, 'Wednesday', '2:00 PM', '5:00 PM'),
    (1, 'Friday', '1:00 PM', '4:00 PM'),
    -- Trainer 2 Availabilities
    (2, 'Tuesday', '10:00 AM', '2:00 PM'), 
    (2, 'Thursday', '8:00 AM', '4:00 PM'),
    -- Trainer 3 Availabilities
    (3, 'Wednesday', '3:00 PM', '7:00 PM'),
    (3, 'Saturday', '10:00 AM', '2:00 PM');

INSERT INTO ClassSchedules (TrainerID, ClassID, RoomID, DayOfWeek, StartTime, EndTime)
VALUES
    (1, 1, 2, 'Monday', '9:00 AM', '10:00 AM'),  -- Yoga in Yoga Room
	(1, 1, 2, 'Wednesday', '2:00 PM', '3:00 PM'), -- Yoga in Yoga Room 
    (2, 2, 4, 'Tuesday', '10:00 AM', '12:00 PM'),  -- Strength Training in Weight Room    
	(2, 2, 4, 'Thursday', '10:00 AM', '12:00 PM'), -- Strength Training in Weight Room
    (3, 3, 3, 'Wednesday', '5:00 PM', '7:00 PM'); -- Spin in Cardio Room

-- This could be extended to fill out all of the routines if we want
INSERT INTO ExerciseRoutines (RoutineID, ExerciseID)
VALUES
    -- Push Day
    (1, 2),  -- Seated Chest Press
    (1, 4),  -- Shoulder Press
    (1, 8),  -- Tricep Pushdown
    (1, 16), -- Incline Dumbbell Press
    -- Pull Day
    (2, 1),  -- Lat Pulldown
    (2, 10), -- Seated Row
    (2, 9),  -- Bicep Curl Machine
    (2, 14), -- Pec Deck Fly
    -- Leg Day
    (3, 3),  -- Leg Press
    (3, 12), -- Smith Machine Squat
    (3, 5),  -- Leg Extension
    (3, 6),  -- Hamstring Curl 
    (3, 7),  -- Seated Calf Raise
	-- Cardio Day
    (4, 18),   -- Treadmill
    (4, 19),   -- Rope Swings
    (4, 20);   -- Spin Bike
INSERT INTO FavouriteRoutines (MemberID, RoutineID)
VALUES
    -- Member 1 Favourites
    (1, 1),
    (1, 3),
    -- Member 2 Favourites
    (2, 2),
	-- Member 3 Favourites
    (3, 1),
	(3, 2),
	-- Member 4 Favourites
    (4, 2),
	-- Member 5 Favourites
    (5, 3);

INSERT INTO EquipmentMaintenanceRequests (EquipmentID, Description, MaintenanceDate)
VALUES
    (4, 'Squeaking noise, lubrication required', CURRENT_DATE + INTERVAL '1 day'), -- Leg press
    (8, 'Broken cable', CURRENT_DATE + INTERVAL '1 week'), -- Seated Cable Row
    (10, 'Elbow pad torn open', CURRENT_DATE + INTERVAL '1 week'); -- Tricep pushdown
	
INSERT INTO Payments (MemberID, InvoiceDate, Amount, ProductPurchased)
VALUES
    (1, CURRENT_DATE - INTERVAL '6 months', 340, 'Annual Membership'),
    (2, CURRENT_DATE - INTERVAL '3 months', 180, 'Quarterly Membership'),
    (3, CURRENT_DATE - INTERVAL '1 month', 50, 'Monthly Membership'), 
    (4, CURRENT_DATE - INTERVAL '9 months', 340, 'Annual Membership'),
    (5, CURRENT_DATE - INTERVAL '2 months', 180, 'Quarterly Membership'); 

INSERT INTO RoomBookings (RoomID, dayOfBooking, StartDateTime, EndDateTime)
VALUES
    (1, '2024-04-11', '09:00', '10:30'),
    (1, '2024-04-11', '12:00', '13:00'),
    (1, '2024-04-12', '09:00', '10:30'),
    (2, '2024-04-12', '14:00', '16:00'),
    (3, '2024-04-13', '10:30', '12:00');




