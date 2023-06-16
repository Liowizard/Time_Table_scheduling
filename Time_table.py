from ortools.sat.python import cp_model
from collections import Counter
import json

def create_timetables():
    # Create the CP model
    model = cp_model.CpModel()

    # Define the variables
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    subjects = {
        'Mathematics': [60, "theory", 15],
        'Physics': [60, "theory", 15],
        'Chemistry': [60, "theory", 15],
        'English': [60, "theory", 15],
        'History': [60, "theory", 15],
        'Bio': [60, "theory", 15],
        'Tamil': [60, "theory", 15],
        'French': [60, "theory", 15]
    }

    sections = ['sec_A', 'sec_B', 'sec_C']

    subject_teachers = {
        'Mathematics': ['Doris Wilson', 'Amy Smith'],
        'Physics': ['Mrs. A. T. Whitecotton', 'Geraldine Carpenter'],
        'Chemistry': ['Edna Francis', 'Sarah Norris'],
        'English': ['Jennie Crigler', 'Gladys Swon'],
        'History': ['Ruth Carman', 'Lela Pat Buckman'],
        'Bio': ['Lio', 'Fin'],
        'Tamil': ['Mrs. A. T. Whitecotton', 'Geraldine Carpenter'],
        'French': ['John Doe', 'Jane Smith']
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
                                if (day, i, subject, section, teacher) not in timetable:
                                    timetable[(day, i, subject, section, teacher)] = model.NewBoolVar(
                                        '{}_{}_{}_{}_{}'.format(day, i, subject, section, teacher))

    # Lab subjects should be scheduled once in 5 days for each section
    for subject in list(subjects.keys()):
        for section in sections:
            model.Add(
                sum(timetable[(day, slot, subject, section, teacher)]
                    for day in days for slot in range(slots_per_day) for teacher in subject_teachers[subject]) ==
                int(subjects[subject][2] / 3))

    # No two classes should be scheduled at the same time
    for day in days:
        for slot in range(slots_per_day):
            for section in sections:
                model.Add(sum(timetable[(day, slot, subject, section, teacher)]
                              for subject in list(subjects.keys()) for teacher in subject_teachers[subject]) <= 1)

    # Teachers should not be assigned to multiple sections at the same time
    for day in days:
        for slot in range(slots_per_day):
            for teacher in set(sum(subject_teachers.values(), [])):
                for section1 in sections:
                    for section2 in sections:
                        if section1 != section2:
                            model.Add(sum(timetable[(day, slot, subject, section1, teacher)]
                                          for subject in list(subjects.keys()) if teacher in subject_teachers[subject]) +
                                      sum(timetable[(day, slot, subject, section2, teacher)]
                                          for subject in list(subjects.keys()) if teacher in subject_teachers[subject]) <= 1)

    # Subjects should not be scheduled continuously
    for day in days:
        for section in sections:
            for subject in list(subjects.keys()):
                for teacher in subject_teachers[subject]:
                    for slot in range(slots_per_day - 1):
                        model.Add(
                            timetable[(day, slot, subject, section, teacher)] +
                            timetable[(day, slot + 1, subject, section, teacher)] <= 1
                        )

    # Schedule English subject at Monday 1st slot in sec_A
    subject = 'English'
    section = 'sec_A'
    teacher = subject_teachers[subject][0]  # Assuming the first teacher in the list
    model.Add(timetable[('Monday', 0, subject, section, teacher)] == 1)

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
                                    total_minutes -= duration  # Subtract the duration if total minutes exceed the limit
                        if timetable_subject:
                            timetable_slot[subject] = timetable_subject
                    if timetable_slot:
                        timetable_day[slot] = timetable_slot
                if timetable_day:
                    timetable_section[day] = timetable_day
            if timetable_section:
                timetables[section] = timetable_section

    return timetables





data=create_timetables()
# print(data)

def timetables_data():
    timetables = create_timetables()

    # Convert the timetables to a format suitable for rendering in HTML
    timetable_data = []
    for section, timetable_section in timetables.items():
        section_data = {'section': section, 'days': []}
        for day, timetable_day in timetable_section.items():
            day_data = {'day': day, 'slots': []}
            for slot, timetable_slot in timetable_day.items():
                slot_data = {'slot': slot + 1, 'subjects': []}
                for subject, teachers in timetable_slot.items():
                    for teacher in teachers:
                        slot_data['subjects'].append({'subject': subject, 'teacher': teacher})
                day_data['slots'].append(slot_data)
            section_data['days'].append(day_data)
        timetable_data.append(section_data)

    return timetable_data


# data=timetables_data()

# print(data)

# with open("output.json", "w") as outfile:
#     json.dump(data, outfile)

# if timetables is not None:
#     for section, timetable_section in timetables.items():
#         print(f"Timetable for section {section}:")
#         for day, timetable_day in timetable_section.items():
#             print(f"Day: {day}")
#             for slot, timetable_slot in timetable_day.items():
#                 print(f"Slot: {slot}")
#                 for subject, classes in timetable_slot.items():
#                     for cls in classes:
#                         if cls['teacher']:
#                             print(f"Subject: {subject}")
#                             print(f"  Teacher: {cls['teacher']}, Duration: {cls['duration']}, Type: {cls['type']}")
#                 print()
#             print()
# else:
#     print("No feasible solution found.")

