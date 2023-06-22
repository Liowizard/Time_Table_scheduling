from ortools.sat.python import cp_model
import datetime

start_time = datetime.time(8, 0)  # Start time: 8 AM
end_time = datetime.time(16, 0)  # End time: 4 PM
interval = datetime.timedelta(minutes=5)  # Time interval: 5 minutes

times = []
current_time = start_time

while current_time < end_time:
    times.append(current_time.strftime('%H:%M'))
    current_time = (datetime.datetime.combine(datetime.date.today(), current_time) + interval).time()

# print(times)

DISTRIBUTE_WORK_LOAD_AMONG_STAFFS = True
# days = ["Monday",'tuesday','wednesday','thursday','friday']
days = ["Monday"]
                      
subjects = {
    'Mathematics': [60, "theory", 1, ['Mathematics1', 'Mathematics2', 'Mathematics3']],
    'Physics': [60, "theory", 1, ['Physics1', 'Physics2', 'Physics3']],
    'Chemistry': [60, "theory", 1, ['Chemistry1', 'Chemistry2', 'Chemistry3']],
    'English': [60, "theory", 1, ['English1', 'English2', 'English3']],
    'History': [60, "theory", 1, ['History1', 'History2', 'History3']],
    'Bio': [60, "theory", 1, ['Bio1', 'Bio2', 'Bio3']],
    'Chemistry_lab': [60, "lab", 1, ['Chemistry_lab1', 'Chemistry_lab2', 'Chemistry_lab3']],
    'Physics_lab': [60, "lab", 1, ['Physics_lab1', 'Physics_lab2', 'Physics_lab3']]
}

sections = ['sec_A']

num_weeks = 1

def create_timetables(days, subjects, sections, num_weeks):
    # Create the CP model
    model = cp_model.CpModel()
    lab_subjects = []

    for subject in subjects.keys():
        if subjects[subject][1] == "lab":
            lab_subjects.append(subject)

    # Define the variables

    slots_per_day = len(times)  # Total number of hours
    slots_per_week = slots_per_day * len(days)
    minutes_per_day = 420  # Maximum minutes per day

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
                


    # Create the solver and solve the model
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 60.0
    status = solver.Solve(model)

    # Check if a solution is found
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        # Create a dictionary to store the timetable
        timetable_data = {}

        # Iterate over the assigned variables and extract the information
        for (week, day, slot, subject, section, teacher), assigned in timetable.items():
            if solver.BooleanValue(assigned):
                # Get the start and end time of the class
                start_slot = slot
                end_slot = slot + int(subjects[subject][0] / 5)  # Divide duration by interval (5 minutes)

                # Get the time range of the class
                start_time = times[start_slot]
                end_time = times[end_slot]

                # Create a unique identifier for the class
                class_id = '{}_{}_{}_{}_{}'.format(week, day, start_time, subject, section)

                # Store the class information in the timetable dictionary
                timetable_data[class_id] = {
                    'Week': week,
                    'Day': day,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Subject': subject,
                    'Section': section,
                    'Teacher': teacher
                }

        # Return the timetable data
        return timetable_data

    else:
        print("No feasible solution found.")

# Generate the timetable
timetable_data = create_timetables(days, subjects, sections, num_weeks)

# Print the timetable data
for class_id, class_info in timetable_data.items():
    print(class_id, ":", class_info)














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