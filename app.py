from ortools.sat.python import cp_model

def create_timetable():
    # Create the CP model
    model = cp_model.CpModel()

    # Define the variables
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    time_slots = ['1st_period', '2nd_period', '3rd_period', '4th_period', '5th_period', '6th_period', '7th_period', '8th_period']
    subjects = ['Mathematics', 'Physics', 'Chemistry', 'English', 'History', 'Physics_lab']
    slots_per_day = len(time_slots)
    days_per_week = len(days)
    slots_per_week = slots_per_day * days_per_week

    # Create the variable for each subject in each time slot
    timetable = {}
    for day in days:
        for slot in time_slots:
            for subject in subjects:
                timetable[(day, slot, subject)] = model.NewBoolVar('{}_{}_{}'.format(day, slot, subject))

    # Add constraints

    # Each subject should have exactly five classes per week, except for Physics_lab (scheduled twice a week)
    for subject in subjects:
        if subject == 'Physics_lab':
            model.Add(sum([timetable[('Wednesday', '3rd_period', subject)], timetable[('Wednesday', '4th_period', subject)]]) == 2)
        else:
            model.Add(sum(timetable[(day, slot, subject)] for day in days for slot in time_slots) == 5)

    # No two classes should be scheduled in the same time slot
    for day in days:
        for slot in time_slots:
            model.Add(sum(timetable[(day, slot, subject)] for subject in subjects) <= 1)

    # Each subject can be scheduled at most two times per day
    for day in days:
        for subject in subjects:
            model.Add(sum(timetable[(day, slot, subject)] for slot in time_slots) <= 2)

    # Create the solver and solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        # Print the timetable
        for day in days:
            print(day)
            for slot in time_slots:
                print(slot)
                for subject in subjects:
                    if solver.Value(timetable[(day, slot, subject)]):
                        print(subject)
                print('---')
            print('========')

create_timetable()
