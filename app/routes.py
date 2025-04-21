from flask import redirect,url_for,render_template,request

from app.logic import CATEGORY_TYPE_MAP, compute_productivity_stats, generate_charts, generate_schedule, read_data, read_data_csv
from . import app, dir_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks')
def tasks():
    return render_template('tasks.html')

@app.route('/dashboard', methods=['POST'])
def dashboard():
    tasks       = request.form.getlist('task')
    categories  = request.form.getlist('category')
    start_times = request.form.getlist('start_time')
    end_times   = request.form.getlist('end_time')
    #energy      = request.form.getlist('energy')
    energy      = request.form['energy'] 

    schedule = generate_schedule(tasks, categories, start_times, end_times, energy)

    #print("schedule: ", schedule)
    
    df = read_data(schedule)
    generate_charts(df)

    
    stats = compute_productivity_stats(df)
    return render_template('dashboard.html', stats=stats)


