from ortools.sat.python import cp_model

def create_timetables():
    # Create the CP model
    model = cp_model.CpModel()

    # Define the variables
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    subjects = ['Mathematics', 'Physics', 'Chemistry', 'English', 'History', 'Physics_Lab']
    sections = ['sec_A', 'sec_B', 'sec_C']
    teachers = ['Doris Wilson', 'Amy Smith', 'Mrs. A. T. Whitecotton', 'Geraldine Carpenter',
                'Edna Francis', 'Sarah Norris', 'Jennie Crigler', 'Gladys Swon',
                'Ruth Carman', 'Lela Pat Buckman']
    slots_per_day = 8

    # Define the subject-teacher mapping
    subject_teacher_mapping = {
        'Mathematics': ['Doris Wilson', 'Amy Smith'],
        'Physics': ['Mrs. A. T. Whitecotton', 'Geraldine Carpenter'],
        'Chemistry': ['Edna Francis', 'Sarah Norris'],
        'English': ['Jennie Crigler', 'Gladys Swon'],
        'History': ['Ruth Carman', 'Lela Pat Buckman'],
        'Physics_Lab': ['Lab Instructor']
    }

    # Create the variables for each subject in each day, slot, and section
    timetable = {}
    for day in days:
        for slot in range(slots_per_day):
            for subject in subjects:
                for section in sections:
                    for teacher in subject_teacher_mapping[subject]:
                        timetable[(day, slot, subject, section, teacher)] = model.NewBoolVar(f'{day}_{slot}_{subject}_{section}_{teacher}')

    # Add constraints

    # Each subject should have exactly one class per section per day
    for subject in subjects:
        for section in sections:
            for day in days:
                model.Add(sum(timetable[(day, slot, subject, section, teacher)]
                             for slot in range(slots_per_day)
                             for teacher in subject_teacher_mapping[subject]) == 1)

    # No two classes should be scheduled at the same time for each section
    for day in days:
        for slot in range(slots_per_day):
            for section in sections:
                model.Add(sum(timetable[(day, slot, subject, section, teacher)]
                                 for subject in subjects
                                 for teacher in subject_teacher_mapping[subject]) <= 1)

    # Subjects in each section should be different for each slot
    for day in days:
        for slot in range(slots_per_day):
            for subject in subjects:
                for section1 in sections:
                    for section2 in sections:
                        if section1 != section2:
                            model.Add(sum(timetable[(day, slot, subject, section1, teacher)]
                                             for teacher in subject_teacher_mapping[subject]) +
                                      sum(timetable[(day, slot, subject, section2, teacher)]
                                             for teacher in subject_teacher_mapping[subject]) <= 1)

    # Teachers should not be assigned to multiple classes at the same time
    for day in days:
        for slot in range(slots_per_day):
            for teacher in teachers:
                model.Add(sum(timetable[(day, slot, subject, section, teacher)]
                             for subject in subjects for section in sections
                             if teacher in subject_teacher_mapping[subject]) <= 1)

    # Physics Lab should be scheduled once a week
    model.Add(sum(timetable[(day, slot, 'Physics_Lab', section, 'Lab Instructor')]
                 for day in days for slot in range(slots_per_day) for section in sections) == 1)

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
                for slot in range(slots_per_day):
                    timetable_slot = {}
                    for subject in subjects:
                        for teacher in subject_teacher_mapping[subject]:
                            if solver.Value(timetable[(day, slot, subject, section, teacher)]) == 1:
                                if subject == 'Physics_Lab':
                                    timetable_slot[subject] = 'Physics_Lab - Lab Instructor'
                                else:
                                    timetable_slot[subject] = f'{subject} - {teacher}'
                    timetable_day[slot] = timetable_slot
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
            print(f"Slot {slot + 1}:")
            for subject, teacher in timetable_slot.items():
                print(f"{subject} - {teacher}")
            print('---')
