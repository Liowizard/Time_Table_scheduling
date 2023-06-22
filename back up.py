

    # # Teachers should not be assigned to multiple sections at the same time
    # for week in range(num_weeks):
    #     for day in days:
    #         for slot in range(slots_per_day):
    #             for teacher in all_staff:
    #                 for section1 in sections:
    #                     for section2 in sections:
    #                         if section1 != section2:
    #                             model.Add(
    #                                 sum(timetable[(week, day, slot, subject, section1, teacher)]
    #                                     for subject in list(subjects.keys()) if teacher in subjects[subject][3]) +
    #                                 sum(timetable[(week, day, slot, subject, section2, teacher)]
    #                                     for subject in list(subjects.keys()) if teacher in subjects[subject][3]) <= 1)

    # # Add constraint to avoid assigning same subject continually in all sections
    # for subject in list(subjects.keys()):
    #     for week in range(num_weeks):
    #         for day in days:
    #             for slot in range(slots_per_day - 1):
    #                 for section1 in sections:
    #                     for section2 in sections:
    #                         if section1 != section2:
    #                             model.Add(
    #                                 sum(timetable[(week, day, slot, subject, section1, teacher)]
    #                                     for teacher in subjects[subject][3]) +
    #                                 sum(timetable[(week, day, slot + 1, subject, section2, teacher)]
    #                                     for teacher in subjects[subject][3]) <= 1)

    # # Add constraint to limit maximum 2 same subjects in the same day
    # for week in range(num_weeks):
    #     for day in days:
    #         for subject in list(subjects.keys()):
    #             for section in sections:
    #                 # Set the probability for assigning the subject twice in a day
    #                 if random.random() < 0.1:  # Adjust the probability as desired (e.g., 0.1 for 10% chance)
    #                     max_assignments = 2
    #                 else:
    #                     max_assignments = 1

    #                 model.Add(
    #                     sum(timetable[(week, day, slot, subject, section, teacher)]
    #                         for slot in range(slots_per_day) for teacher in subjects[subject][3]) <= max_assignments)

    # # Add constraint to avoid assigning the same subject in consecutive time slots
    # for week in range(num_weeks):
    #     for day in days:
    #         for subject in list(subjects.keys()):
    #             for section in sections:
    #                 for slot in range(slots_per_day - 1):
    #                     model.Add(
    #                         sum(timetable[(week, day, slot, subject, section, teacher)]
    #                             for teacher in subjects[subject][3]) +
    #                         sum(timetable[(week, day, slot + 1, subject, section, teacher)]
    #                             for teacher in subjects[subject][3]) <= 1)

    # # Distribute workload among staffs
    # if DISTRIBUTE_WORK_LOAD_AMONG_STAFFS:
    #     for teacher in all_staff:
    #         for week in range(num_weeks):
    #             for day in days:
    #                 model.Add(
    #                     sum(timetable[(week, day, slot, subject, section, teacher)]
    #                         for slot in range(slots_per_day) for subject in list(subjects.keys())
    #                         for section in sections if teacher in subjects[subject][3]) <= 5)
