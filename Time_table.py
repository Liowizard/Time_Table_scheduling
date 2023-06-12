from ortools.sat.python import cp_model

def create_timetables():
    # Create the CP model
    model = cp_model.CpModel()

    # Define the variables
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    time_slots = ['1st_period', '2nd_period', '3rd_period', '4th_period', '5th_period', '6th_period', '7th_period', '8th_period']
    subjects = ['Mathematics', 'Physics', 'Chemistry', 'English', 'History', 'Physics_lab', 'Chemistry_lab']
    sections = ['sec_A', 'sec_B']
    slots_per_day = len(time_slots)
    days_per_week = len(days)
    slots_per_week = slots_per_day * days_per_week

    # Create the variables for each subject in each time slot and section
    timetable = {}
    for day in days:
        for slot in time_slots:
            for subject in subjects:
                for section in sections:
                    timetable[(day, slot, subject, section)] = model.NewBoolVar('{}_{}_{}_{}'.format(day, slot, subject, section))

    # Add constraints

    # Each subject should have exactly five classes per week, except for Physics_lab and Chemistry_lab
    for subject in subjects:
        for section in sections:
            if subject == 'Physics_lab':
                model.Add(timetable[('Wednesday', '3rd_period', subject, section)] + timetable[('Wednesday', '4th_period', subject, section)] == 2)
            elif subject == 'Chemistry_lab':
                model.Add(timetable[('Friday', '3rd_period', subject, section)] + timetable[('Friday', '4th_period', subject, section)] == 2)
            else:
                model.Add(sum(timetable[(day, slot, subject, section)] for day in days for slot in time_slots) == 5)

    # No two classes should be scheduled in the same time slot
    for day in days:
        for slot in time_slots:
            for section in sections:
                model.Add(sum(timetable[(day, slot, subject, section)] for subject in subjects) <= 1)

    # Each subject can be scheduled at most two times per day
    for day in days:
        for subject in subjects:
            for section in sections:
                model.Add(sum(timetable[(day, slot, subject, section)] for slot in time_slots) <= 2)

    # Subjects in sec_A and sec_B should be different, except for Physics_lab and Chemistry_lab
    for day in days:
        for slot in time_slots:
            for subject in subjects:
                if subject != 'Physics_lab' and subject != 'Chemistry_lab':
                    model.Add(timetable[(day, slot, subject, 'sec_A')] + timetable[(day, slot, subject, 'sec_B')] <= 1)

    # Create the solvers and solve the models
    solvers = [cp_model.CpSolver() for _ in sections]
    statuses = [solvers[i].Solve(model) for i in range(len(solvers))]

    # Generate the timetables as dictionaries
    timetables = {}
    for i in range(len(sections)):
        section = sections[i]
        solver = solvers[i]
        if statuses[i] == cp_model.OPTIMAL:
            timetable_dict = {}
            for day in days:
                timetable_dict[day] = {}
                for slot in time_slots:
                    timetable_dict[day][slot] = []
                    for subject in subjects:
                        if solver.Value(timetable[(day, slot, subject, section)]):
                            timetable_dict[day][slot].append(subject)
            timetables[section] = timetable_dict

    # Return the timetables as dictionaries
    return timetables

timetables = create_timetables()


# Print the timetables
for section, timetable in timetables.items():
    print(f"Timetable for {section}:")
    for day, slots in timetable.items():
        print(f"\n{day}")
        for slot, subjects in slots.items():
            print(slot, subjects)
