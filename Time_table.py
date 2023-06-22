from ortools.sat.python import cp_model
from collections import Counter
import random


DISTRIBUTE_WORK_LOAD_AMONG_STAFFS = True
# days = ["Monday",'tuesday','wednesday','thursday','friday']
days = ["Monday"]
                      
subjects = {
        'Mathematics': [60, "theory", 1, ['Mathematics1', 'Mathematics2', 'Mathematics3'], 1],
        'Physics': [60, "theory", 1, ['Physics1', 'Physics2', 'Physics3'], 1],
        'Chemistry': [60, "theory", 1, ['Chemistry1', 'Chemistry2', 'Chemistry3'], 1],
        'English': [60, "theory", 1, ['English1', 'English2', 'English3'], 1],
        'History': [60, "theory", 1, ['History1', 'History2', 'History3'], 1],
        'Bio': [60, "theory", 1, ['Bio1', 'Bio2', 'Bio3'], 1],
        'Chemistry_lab': [60, "lab", 1, ['Chemistry_lab1', 'Chemistry_lab2', 'Chemistry_lab3'], 2],
        'Physics_lab': [60, "lab", 1, ['Physics_lab1', 'Physics_lab2', 'Physics_lab3'], 2]
        }

sections = ['sec_A', 'sec_B', 'sec_C']

num_weeks = 1

def create_timetables( days,subjects,sections,num_weeks):
    # Create the CP model
    model = cp_model.CpModel()
    lab_subjects=[]

    for subject in subjects.keys():
        if subjects[subject][1] == "lab":
            lab_subjects.append(subject)

        

    # Define the variables

    slots_per_day = 8  # Total number of hours
    slots_per_week = slots_per_day * len(days)
    minutes_per_day = 420 # Maximum minutes per day

    all_staff = set()
    for subject_info in subjects.values():
        names = subject_info[3]
        all_staff.update(names)

    # Create the variables for each subject in each time slot, section, teacher, and week
    timetable = {}
    for week in range(num_weeks):
        for day in days:
            for slot in range(slots_per_day):
                for subject in list(subjects.keys()):
                    for section in sections:
                        for teacher in subjects[subject][3]:
                            if (week, day, slot, subject, section, teacher) not in timetable:
                                for i in range(slots_per_day):
                                    if (week, day, i, subject, section, teacher) not in timetable:
                                        timetable[(week, day, i, subject, section, teacher)] = model.NewBoolVar(
                                            '{}_{}_{}_{}_{}_{}'.format(week, day, i, subject, section, teacher))

    # Subjects should be scheduled as per they mentioned
    for subject in list(subjects.keys()):
        for section in sections:
            for week in range(num_weeks):
                model.Add(
                    sum(timetable[(week, day, slot, subject, section, teacher)]
                        for day in days for slot in range(slots_per_day) for teacher in subjects[subject][3]) ==
                    int(subjects[subject][2]))


    # No two classes should be scheduled at the same time
    for week in range(num_weeks):
        for day in days:
            for slot in range(slots_per_day):
                for section in sections:
                    model.Add(sum(timetable[(week, day, slot, subject, section, teacher)]
                                  for subject in list(subjects.keys()) for teacher in subjects[subject][3]) <= 1)


    # Teachers should not be assigned to multiple sections at the same time
    for week in range(num_weeks):
        for day in days:
            for slot in range(slots_per_day):
                for teacher in all_staff:
                    for section1 in sections:
                        for section2 in sections:
                            if section1 != section2:
                                model.Add(sum(timetable[(week, day, slot, subject, section1, teacher)]
                                              for subject in list(subjects.keys()) if teacher in subjects[subject][3]) +
                                          sum(timetable[(week, day, slot, subject, section2, teacher)]
                                              for subject in list(subjects.keys()) if teacher in subjects[subject][3]) <= 1)


    # # Schedule English subject at Monday 1st slot in sec_A for the first week
    # subject = 'English'
    # section = 'sec_A'
    # teacher = subjects[subject][3][0]  # Assuming the first teacher in the list
    # model.Add(timetable[(0, 'Monday', 0, subject, section, teacher)] == 1)


    # Add constraint to avoid assigning same subject continually in all sections
    for subject in list(subjects.keys()):
        for week in range(num_weeks):
            for day in days:
                for slot in range(slots_per_day - 1):
                    for section1 in sections:
                        for section2 in sections:
                            if section1 != section2:
                                model.Add(sum(timetable[(week, day, slot, subject, section1, teacher)]
                                              for teacher in subjects[subject][3]) +
                                          sum(timetable[(week, day, slot + 1, subject, section2, teacher)]
                                              for teacher in subjects[subject][3]) <= 1)


    # Add constraint to limit maximum 2 same subjects in the same day
    for week in range(num_weeks):
        for day in days:
            for subject in list(subjects.keys()):
                for section in sections:
                    # Set the probability for assigning the subject twice in a day
                    if random.random() < 0.1:  # Adjust the probability as desired (e.g., 0.1 for 10% chance)
                        max_assignments = 2
                    else:
                        max_assignments = 1

                    model.Add(sum(timetable[(week, day, slot, subject, section, teacher)]
                                  for slot in range(slots_per_day) for teacher in subjects[subject][3]) <= max_assignments)


    # Add constraint to avoid assigning the same subject in consecutive time slots
    for week in range(num_weeks):
        for day in days:
            for subject in list(subjects.keys()):
                for section in sections:
                    for slot in range(slots_per_day - 1):
                        model.Add(sum(timetable[(week, day, slot, subject, section, teacher)]
                                      for teacher in subjects[subject][3]) +
                                  sum(timetable[(week, day, slot + 1, subject, section, teacher)]
                                      for teacher in subjects[subject][3]) <= 1)


    # Distribute workload among staffs
    if DISTRIBUTE_WORK_LOAD_AMONG_STAFFS:
        for teacher in all_staff:
            total_assigned_slots = sum(timetable[key] for key in timetable if key[5] == teacher)
            model.Add(total_assigned_slots >= 1)


    # lab_subjects = ['Physics_lab', 'Chemistry_lab']  # Add other lab subjects if needed

    for lab_subject in lab_subjects:
        for week in range(num_weeks):
            for day in days:
                for slot in range(slots_per_day - 1):
                    # Check if the current slot and the next slot both have the lab subject
                    model.Add(sum(timetable[(week, day, slot, lab_subject, section, teacher)]
                                for section in sections for teacher in subjects[lab_subject][3]) +
                            sum(timetable[(week, day, slot + 1, lab_subject, section, teacher)]
                                for section in sections for teacher in subjects[lab_subject][3]) <= 1)


    # Create the solver and solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    timetables = {}
    subject_counter = Counter()
    if status == cp_model.OPTIMAL:
        for week in range(num_weeks):
            for section in sections:
                timetable_section = {}
                for day in days:
                    timetable_day = {}
                    total_minutes = 0  # Track the total minutes scheduled in a day
                    for slot in range(slots_per_day):
                        timetable_slot = {}
                        for subject in list(subjects.keys()):
                            timetable_subject = []
                            for teacher in subjects[subject][3]:
                                if solver.Value(timetable[(week, day, slot, subject, section, teacher)]) == 1:
                                    subject_duration = subjects[subject][0]
                                    timetable_subject.append((teacher, subject_duration))
                                    subject_counter[subject] += 1
                            if timetable_subject:
                                timetable_slot[subject] = timetable_subject
                        if timetable_slot:
                            total_minutes += subjects[list(timetable_slot.keys())[0]][0]
                            timetable_day[slot] = timetable_slot
                        # If the total minutes for the day is reached, stop adding more slots
                        # print(total_minutes)
                        if total_minutes > minutes_per_day:
                            break
                        else:
                            # print(total_minutes)
                            pass
                    timetable_section[day] = timetable_day
                timetables[(week, section)] = timetable_section
    class_check=[]
    for subject in list(subjects.keys()):
        if subjects[subject][2]*len(sections) != subject_counter[subject]:
            class_check.append("bad")

    # print(len(class_check))
    return timetables













# data=create_timetables()
# print(data)



def timetables_data(days,subjects,sections,num_weeks):

    timetables = create_timetables(days,subjects,sections,num_weeks)

    output = []
    for (week, section), timetable_section in timetables.items():
        section_data = {
            'section': (week, section),
            'days': []
        }
        for day, timetable_day in timetable_section.items():
            day_data = {
                'day': day,
                'slots': []
            }
            for slot, timetable_slot in timetable_day.items():
                slot_data = {
                    'slot': slot + 1,
                    'subjects': []
                }
                for subject, teachers in timetable_slot.items():
                    for teacher, duration in teachers:
                        subject_data = {
                            'subject': subject,
                            'teacher': (teacher, duration)
                        }
                        slot_data['subjects'].append(subject_data)
                day_data['slots'].append(slot_data)
            section_data['days'].append(day_data)
        output.append(section_data)

    return output


# data = timetables_data(days,subjects,sections,num_weeks)
# print(data)









# def timetables_data():
#     timetables = create_timetables()

#     # Convert the timetables to a format suitable for rendering in HTML
#     timetable_data = []
#     for section, timetable_section in timetables.items():
#         section_data = {'section': section, 'days': []}
#         for day, timetable_day in timetable_section.items():
#             day_data = {'day': day, 'slots': []}
#             for slot, timetable_slot in timetable_day.items():
#                 slot_data = {'slot': slot + 1, 'subjects': []}
#                 for subject, teachers in timetable_slot.items():
#                     for teacher in teachers:
#                         slot_data['subjects'].append({'subject': subject, 'teacher': teacher})
#                 day_data['slots'].append(slot_data)
#             section_data['days'].append(day_data)
#         timetable_data.append(section_data)

#     return timetable_data

# data= timetables_data()
# print(data)