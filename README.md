# AI-Based Productivity Coach
<div align="justify">
This web-based productivity dashboard is designed to help individuals, students, and professionals organise their tasks, manage their time, and track their daily activities with enhanced efficiency. Built using Flask, HTML, CSS, and JavaScript, the application integrates smart scheduling tools and visual progress indicators to provide users with an intuitive and interactive experience. It supports dynamic task updates, categorisation, and daily summaries, empowering users to prioritise their goals and stay focused. By incorporating productivity techniques like the Pomodoro method and intelligent task batching, the application fosters a well-structured approach to time management. Whether you're working on personal goals or managing multiple professional commitments, this dashboard is tailored to improve productivity, ensure optimal use of time, and support a balanced workflow.
</div>

## Table of Contents
- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Fork and Clone the Repository](#fork-and-clone-the-repository)
  - [Setting up a Python Virtual Environment](#setting-up-a-python-virtual-environment)
  - [Installing Dependencies](#installing-dependencies)
- [Running the Application](#running-the-application)
- [Usage Guide](#usage-guide)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)


## About the Application

## Features

- Task management with smart prioritisation
- Pomodoro Technique
- Habit tracking and reinforcement
- Focus session management with Pomodoro technique
- Personalised productivity insights and recommendations
- Progress visualisation and reporting
- AI-powered coaching based on your work patterns
- Task creation and categorisation (e.g., Work, Study, Personal)
- Live digital clock and date tracking
- Visual task progress indicators with completion animations
- Optimised task scheduling based on time and priority
- Integration of the Pomodoro Technique for time-blocked focus sessions
- Recommendations for task batching to improve efficiency and reduce context switching
- Toggle-based views for completed vs. pending tasks
- Responsive design adaptable to mobile and desktop screens
- Animated transitions for task status updates
- End-of-day summary and reset functionality

## Installation

### Prerequisites

Before installing the AI-Based Productivity Coach, ensure you have the following installed on your system:

- Git
- Python 3.8 or higher
- pip (Python package installer)

### Fork and Clone the Repository

1. **Fork the repository**:
   - Visit https://github.com/imosudi/AI-Based-Productivity-Coach
   - Click on the "Fork" button in the top-right corner
   - This creates a copy of the repository in your GitHub account

2. **Clone your forked repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/AI-Based-Productivity-Coach.git
   ```

3. **Navigate to the project directory**:
   ```bash
   cd AI-Based-Productivity-Coach
   ```

### Setting up a Python Virtual Environment

Creating a virtual environment keeps the application's dependencies isolated from other Python projects on your system.

#### For Windows:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate
```

#### For macOS and Linux:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

You'll know the virtual environment is active when your terminal prompt is prefixed with `(venv)`.

### Installing Dependencies

With the virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

This command installs all the necessary dependencies defined in the `requirements.txt` file.

## Running the Application

No additional configuration is needed as the application uses the existing config.py file with the following default settings:

```python
HOST="0.0.0.0"
PORT=9921
DEBUG=True
```

After installation, you can start the application:

```bash
python main.py
```

The application will be running on http://0.0.0.0:9921 (You can access it via http://localhost:9921 in your browser).

## Usage Guide

Once the application is running, you can:

1. **Create an account or log in** if authentication is required
2. **Set up your productivity profile** by answering questions about your work habits
3. **Add tasks and projects** you want to track
4. **Set up habits** you want to develop
5. **Start focus sessions** when you're ready to work
6. **Review insights** from the AI coach to improve your productivity

## Troubleshooting

### Common Issues

1. **Installation errors**:
   - Ensure you have the correct Python version
   - Try upgrading pip: `pip install --upgrade pip`
   - Check for system-specific dependencies mentioned in the error messages

2. **Application won't start**:
   - Ensure port 9921 is not in use by another application
   - Check terminal output for error messages
   - Verify that all dependencies were installed correctly

3. **Dependency conflicts**:
   - Make sure you're using a clean virtual environment
   - Check for specific version requirements in the error messages

### Getting Help

If you encounter issues not covered here:
- Check the [Issues](https://github.com/imosudi/AI-Based-Productivity-Coach/issues) section on GitHub
- Open a new issue with details about your problem and environment

## Contributing

Contributions are welcome! To contribute:

1. Ensure you work from your fork
2. Create a new branch for your feature: `git checkout -b feature-name`
3. Make your changes and commit them: `git commit -m "Add some feature"`
4. Push to your branch: `git push origin feature-name`
5. Open a Pull Request against the original repository

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## About Pomodoro Technique
<div align="justify">
The Pomodoro Technique is a time management method developed by Francesco Cirillo in the late 1980s. It uses a timer to break down work into intervals, traditionally 25 minutes in length, separated by short breaks of around 5 minutes. After completing four such intervals (called "Pomodoros"), a longer break of 15 to 30 minutes is taken. This technique aims to improve focus, minimise mental fatigue, and increase sustained productivity. By working with the natural rhythm of concentration and rest, the Pomodoro Technique helps individuals maintain consistent energy levels and reduce procrastination. The technique is especially effective in environments with high cognitive load, where maintaining attention and discipline is key. It encourages goal setting, frequent review, and the ability to estimate effort more accurately over time, contributing to both short-term task completion and long-term productivity habits.
</div>