

import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend
import matplotlib.pyplot as plt

import os
from datetime import timedelta, datetime
from . import dir_path

# Define how each category maps to a broader type
CATEGORY_TYPE_MAP = {
    'Deep Work':                   'focus', 'Creative Session':           'focus', 'Learning & Development':     'focus',

    'Break':                      'break',  'Lunch':                      'break', 'Short Break':                'break',

    'Admin':                      'other',  'Shallow Work':               'other',  'Collaboration':              'other',
    'Planning & Strategy':        'other',  'Meetings (1-on-1)':          'other',  'Documentation':              'other',
    'Support & Maintenance':      'other',  'Client Engagement':          'other',  'Team Management':            'other',
    'Errands & Admin (Personal)': 'other',  'Reflection & Review':        'other'
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




def calculate_task_priority(task_name, category, duration, energy_level):
    """
    Calculate priority score for a task based on its attributes.
    
    Parameters:
    - task_name: Name of the task
    - category: Category of the task
    - duration: Duration in minutes
    - energy_level: User's reported energy level (Low/Medium/High)
    
    Returns:
    - priority_score: Numerical score for task priority
    """
    # Base priority score
    priority_score = 0
    
    # Priority based on category type
    category_priority = {
        'Deep Work': 10,
        'Creative Session': 9,
        'Learning & Development': 8,
        'Planning & Strategy': 7,
        'Collaboration': 6,
        'Client Engagement': 6,
        'Team Management': 5,
        'Documentation': 4,
        'Admin': 3,
        'Shallow Work': 2,
        'Support & Maintenance': 2,
        'Errands & Admin (Personal)': 1,
        'Reflection & Review': 4
    }
    
    priority_score += category_priority.get(category, 0)
    
    # Adjust priority based on energy level and task category type
    task_type = CATEGORY_TYPE_MAP.get(category, 'other')
    
    if energy_level == 'High':
        # When energy is high, prioritize focus tasks
        if task_type == 'focus':
            priority_score += 5
    elif energy_level == 'Low':
        # When energy is low, focus tasks are harder to do
        if task_type == 'focus':
            priority_score -= 3
        # Low energy tasks get priority when tired
        if task_type == 'other' and duration <= 30:  # Short administrative tasks
            priority_score += 2
    
    # Urgent/important keywords in task name
    urgent_keywords = ['urgent', 'deadline', 'today', 'important', 'critical', 'due']
    if any(keyword in task_name.lower() for keyword in urgent_keywords):
        priority_score += 5
    
    # Consider duration - shorter tasks may be easier to complete
    if duration <= 15:
        priority_score += 1
    
    return priority_score

def optimise_task_schedule(tasks, categories, durations, start_time, end_time, energy_level):
    """
    optimise task ordering based on priority scores and time constraints.
    
    Parameters:
    - tasks: List of task names
    - categories: List of task categories
    - durations: List of task durations (minutes)
    - start_time: Schedule start time
    - end_time: Schedule end time
    - energy_level: User's reported energy level
    
    Returns:
    - optimised_schedule: List of task blocks with optimised timing
    """
    # Calculate priority for each task
    task_priorities = []
    total_duration = sum(durations)
    
    for i in range(len(tasks)):
        priority = calculate_task_priority(tasks[i], categories[i], durations[i], energy_level)
        task_priorities.append({
            'index': i,
            'task': tasks[i],
            'category': categories[i],
            'duration': durations[i],
            'priority': priority
        })
    
    # Sort tasks by priority (highest first)
    sorted_tasks = sorted(task_priorities, key=lambda x: x['priority'], reverse=True)
    
    # Time blocking - allocate specific time blocks
    current_time = start_time
    optimised_schedule = []
    
    # First pass: Schedule high-priority focus work during peak energy hours
    peak_hours_start = start_time + timedelta(hours=1)  # Assuming peak is 1 hour after start
    peak_hours_end = peak_hours_start + timedelta(hours=3)  # 3-hour peak window
    
    # Schedule focus tasks during peak hours
    focus_tasks = [t for t in sorted_tasks if CATEGORY_TYPE_MAP.get(t['category'], 'other') == 'focus']
    
    remaining_tasks = []
    current_time = start_time
    
    if energy_level == 'High' or energy_level == 'Medium':
        # Process focus tasks first during high/medium energy
        for task in focus_tasks:
            task_duration = timedelta(minutes=task['duration'])
            task_end_time = current_time + task_duration
            
            if task_end_time <= end_time:
                optimised_schedule.append({
                    'task': task['task'],
                    'category': task['category'],
                    'start': current_time.strftime("%I:%M %p"),
                    'end': task_end_time.strftime("%I:%M %p")
                })
                current_time = task_end_time
                
                # Add break after focus tasks if it's a long task
                if task['duration'] > 45:
                    break_end = current_time + timedelta(minutes=10)
                    if break_end <= end_time:
                        optimised_schedule.append({
                            'task': 'Quick Break',
                            'category': 'Break',
                            'start': current_time.strftime("%I:%M %p"),
                            'end': break_end.strftime("%I:%M %p")
                        })
                        current_time = break_end
            else:
                remaining_tasks.append(task)
    else:
        # For low energy, start with easier tasks
        remaining_tasks = focus_tasks
    
    # Add non-focus tasks to remaining
    remaining_tasks.extend([t for t in sorted_tasks if CATEGORY_TYPE_MAP.get(t['category'], 'other') != 'focus' and t not in remaining_tasks])
    
    # Process remaining tasks
    for task in remaining_tasks:
        task_duration = timedelta(minutes=task['duration'])
        task_end_time = current_time + task_duration
        
        if task_end_time <= end_time:
            optimised_schedule.append({
                'task': task['task'],
                'category': task['category'],
                'start': current_time.strftime("%I:%M %p"),
                'end': task_end_time.strftime("%I:%M %p")
            })
            current_time = task_end_time
    
    return optimised_schedule

def generate_time_blocked_schedule(tasks, categories, start_times, end_times, energy):
    """
    Generate an optimised time-blocked schedule based on tasks and energy level.
    """
    # Parse user-provided start and end times
    parsed_start_times = [datetime.strptime(t, "%H:%M") for t in start_times]
    parsed_end_times = [datetime.strptime(t, "%H:%M") for t in end_times]
    
    # Calculate durations for each task
    durations = []
    for i in range(len(parsed_start_times)):
        duration_delta = parsed_end_times[i] - parsed_start_times[i]
        duration_minutes = duration_delta.total_seconds() / 60
        durations.append(duration_minutes)
    
    # Find overall schedule start and end times
    schedule_start = min(parsed_start_times)
    schedule_end = max(parsed_end_times)
    
    # Build time-blocked schedule
    time_blocks = []
    
    # Add energy level information
    time_blocks.append({'energy': energy})
    
    # Generate optimised schedule if user wants automatic time blocking
    user_schedule = []
    for i in range(len(tasks)):
        task_block = {
            'task': tasks[i],
            'category': categories[i],
            'start': parsed_start_times[i].strftime("%I:%M %p"),
            'end': parsed_end_times[i].strftime("%I:%M %p")
        }
        user_schedule.append(task_block)
    
    # Add user's schedule to time blocks
    time_blocks.extend(user_schedule)
    
    return time_blocks


def apply_pomodoro_technique(tasks, categories, durations, start_time, end_time, pomodoro_settings):
    """
    Apply Pomodoro technique to a task schedule.
    
    Parameters:
    - tasks: List of task names
    - categories: List of task categories
    - durations: List of task durations (minutes)
    - start_time: Schedule start time
    - end_time: Schedule end time
    - pomodoro_settings: Dictionary with Pomodoro settings
        - focus_duration: Duration of focus periods (default: 25 minutes)
        - short_break: Duration of short breaks (default: 5 minutes)
        - long_break: Duration of long breaks (default: 15 minutes)
        - sessions_before_long_break: Number of focus sessions before a long break (default: 4)
    
    Returns:
    - pomodoro_schedule: List of task blocks with Pomodoro intervals
    """
    # Get Pomodoro settings or use defaults
    focus_duration = pomodoro_settings.get('focus_duration', 25)
    short_break = pomodoro_settings.get('short_break', 5) 
    long_break = pomodoro_settings.get('long_break', 15)
    sessions_before_long_break = pomodoro_settings.get('sessions_before_long_break', 4)
    
    pomodoro_schedule = []
    current_time = start_time
    pomodoro_count = 0
    
    # Group tasks by category type
    task_data = []
    for i in range(len(tasks)):
        task_type = CATEGORY_TYPE_MAP.get(categories[i], 'other')
        if task_type == 'break':  # Skip break tasks as we'll be adding breaks automatically
            continue
        
        task_data.append({
            'task': tasks[i],
            'category': categories[i],
            'duration': durations[i],
            'remaining_duration': durations[i],
            'type': task_type
        })
    
    # First, handle focus tasks with Pomodoro technique
    focus_tasks = [t for t in task_data if t['type'] == 'focus']
    other_tasks = [t for t in task_data if t['type'] != 'focus']
    
    # Process focus tasks using Pomodoro
    for task in focus_tasks:
        # Work on task until it's completed
        while task['remaining_duration'] > 0 and current_time < end_time:
            # Determine focus period duration for this iteration
            current_focus_duration = min(focus_duration, task['remaining_duration'])
            
            # Add focus period
            focus_end_time = current_time + timedelta(minutes=current_focus_duration)
            if focus_end_time > end_time:
                # Don't go beyond the end time
                focus_end_time = end_time
                current_focus_duration = (focus_end_time - current_time).total_seconds() / 60
            
            pomodoro_schedule.append({
                'task': task['task'],
                'category': task['category'],
                'start': current_time.strftime("%I:%M %p"),
                'end': focus_end_time.strftime("%I:%M %p"),
                'pomodoro_type': 'focus'
            })
            
            # Update remaining duration and current time
            task['remaining_duration'] -= current_focus_duration
            current_time = focus_end_time
            pomodoro_count += 1
            
            # If task is completed or we've reached the end time, break the loop
            if task['remaining_duration'] <= 0 or current_time >= end_time:
                break
                
            # Add appropriate break based on Pomodoro count
            if pomodoro_count % sessions_before_long_break == 0:
                # Long break after specified number of sessions
                break_duration = long_break
                break_type = 'Long Break'
            else:
                # Short break
                break_duration = short_break
                break_type = 'Short Break'
                
            break_end_time = current_time + timedelta(minutes=break_duration)
            if break_end_time > end_time:
                break_end_time = end_time
                
            pomodoro_schedule.append({
                'task': break_type,
                'category': 'Break',
                'start': current_time.strftime("%I:%M %p"),
                'end': break_end_time.strftime("%I:%M %p"),
                'pomodoro_type': 'break'
            })
            
            current_time = break_end_time
            if current_time >= end_time:
                break
    
    # Process other tasks normally (without strict Pomodoro intervals)
    for task in other_tasks:
        # If we've reached the end time, stop scheduling
        if current_time >= end_time:
            break
            
        task_end_time = current_time + timedelta(minutes=task['duration'])
        if task_end_time > end_time:
            task_end_time = end_time
            
        pomodoro_schedule.append({
            'task': task['task'],
            'category': task['category'],
            'start': current_time.strftime("%I:%M %p"),
            'end': task_end_time.strftime("%I:%M %p"),
            'pomodoro_type': 'other'
        })
        
        current_time = task_end_time
    
    return pomodoro_schedule

def generate_daily_schedule_with_pomodoro(tasks, categories, start_times, end_times, energy, pomodoro_settings):
    """
    Generate a full daily schedule with Pomodoro technique applied to focus tasks.
    
    Parameters:
    - tasks: List of task names
    - categories: List of task categories
    - start_times: List of start times (string format)
    - end_times: List of end times (string format)
    - energy: User's energy level
    - pomodoro_settings: Dictionary of Pomodoro settings
    
    Returns:
    - schedule: Full daily schedule with Pomodoro blocks
    """
    # Parse user-provided start and end times
    parsed_start_times = [datetime.strptime(t, "%H:%M") for t in start_times]
    parsed_end_times = [datetime.strptime(t, "%H:%M") for t in end_times]
    
    # Calculate durations for each task
    durations = []
    for i in range(len(parsed_start_times)):
        duration_delta = parsed_end_times[i] - parsed_start_times[i]
        duration_minutes = duration_delta.total_seconds() / 60
        durations.append(duration_minutes)
    
    # Find overall schedule start and end times
    schedule_start = min(parsed_start_times)
    schedule_end = max(parsed_end_times)
    
    # Apply Pomodoro technique
    pomodoro_blocks = apply_pomodoro_technique(
        tasks, categories, durations, 
        schedule_start, schedule_end, 
        pomodoro_settings
    )
    
    # Create final schedule
    schedule = [{'energy': energy}]  # Add energy level information
    schedule.extend(pomodoro_blocks)
    
    return schedule


def generate_task_batching_recommendations(tasks, categories, durations):
    """
    Generate recommendations for task batching based on task categories and durations.
    
    Parameters:
    - tasks: List of task names
    - categories: List of task categories
    - durations: List of task durations (minutes)
    
    Returns:
    - batching_recommendations: Dictionary with batching suggestions
    """
    # Prepare data structure
    task_data = []
    for i in range(len(tasks)):
        task_data.append({
            'task': tasks[i],
            'category': categories[i],
            'duration': durations[i],
            'type': CATEGORY_TYPE_MAP.get(categories[i], 'other')
        })
    
    # Group tasks by category
    category_groups = {}
    for task in task_data:
        if task['category'] not in category_groups:
            category_groups[task['category']] = []
        category_groups[task['category']].append(task)
    
    # Create batching recommendations
    batching_recommendations = {
        'category_batches': [],
        'micro_tasks': [],
        'context_switch_reduction': [],
        'energy_based_batches': {
            'high_energy': [],
            'medium_energy': [],
            'low_energy': []
        }
    }
    
    # 1. Category-based batching
    for category, tasks in category_groups.items():
        if len(tasks) > 1:
            batch = {
                'category': category,
                'tasks': [t['task'] for t in tasks],
                'total_duration': sum(t['duration'] for t in tasks),
                'recommendation': f"Batch {len(tasks)} '{category}' tasks together to maintain context and flow."
            }
            batching_recommendations['category_batches'].append(batch)
    
    # 2. Identify micro-tasks (short tasks that can be batched)
    micro_tasks = [task for task in task_data if task['duration'] <= 10]
    if micro_tasks:
        batching_recommendations['micro_tasks'] = {
            'tasks': [t['task'] for t in micro_tasks],
            'recommendation': f"Batch these {len(micro_tasks)} short tasks together in a single session to quickly clear them."
        }
    
    # 3. Context switch reduction recommendations
    similar_categories = []
    all_categories = list(category_groups.keys())
    
    # Define category relationships (which categories work well together)
    category_relationships = {
        'Admin': ['Documentation', 'Errands & Admin (Personal)'],
        'Documentation': ['Admin', 'Shallow Work'],
        'Collaboration': ['Team Management', 'Client Engagement'],
        'Planning & Strategy': ['Reflection & Review'],
        'Shallow Work': ['Admin', 'Support & Maintenance'],
    }
    
    # Find potential batches based on related categories
    for category in all_categories:
        if category in category_relationships:
            related = [rel for rel in category_relationships[category] if rel in all_categories]
            if related:
                group = {
                    'primary': category,
                    'related': related,
                    'recommendation': f"Reduce context switching by grouping '{category}' tasks with {', '.join(related)} tasks."
                }
                similar_categories.append(group)
    
    batching_recommendations['context_switch_reduction'] = similar_categories
    
    # 4. Energy-based batching
    for task in task_data:
        # Focus tasks often require high energy
        if task['type'] == 'focus':
            batching_recommendations['energy_based_batches']['high_energy'].append(task['task'])
        # Admin/shallow work can be done with medium energy
        elif task['category'] in ['Admin', 'Shallow Work', 'Documentation']:
            batching_recommendations['energy_based_batches']['medium_energy'].append(task['task'])
        # Other tasks might be suitable for low energy periods
        else:
            batching_recommendations['energy_based_batches']['low_energy'].append(task['task'])
    
    return batching_recommendations

