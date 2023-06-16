from flask import Flask , render_template
# from ortools.sat.python import cp_model
from Time_table import timetables_data


app = Flask(__name__)


@app.route('/')
def display_timetables():
    timetables = timetables_data()

    return render_template('timetable.html', timetables=timetables)
    

if __name__ == '__main__':
    app.run(debug=True)