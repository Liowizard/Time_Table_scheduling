from flask import Flask , render_template ,request
from Time_table import timetables_data


app = Flask(__name__)

data_storage = []

@app.route('/', methods =[ "POST"])
def POST_timetables():
    data = request.get_json()

    data_storage.append(data)

    return "cool"




@app.route('/TimeTable')
def Display_timetables():
    if len(data_storage)==0:
        return "update a data first"
    data=data_storage[-1]


    days = data.get('days')
    subjects=data.get("subjects")
    sections=data.get("sections")
    num_weeks=data.get("num_weeks")
    timetables = timetables_data(days,subjects,sections,num_weeks)

    return render_template('timetable.html', timetable_data=timetables)


if __name__ == '__main__':
    app.run(debug=True)