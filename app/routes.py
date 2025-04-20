from flask import redirect,url_for,render_template,request

from app.logic import CATEGORY_TYPE_MAP, generate_charts, generate_schedule, read_data, read_data_csv
from . import app, dir_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    df = read_data_csv()
    generate_charts(df)

    total_focus = df[df['Category'] == 'Deep Work']['Duration (min)'].sum()
    total_break = df[df['Category'] == 'Break']['Duration (min)'].sum()
    total_minutes = df['Duration (min)'].sum()

    stats = {
        'focus': round(total_focus, 1),
        'break': round(total_break, 1),
        'productivity_ratio': round((total_focus / total_minutes) * 100, 1)
    }

    return render_template('dashboard.html', stats=stats)

@app.route('/schedule', methods=['POST'])
def schedule():
    tasks       = request.form.getlist('task')
    categories  = request.form.getlist('category')
    start_times = request.form.getlist('start_time')
    end_times   = request.form.getlist('end_time')
    #energy      = request.form.getlist('energy')
    energy      = request.form['energy'] 

    schedule = generate_schedule(tasks, categories, start_times, end_times, energy)

    print("schedule: ", schedule)
    
    df = read_data(schedule)
    generate_charts(df)

    """total_focus = df[df['Category'] == 'Deep Work']['Duration (min)'].sum()
    total_break = df[df['Category'] == 'Break']['Duration (min)'].sum()
    total_minutes = df['Duration (min)'].sum()

    stats = {
        'focus': round(total_focus, 1),
        'break': round(total_break, 1),
        'productivity_ratio': round((total_focus / total_minutes) * 100, 1)
    }"""

    def compute_productivity_stats(df):
        # Map each row to its type
        df['Type'] = df['Category'].map(CATEGORY_TYPE_MAP).fillna('other')
        
        # Sum durations by type
        sums = df.groupby('Type')['Duration (min)'].sum().to_dict()
        
        total_focus   = sums.get('focus', 0.0)
        total_break   = sums.get('break', 0.0)
        total_minutes = df['Duration (min)'].sum()
        
        # Avoid division by zero
        productivity_ratio = (total_focus / total_minutes * 100) if total_minutes else 0.0
        
        stats = {
            'focus':               round(total_focus, 1),
            'break':               round(total_break, 1),
            'other':               round(sums.get('other', 0.0), 1),
            'productivity_ratio':  round(productivity_ratio, 1)
        }
        return stats
    stats = compute_productivity_stats(df)
    return render_template('dashboard.html', stats=stats)

    return render_template('schedule.html', schedule=schedule)


