import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import timedelta, datetime

from . import dir_path

# Define how each category maps to a broader type
CATEGORY_TYPE_MAP = {
    'Deep Work':       'focus',
    'Creative Session':'focus',     # new focus category
    'Admin':           'other',
    'Collaboration':   'other',
    'Shallow Work':    'other',
    'Break':           'break',
    'Lunch':           'break',     # treat lunch as a break
    'Short Break':     'break'      # etc.
}

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

def read_data_csv():
    df = pd.read_csv('productivity_data.csv')
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Duration (min)'] = (df['End Time'] - df['Start Time']).dt.total_seconds() / 60
    return df

def generate_schedule(tasks, categories, start_times, end_times, energy):
    time_blocks = []
    time_blocks.append({'energy': energy})  
    for i in range(len(tasks)):
        start = datetime.strptime(start_times[i], "%H:%M")
        end = datetime.strptime(end_times[i], "%H:%M")
        task_block = {
            'task': tasks[i],
            'category': categories[i],
            'start': start.strftime("%I:%M %p"),
            'end': end.strftime("%I:%M %p"),
            #'energy': energy  # applied to each task block
        }
        time_blocks.append(task_block)
    return time_blocks


def read_data(time_blocks):
    # Extract energy level (assuming it's the first item and a dict with 'energy' key)
    energy_entry = time_blocks[0]
    energy = energy_entry.get('energy', ['Unknown'])[0]

    # Extract task blocks
    tasks = time_blocks[1:]  # remaining items are tasks

    # Convert to structured list of dicts for DataFrame
    structured_data = []
    for block in tasks:
        start_dt = datetime.strptime(block['start'], "%I:%M %p")
        end_dt = datetime.strptime(block['end'], "%I:%M %p")
        duration_min = (end_dt - start_dt).total_seconds() / 60

        structured_data.append({
            'Task': block['task'],
            'Category': block['category'],
            'Start Time': start_dt,
            'End Time': end_dt,
            'Duration (min)': duration_min,
            'Energy': energy
        })

    df = pd.DataFrame(structured_data)
    return df

def generate_charts(df):
    os.makedirs(f'{dir_path}app/static/charts', exist_ok=True)

    # Pie chart: Category distribution
    pie_data = df.groupby('Category')['Duration (min)'].sum()
    plt.figure(figsize=(6, 6))
    pie_data.plot.pie(autopct='%1.1f%%')
    plt.title('Time Spent by Category')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig(f'{dir_path}app/static/charts/pie_chart.png')
    plt.close()

    # Bar chart: Time spent per task
    bar_data = df.groupby('Task')['Duration (min)'].sum()
    bar_data = bar_data.sort_values()
    plt.figure(figsize=(8, 6))
    bar_data.plot(kind='barh', color='skyblue')
    plt.title('Time Spent per Task')
    plt.xlabel('Minutes')
    plt.tight_layout()
    plt.savefig(f'{dir_path}app/static/charts/bar_chart.png')
    plt.close()





