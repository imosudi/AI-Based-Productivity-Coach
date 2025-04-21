from datetime import datetime
from flask import redirect,url_for,render_template,request

#from app.logic import CATEGORY_TYPE_MAP, compute_productivity_stats, generate_charts, generate_schedule, optimise_task_schedule, read_data, read_data_csv
from app.logic import (
    CATEGORY_TYPE_MAP, 
    compute_productivity_stats, 
    generate_charts, 
    generate_schedule,
    generate_time_blocked_schedule,
    optimise_task_schedule,
    read_data, 
    read_data_csv
)

from . import app, dir_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks')
def tasks():
    return render_template('tasks.html')


@app.route('/dashboard', methods=['POST'])
def dashboard():
    tasks = request.form.getlist('task')
    categories = request.form.getlist('category')
    start_times = request.form.getlist('start_time')
    end_times = request.form.getlist('end_time')
    energy = request.form['energy']
    
    # Check if user wants automatic time blocking
    use_time_blocking = request.form.get('use_time_blocking', 'off') == 'on'
    
    if use_time_blocking:
        # Generate optimized schedule
        schedule = generate_time_blocked_schedule(tasks, categories, start_times, end_times, energy)
    else:
        # Use the original schedule as provided by user
        schedule = generate_schedule(tasks, categories, start_times, end_times, energy)
    
    df = read_data(schedule)
    generate_charts(df)
    
    stats = compute_productivity_stats(df)
    return render_template('dashboard.html', stats=stats)

@app.route('/optimise', methods=['POST'])
def optimise():
    """Route for optimizing an existing schedule"""
    tasks = request.form.getlist('task')
    categories = request.form.getlist('category')
    start_times = request.form.getlist('start_time')
    end_times = request.form.getlist('end_time')
    energy = request.form['energy']
    
    # Parse times to calculate durations
    parsed_start_times = [datetime.strptime(t, "%H:%M") for t in start_times]
    parsed_end_times = [datetime.strptime(t, "%H:%M") for t in end_times]
    durations = [(parsed_end_times[i] - parsed_start_times[i]).total_seconds() / 60 for i in range(len(tasks))]
    
    # Get overall schedule start and end
    overall_start = min(parsed_start_times)
    overall_end = max(parsed_end_times)
    
    # optimise the schedule
    optimised_blocks = optimise_task_schedule(tasks, categories, durations, overall_start, overall_end, energy)
    
    # Prepend energy information
    schedule = [{'energy': energy}]
    schedule.extend(optimised_blocks)
    
    df = read_data(schedule)
    generate_charts(df)
    
    stats = compute_productivity_stats(df)
    return render_template('dashboard.html', stats=stats, is_optimised=True)

