# from ortools.sat.python import cp_model

# def create_timetables():
#     # Create the CP model
#     model = cp_model.CpModel()

#     # Define the variables
#     days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
#     subjects = {
#         'Mathematics': [60,"theory "],
#         'Physics': [90,"Lab "],
#         'Chemistry': [60,"theory "],
#         'English': [60,"theory "],
#         'History': [60,"theory "],
#         'Bio': [60,"theory "],
#         'Chemistry_Lab': [90,"Lab "]
#     }
#     sections = ['sec_A', 'sec_B', 'sec_C']
#     subject_teachers = {
#         'Mathematics': ['Doris Wilson', 'Amy Smith'],
#         'Physics': ['Mrs. A. T. Whitecotton', 'Geraldine Carpenter'],
#         'Chemistry': ['Edna Francis', 'Sarah Norris'],
#         'English': ['Jennie Crigler', 'Gladys Swon'],
#         'History': ['Ruth Carman', 'Lela Pat Buckman'],
#         'Bio': ['Lio', 'Fin'],
#         'Chemistry_Lab': ['John Doe', 'Jane Smith']
#     }
#     slots_per_day = 8  # Total number of hours
#     slots_per_week = slots_per_day * len(days)
#     minutes_per_day = 480  # Maximum minutes per day

#     # Create the variables for each subject in each time slot, section, and teacher
#     timetable = {}
#     for day in days:
#         for slot in range(slots_per_day):
#             for subject, duration in subjects.items():
#                 for section in sections:
#                     for teacher in subject_teachers[subject]:
#                         if (day, slot, subject, section, teacher) not in timetable:
#                             num_slots = duration // 30
#                             for i in range(num_slots):
#                                 if (day, slot + i, subject, section, teacher) not in timetable:
#                                     timetable[(day, slot + i, subject, section, teacher)] = model.NewBoolVar(
#                                         '{}_{}_{}_{}_{}'.format(day, slot + i, subject, section, teacher))

#     # Add constraints...

#     # Each subject should have the required number of classes per week
#     for subject, duration in subjects.items():
#         for section in sections:
#             required_slots = duration // 30
#             model.Add(sum(timetable[(day, slot, subject, section, teacher)]
#                           for day in days for slot in range(slots_per_day) for teacher in subject_teachers[subject]) == required_slots)

#     # No two classes should be scheduled at the same time
#     for day in days:
#         for slot in range(slots_per_day):
#             for section in sections:
#                 model.Add(sum(timetable[(day, slot, subject, section, teacher)]
#                                  for subject in subjects for teacher in subject_teachers[subject]) <= 1)

#     # Each subject can be scheduled at most two times per day, with reduced repetition
#     for day in days:
#         for subject, duration in subjects.items():
#             for section in sections:
#                 for teacher in subject_teachers[subject]:
#                     num_slots = duration // 30
#                     model.Add(sum(timetable[(day, slot, subject, section, teacher)]
#                                   for slot in range(slots_per_day)) <= num_slots)

#     # Subjects in each section should be different
#     for day in days:
#         for slot in range(slots_per_day):
#             for subject in subjects:
#                 for section1 in sections:
#                     for section2 in sections:
#                         if section1 != section2:
#                             model.Add(sum(timetable[(day, slot, subject, section1, teacher)]
#                                              for teacher in subject_teachers[subject]) +
#                                       sum(timetable[(day, slot, subject, section2, teacher)]
#                                              for teacher in subject_teachers[subject]) <= 1)

#     # Teachers should not be assigned to multiple classes at the same time
#     for day in days:
#         for slot in range(slots_per_day):
#             for teacher in set(sum(subject_teachers.values(), [])):
#                 for section in sections:
#                     model.Add(sum(timetable[(day, slot, subject, section, teacher)]
#                                  for subject in subjects if teacher in subject_teachers[subject]) <= 1)

#     # Add a constraint to avoid consecutive slots with the same subject
#     for day in days:
#         for slot in range(slots_per_day - 1):
#             for section in sections:
#                 for subject in subjects:
#                     for teacher in subject_teachers[subject]:
#                         next_slot = slot + 1
#                         current_subject_var = timetable[(day, slot, subject, section, teacher)]
#                         next_subject_var = timetable[(day, next_slot, subject, section, teacher)]
#                         model.AddImplication(current_subject_var, next_subject_var.Not())
#                         model.AddImplication(next_subject_var, current_subject_var.Not())

#     # Create the solver and solve the model
#     solver = cp_model.CpSolver()
#     status = solver.Solve(model)

#     # Generate the timetables as dictionaries
#     timetables = {}
#     if status == cp_model.OPTIMAL:
#         for section in sections:
#             timetable_section = {}
#             for day in days:
#                 timetable_day = {}
#                 for slot in range(slots_per_day):
#                     timetable_slot = {}
#                     for subject, duration in subjects.items():
#                         timetable_subject = []
#                         for teacher in subject_teachers[subject]:
#                             if solver.Value(timetable[(day, slot, subject, section, teacher)]):
#                                 timetable_subject.append(teacher)
#                         timetable_slot[subject] = {'teachers': timetable_subject, 'duration': duration}
#                     timetable_day[slot] = timetable_slot
#                 timetable_section[day] = timetable_day
#             timetables[section] = timetable_section

#     return timetables

# timetables = create_timetables()

# print(timetables)

# # # Print the timetables
# # for section, timetable_section in timetables.items():
# #     print(f"Timetable for {section}:")
# #     for day, timetable_day in timetable_section.items():
# #         print(f"\n{day}")
# #         for slot, timetable_slot in timetable_day.items():
# #             print(f"\nSlot {slot + 1}:")
# #             for subject, data in timetable_slot.items():
# #                 teachers = ', '.join(data['teachers'])
# #                 duration = data['duration']
# #                 print(f"{subject} ({duration} min) - {teachers}")
# #             print('---')
