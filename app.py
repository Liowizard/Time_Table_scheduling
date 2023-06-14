from flask import Flask , render_template
# from ortools.sat.python import cp_model
from Time_table import create_timetables


app = Flask(__name__)


@app.route('/')
def display_timetables():
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
        # print(timetable_data)

    return render_template('timetable.html', timetables=timetable_data)
    

if __name__ == '__main__':
    app.run(debug=True)