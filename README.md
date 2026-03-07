# My Mood Tracker & Psychoeducation

**My Mood Tracker & Psychoeducation** is a Python-based desktop application built with Tkinter. It is designed to help users track their mental health metrics, visualize mood trends over time, and learn about various psychological conditions through a built-in psychoeducation library.

## ⚠️ Medical Disclaimer

This software is for **educational and self-tracking purposes only**.

* It is **NOT** a substitute for professional medical advice, diagnosis, or treatment.
* Always seek the advice of your physician, therapist, or other qualified health provider with any questions you may have.
* If you are experiencing a medical emergency, feeling unsafe, or thinking about hurting yourself, **call your local emergency services or a suicide prevention hotline immediately**.

## Features

* **Customizable Tracking:** Track various conditions using pre-configured markers (e.g., PHQ-9 for Depression, GAD-7 for Anxiety, PERMA for Positive Psychology) or create your own custom topics and sliders.
* **Data Visualization:** View your logged data on interactive graphs over time to identify trends and patterns, powered by Matplotlib.
* **Psychoeducation Library:** Access built-in informational guides on topics like ADHD, Bipolar Disorder, PTSD, Sleep Hygiene, Substance Use Recovery, and more, complete with coping strategies.
* **Local & Secure Storage:** All data is saved locally to your machine in a `mood_data.json` file, ensuring your personal health data remains private.
* **CSV Export:** Export your tracking history to a `.csv` file to share with your therapist or analyze in a spreadsheet.

## Prerequisites

To run this application, you need **Python 3.x** installed on your system.

You will also need to install the following third-party library:

* `matplotlib` (for generating history graphs)

*Note: `tkinter` is included with most standard Python installations. If you are on Linux, you may need to install it separately via your package manager (e.g., `sudo apt-get install python3-tk`).*

## Installation

1. **Clone the repository:**
```bash
git clone https://gitlab.com/your-username/your-repo-name.git
cd your-repo-name

```


2. **Install dependencies:**
```bash
pip install matplotlib

```


3. **Run the application:**
```bash
python mood_tracker.py

```



## How to Use

1. **Log an Entry:** Click **Add New Entry** from the main menu, select a topic, adjust the sliders (0-100) to reflect your current state, add any optional notes, and click save.
2. **View History:** Click **View Graphs & History** to see a line chart of your tracked metrics over time, alongside a log of your recent entries and notes.
3. **Learn:** Navigate to **Psychoeducation & Info** to read summaries of common mental health topics, standard tracking metrics, and practical coping techniques.
4. **Customize:** Go to **Manage Topics & Sliders** to add new tracking categories or remove ones you don't need.

## Data Privacy

Your privacy is a priority. This application does not connect to the internet to sync or store your data. Everything is saved locally in a JSON file in the same directory as the script. Please ensure your device is password-protected to keep your data secure.

---
