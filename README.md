# My Mood Tracker & Psychoeducation

A desktop application for tracking mental health metrics and accessing evidence-based psychoeducational content. Built with Python and Tkinter, all data stays private on your local machine.

## Features

- **Mood & Symptom Tracking** -- Log daily mental health metrics on a 0-100 scale across customizable categories
- **16 Pre-built Tracking Categories** -- Depression (PHQ-9), Anxiety (GAD-7), Social Anxiety, Bipolar, PTSD, OCD, ADHD, Eating Disorders, Substance Use Recovery, Sleep Hygiene, Anger Management, Chronic Pain, Self-Esteem, Positive Psychology (PERMA), Character Strengths, and Schizophrenia & Psychosis
- **Trend Graphs** -- Visualize your data over time with interactive line charts
- **Psychoeducation Library** -- Read evidence-based information on 13+ mental health topics
- **Custom Categories** -- Add your own tracking topics and metrics
- **CSV Export** -- Export your data for use in spreadsheets or other tools
- **Local-only Storage** -- All data stored in a local JSON file; nothing is sent to the cloud

## Screenshots

The application launches with a main menu providing access to all features:

- Add New Entry
- View Graphs & History
- Psychoeducation & Info
- Manage Topics & Sliders
- Export Data to CSV

## Requirements

- Python 3.x
- `matplotlib`
- `tkinter` (included with most Python installations)

## Installation

```bash
# Clone the repository
git clone https://github.com/hamishdean/Mood_tracker.git
cd Mood_tracker

# Install dependencies
pip install matplotlib
```

## Usage

```bash
python mood_tracker.py
```

The application opens a GUI window where you can:

1. **Track** -- Select a category, adjust sliders for each metric (0-100), add optional notes, and save
2. **Review** -- View trend graphs and your most recent entries
3. **Learn** -- Browse psychoeducation content on various mental health topics
4. **Customize** -- Add or remove tracking categories and individual metrics
5. **Export** -- Save all recorded data to a CSV file for external analysis

## Data Storage

All user data is stored locally in `mood_data.json` in the working directory. The file is created automatically on first run. No data is transmitted externally.

## Disclaimer

This software is for **educational and self-tracking purposes only**. It is not a substitute for professional medical advice, diagnosis, or treatment. If you are experiencing a mental health emergency, please contact your local emergency services or a crisis hotline immediately.

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).
