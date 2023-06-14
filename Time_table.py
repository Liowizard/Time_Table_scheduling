from ortools.sat.python import cp_model

def create_timetables():
    # Create the CP model
    model = cp_model.CpModel()

    # Define the variables
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    subjects = ['Mathematics', 'Physics_lab', 'Chemistry', 'English', 'History', 'Bio', 'Chemistry_Lab']
    sections = ['sec_A', 'sec_B', 'sec_C']
    subject_teachers = {
        'Mathematics': ['Doris Wilson', 'Amy Smith'],
        'Physics_lab': ['Mrs. A. T. Whitecotton', 'Geraldine Carpenter'],
        'Chemistry': ['Edna Francis', 'Sarah Norris'],
        'English': ['Jennie Crigler', 'Gladys Swon'],
        'History': ['Ruth Carman', 'Lela Pat Buckman'],
        'Bio': ['Lio', 'Fin'],
        'Chemistry_Lab': ['John Doe', 'Jane Smith']
    }
    slots_per_day = 8  # Total number of hours
    slots_per_week = slots_per_day * len(days)
    start_time = 8  # Start time in AM

    # Create the variables for each subject in each time slot, section, and teacher
    timetable = {}
    for day in days:
        for slot in range(slots_per_day):
            for subject in subjects:
                for section in sections:
                    for teacher in subject_teachers[subject]:
                        if (day, slot, subject, section, teacher) not in timetable:
                            # Adjust duration based on the subject
                            duration = 90 if subject in ['Physics_lab', 'Chemistry_Lab'] else 60
                            num_slots = duration // 30
                            for i in range(num_slots):
                                if (day, slot + i, subject, section, teacher) not in timetable:
                                    timetable[(day, slot + i, subject, section, teacher)] = model.NewBoolVar(
                                        '{}_{}_{}_{}_{}'.format(day, slot + i, subject, section, teacher))

    # Add constraints...

    # Each subject should have the required number of classes per week
    for subject in subjects:
        for section in sections:
            if subject in ['Physics_lab', 'Chemistry_Lab']:
                model.Add(sum(timetable[(day, slot, subject, section, teacher)]
                              for day in days for slot in range(slots_per_day) for teacher in subject_teachers[subject]) == 1)
            else:
                model.Add(sum(timetable[(day, slot, subject, section, teacher)]
                              for day in days for slot in range(slots_per_day) for teacher in subject_teachers[subject]) == 5)

    # No two classes should be scheduled at the same time
    for day in days:
        for slot in range(slots_per_day):
            for section in sections:
                model.Add(sum(timetable[(day, slot, subject, section, teacher)]
                                 for subject in subjects for teacher in subject_teachers[subject]) <= 1)

    # Each subject can be scheduled at most two times per day, with reduced repetition
    for day in days:
        for subject in subjects:
            for section in sections:
                for teacher in subject_teachers[subject]:
                    if subject in ['Physics_lab', 'Chemistry_Lab']:
                        model.Add(sum(timetable[(day, slot, subject, section, teacher)]
                                      for slot in range(slots_per_day)) <= 1)
                    else:
                        model.Add(sum(timetable[(day, slot, subject, section, teacher)]
                                      for slot in range(slots_per_day)) <= 2)

    # Subjects in each section should be different
    for day in days:
        for slot in range(slots_per_day):
            for subject in subjects:
                for section1 in sections:
                    for section2 in sections:
                        if section1 != section2:
                            model.Add(sum(timetable[(day, slot, subject, section1, teacher)]
                                             for teacher in subject_teachers[subject]) +
                                      sum(timetable[(day, slot, subject, section2, teacher)]
                                             for teacher in subject_teachers[subject]) <= 1)

    # Teachers should not be assigned to multiple classes at the same time
    for day in days:
        for slot in range(slots_per_day):
            for teacher in set(sum(subject_teachers.values(), [])):
                for section in sections:
                    model.Add(sum(timetable[(day, slot, subject, section, teacher)]
                                 for subject in subjects if teacher in subject_teachers[subject]) <= 1)

    # Ensure the timetable ends at 4 PM by reducing time at unscheduled classes
    for day in days:
        for slot in range(slots_per_day, slots_per_week):
            for subject in subjects:
                for section in sections:
                    for teacher in subject_teachers[subject]:
                        if (day, slot, subject, section, teacher) not in timetable:
                            timetable[(day, slot, subject, section, teacher)] = model.NewBoolVar(
                                '{}_{}_{}_{}_{}'.format(day, slot, subject, section, teacher))

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
                for slot in range(slots_per_week):
                    if slot < slots_per_day:
                        timetable_slot = {}
                        for subject in subjects:
                            timetable_subject = []
                            for teacher in subject_teachers[subject]:
                                if solver.Value(timetable[(day, slot, subject, section, teacher)]):
                                    timetable_subject.append(teacher)
                            timetable_slot[subject] = timetable_subject
                        timetable_day[slot] = timetable_slot
                    else:
                        # Time slots beyond the regular slots (unscheduled classes)
                        timetable_day[slot] = {}
                timetable_section[day] = timetable_day
            timetables[section] = timetable_section

    return timetables

timetables = create_timetables()

# Print the timetables
for section, timetable_section in timetables.items():
    print(f"Timetable for {section}:")
    for day, timetable_day in timetable_section.items():
        print(f"\n{day}")
        for slot, timetable_slot in timetable_day.items():
            print(f"\nSlot {slot + 1}:")
            if timetable_slot:
                for subject, teachers in timetable_slot.items():
                    for teacher in teachers:
                        print(f"{subject} - {teacher}")
            else:
                print("Unscheduled class")
            print('---')
