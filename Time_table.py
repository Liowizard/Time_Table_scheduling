from ortools.sat.python import cp_model

def create_timetables():
    # Create the CP model
    model = cp_model.CpModel()

    # Define the variables
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    subjects = {
        'Mathematics': [60, "theory"],
        'Physics': [60, "theory"],
        'Chemistry': [60, "theory"],
        'English': [60, "theory"],
        'History': [60, "theory"],
        'Bio': [60, "theory"],
        'Physics_Lab': [90, "Lab"],
        'Chemistry_Lab': [60, "Lab"]
    }
    sections = ['sec_A', 'sec_B', 'sec_C']
    subject_teachers = {
        'Mathematics': ['Doris Wilson', 'Amy Smith'],
        'Physics': ['Mrs. A. T. Whitecotton', 'Geraldine Carpenter'],
        'Chemistry': ['Edna Francis', 'Sarah Norris'],
        'English': ['Jennie Crigler', 'Gladys Swon'],
        'History': ['Ruth Carman', 'Lela Pat Buckman'],
        'Bio': ['Lio', 'Fin'],
        'Physics_Lab': ['Mrs. A. T. Whitecotton', 'Geraldine Carpenter'],
        'Chemistry_Lab': ['John Doe', 'Jane Smith']
    }
    slots_per_day = 8  # Total number of hours
    slots_per_week = slots_per_day * len(days)
    minutes_per_day = 480  # Maximum minutes per day

    # Create the variables for each subject in each time slot, section, and teacher
    timetable = {}
    for day in days:
        for slot in range(slots_per_day):
            for subject in list(subjects.keys()):
                for section in sections:
                    for teacher in subject_teachers[subject]:
                        if (day, slot, subject, section, teacher) not in timetable:
                            for i in range(slots_per_day):
                                if (day, slot + i, subject, section, teacher) not in timetable:
                                    timetable[(day, slot + i, subject, section, teacher)] = model.NewBoolVar(
                                        '{}_{}_{}_{}_{}'.format(day, slot + i, subject, section, teacher))

    # Add constraints...

    # Each subject should have the required number of classes per week
    for subject in list(subjects.keys()):
        if subject not in ['Physics_Lab', 'Chemistry_Lab']:
            for section in sections:
                model.Add(sum(timetable[(day, slot, subject, section, teacher)]
                              for day in days for slot in range(slots_per_day) for teacher in subject_teachers[subject]) == 5)

    # Lab subjects should be scheduled once in 5 days for each section
    for subject in ['Physics_Lab', 'Chemistry_Lab']:
        for section in sections:
            model.Add(sum(timetable[(day, slot, subject, section, teacher)]
                          for day in days for slot in range(slots_per_day) for teacher in subject_teachers[subject]) == 1)

    # No two classes should be scheduled at the same time
    for day in days:
        for slot in range(slots_per_day):
            for section in sections:
                model.Add(sum(timetable[(day, slot, subject, section, teacher)]
                                 for subject in list(subjects.keys()) for teacher in subject_teachers[subject]) <= 1)

    # Each subject can be scheduled at most two times per day, with reduced repetition
    for day in days:
        for subject in list(subjects.keys()):
            for section in sections:
                for teacher in subject_teachers[subject]:
                    if subject in ['Physics_Lab', 'Chemistry_Lab']:
                        model.Add(sum(timetable[(day, slot, subject, section, teacher)]
                                      for slot in range(slots_per_day)) <= 1)
                    else:
                        model.Add(sum(timetable[(day, slot, subject, section, teacher)]
                                      for slot in range(slots_per_day)) <= 2)

    # Teachers should not be assigned to multiple classes at the same time
    for day in days:
        for slot in range(slots_per_day):
            for teacher in set(sum(subject_teachers.values(), [])):
                for section in sections:
                    model.Add(sum(timetable[(day, slot, subject, section, teacher)]
                                 for subject in list(subjects.keys()) if teacher in subject_teachers[subject]) <= 1)

    # Avoid consecutive classes for the same subject and section
    for day in days:
        for section in sections:
            for subject in list(subjects.keys()):
                for teacher in subject_teachers[subject]:
                    for slot in range(slots_per_day - 1):
                        if (day, slot, subject, section, teacher) in timetable and (day, slot + 1, subject, section, teacher) in timetable:
                            model.Add(timetable[(day, slot, subject, section, teacher)] + timetable[(day, slot + 1, subject, section, teacher)] <= 1)

    # Create the solver and solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Generate the timetables as dictionaries
    timetables = {}
    if status == cp_model.OPTIMAL:
        for section in sections:
            timetable_section = {}
            for day in days:
                timetable_day = {}
                total_minutes = 0  # Track the total minutes scheduled in a day
                for slot in range(slots_per_day):
                    timetable_slot = {}
                    for subject in list(subjects.keys()):
                        timetable_subject = []
                        for teacher in subject_teachers[subject]:
                            if solver.Value(timetable[(day, slot, subject, section, teacher)]):
                                duration = subjects[subject][0]
                                total_minutes += duration
                                if total_minutes <= minutes_per_day:  # Check if total minutes exceed the limit
                                    timetable_subject.append({
                                        'teacher': teacher,
                                        'duration': duration,
                                        'type': subjects[subject][1]
                                    })
                                else:
                                    total_minutes -= duration  # Exclude the current slot from exceeding the limit
                        timetable_slot[subject] = timetable_subject
                    timetable_day[slot] = timetable_slot
                timetable_section[day] = timetable_day
            timetables[section] = timetable_section

    return timetables


# Example usage
timetables = create_timetables()

if timetables is not None:
    for section, timetable_section in timetables.items():
        print(f"Timetable for section {section}:")
        for day, timetable_day in timetable_section.items():
            print(f"Day: {day}")
            for slot, timetable_slot in timetable_day.items():
                print(f"Slot: {slot}")
                for subject, classes in timetable_slot.items():
                    for cls in classes:
                        if cls['teacher']:
                            print(f"Subject: {subject}")
                            print(f"  Teacher: {cls['teacher']}, Duration: {cls['duration']}, Type: {cls['type']}")
                print()
            print()
else:
    print("No feasible solution found.")

