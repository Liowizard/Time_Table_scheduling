from flask import Flask , render_template
from ortools.sat.python import cp_model
from Time_table import create_timetables

app = Flask(__name__)


@app.route('/')
def helloworld():
        timetables = create_timetables()
        sections = list(timetables.keys())
        return render_template('timetable.html', timetables=timetables)
    

if __name__ == '__main__':
    app.run(debug=True)