# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-


import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import json
import os
import csv
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates

# --- Constants & Config ---
DATA_FILE = "mood_data.json"
APP_TITLE = "My Mood Tracker & Psychoeducation"
THEME_COLOR = "#2c3e50"
ACCENT_COLOR = "#3498db"
BG_COLOR = "#ecf0f1"
TEXT_COLOR = "#2c3e50"

# --- Disclaimer Text ---
DISCLAIMER_TEXT = """MEDICAL DISCLAIMER

1. NO MEDICAL ADVICE: This software is for educational and self-tracking purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment.

2. CONSULT A PROFESSIONAL: Always seek the advice of your physician, therapist, or other qualified health provider with any questions you may have regarding a medical condition. Never disregard professional medical advice or delay in seeking it because of something you have tracked or read in this application.

3. EMERGENCIES: If you think you may have a medical emergency, are feeling unsafe, or are thinking about hurting yourself, call your local emergency services or a suicide prevention hotline immediately.

4. DATA PRIVACY: Your data is stored locally on this computer in a text file. Please ensure your device is secure to protect your privacy."""

# --- Informational Content (Psychoeducation) ---
INFO_CONTENT = {
    "Positive Psychology (PERMA)": """POSITIVE PSYCHOLOGY & THE PERMA MODEL

Positive psychology is the scientific study of what makes life most worth living. It focuses on strengths instead of weaknesses.

The PERMA Model (Dr. Martin Seligman):
P - Positive Emotion: Feeling good, optimism, pleasure, and enjoyment.
E - Engagement (Flow): Losing track of time in activities you love.
R - Relationships: Authentic, supportive connections with others.
M - Meaning: Belonging to and serving something bigger than yourself.
A - Accomplishment: Pursuing success, winning, achievement, and mastery.

Key Practice: "Three Good Things". Write down 3 things that went well today and why. This retrains the brain to scan for the positive.""",

    "Depression": """UNDERSTANDING DEPRESSION

Depression is more than just feeling sad. It is a mood disorder that causes a persistent feeling of sadness and loss of interest.

Common Tracking Metrics (PHQ-9):
1. Anhedonia: Little interest or pleasure in doing things.
2. Low Mood: Feeling down, depressed, or hopeless.
3. Sleep Changes: Trouble falling/staying asleep, or sleeping too much.
4. Energy: Feeling tired or having little energy.
5. Appetite: Poor appetite or overeating.

Coping Tip: "Behavioral Activation" - Do the thing, and the motivation will follow. Start with very small tasks.""",

    "Anxiety": """UNDERSTANDING ANXIETY (GAD)

Generalized Anxiety Disorder involves persistent and excessive worry that interferes with daily activities.

Common Tracking Metrics (GAD-7):
1. Nervousness: Feeling anxious or on edge.
2. Worry: Not being able to stop or control worrying.
3. Relaxation: Trouble relaxing.
4. Restlessness: Being so restless that it is hard to sit still.
5. Irritability: Becoming easily annoyed.

Coping Tip: The 5-4-3-2-1 Grounding Technique. Acknowledge 5 things you see, 4 you feel, 3 you hear, 2 you smell, and 1 you taste.""",

    "Social Anxiety": """SOCIAL ANXIETY DISORDER

Fear of social situations that involve interaction with other people.

Key Metrics:
- Fear of Judgment: Worrying about being humiliated or judged.
- Avoidance: Staying away from social gatherings.
- Physical Symptoms: Blushing, sweating, trembling.
- Post-Event Rumination: Replaying interactions in your head repeatedly.

Coping: "Spotlight Effect" - Remind yourself that people are not paying as much attention to you as you think.""",

    "Bipolar Disorder": """BIPOLAR DISORDER TRACKING

Tracking is crucial in Bipolar Disorder to catch the shift between states before they become severe.

Mania/Hypomania Signs:
- Decreased need for sleep (feeling rested after 3 hours).
- Racing thoughts or rapid speech.
- Impulsive behavior (spending, risks).
- Inflated self-esteem or grandiosity.

Depressive Signs:
- Crash in energy.
- Withdrawal from social contact.

Goal: Maintain a stable rhythm of sleep and wake times (Social Rhythm Therapy).""",

    "PTSD": """POST-TRAUMATIC STRESS DISORDER

PTSD develops in some people who have experienced a shocking, scary, or dangerous event.

Key Symptoms to Track:
- Intrusive Memories: Flashbacks or nightmares.
- Avoidance: Staying away from places/events that remind you of the trauma.
- Hyperarousal: Being easily startled, feeling tense (hypervigilance).
- Negative Mood: Distorted beliefs about oneself or the world.

Coping: Focus on "Safety" in the present moment. Remind yourself: 'I am safe now.'""",

    "ADHD": """ATTENTION DEFICIT HYPERACTIVITY DISORDER

ADHD is not just a deficit of attention, but a difficulty in regulating attention.

Key Metrics:
- Executive Dysfunction: Difficulty starting tasks (task paralysis).
- Time Blindness: Difficulty estimating how long things take.
- Impulsivity: Acting without thinking.
- Dopamine Seeking: Constant need for stimulation.

Strategy: Use "Body Doubling" (working alongside someone else) to help with task initiation.""",

    "Eating Disorders": """EATING DISORDERS & BODY IMAGE

Tracking should focus on behaviors and feelings, not just numbers.

Key Metrics:
- Restriction Urges: The drive to limit food intake.
- Binge/Purge Urges: The compulsion to overeat or compensate.
- Body Image Distress: Preoccupation with body shape/weight.
- Anxiety around Mealtimes.

Goal: Mechanical Eating - eating at regular intervals regardless of hunger cues to stabilize blood sugar and mood.""",

    "Substance Use": """SUBSTANCE USE & RECOVERY

Tracking triggers is key to relapse prevention.

Key Metrics:
- Craving Intensity: How strong is the urge? (0-100).
- Trigger Exposure: Did you encounter high-risk situations?
- Coping Skill Utilization: Did you use your tools?
- Emotional Regulation: Ability to manage feelings without substances.

Tip: "Urge Surfing" - Imagine the craving as a wave. It will rise, peak, and eventually crash and recede. You just have to ride it out.""",

    "Sleep Hygiene": """SLEEP HYGIENE

Sleep is the foundation of mental health.

Key Metrics:
- Quantity: Total hours slept.
- Quality: Deep vs light sleep, feeling rested.
- Latency: How long it takes to fall asleep.

Tips:
- Keep a consistent wake-up time.
- No screens 1 hour before bed.
- Keep the room cool and dark.""",

    "Anger Management": """ANGER MANAGEMENT

Anger is a normal emotion, but it can become destructive if uncontrolled.

Key Metrics:
- Irritability: Baseline frustration level.
- Triggers: Identifying what sets you off.
- Cool Down Time: How long it takes to return to baseline.

Technique: "Time Out" - Remove yourself from the situation before you react. Take a walk or practice deep breathing."""
}

class DataManager:
    def __init__(self):
        self.data = self.load_data()

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            return self.create_default_data()

        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                if "topics" not in data or "entries" not in data:
                    return self.create_default_data()
                return data
        except (json.JSONDecodeError, IOError):
            return self.create_default_data()

    def create_default_data(self):
        return {
            "topics": {
                "Depression (PHQ-9 Markers)": ["Interest/Pleasure", "Feeling Down/Depressed", "Sleep Quality", "Energy Levels", "Appetite Change", "Feeling of Failure", "Concentration"],
                "Anxiety (GAD-7 Markers)": ["Nervousness", "Uncontrollable Worry", "Trouble Relaxing", "Restlessness", "Irritability", "Fear of Something Awful"],
                "Social Anxiety": ["Fear of Judgment", "Avoidance of Social Situations", "Physical Symptoms (Sweating/Shaking)", "Post-Event Rumination"],
                "Bipolar (Mood & Rhythm)": ["Elevated Mood (High)", "Depressed Mood (Low)", "Hours of Sleep", "Impulsivity", "Racing Thoughts", "Irritability"],
                "Schizophrenia & Psychosis": ["Auditory Hallucinations", "Visual Hallucinations", "Paranoia", "Thought Clarity", "Social Withdrawal"],
                "PTSD & Trauma": ["Flashbacks", "Nightmares", "Hypervigilance", "Startle Response", "Avoidance of Triggers"],
                "OCD": ["Obsessive Thoughts", "Compulsive Rituals", "Distress Level", "Time Spent on Rituals"],
                "ADHD & Focus": ["Focus/Concentration", "Hyperactivity", "Impulsivity", "Task Initiation Difficulty", "Procrastination"],
                "Eating Disorders": ["Body Image Distress", "Restriction Urges", "Binge Urges", "Purge Urges", "Anxiety at Meals"],
                "Substance Use Recovery": ["Craving Intensity", "Trigger Exposure", "Coping Skill Use", "Commitment to Sobriety"],
                "Sleep Hygiene": ["Hours Slept", "Sleep Quality", "Difficulty Falling Asleep", "Nighttime Awakenings", "Daytime Drowsiness"],
                "Anger Management": ["Irritability Level", "Trigger Frequency", "Intensity of Outbursts", "Time to Cool Down", "Regret/Guilt"],
                "Chronic Pain": ["Pain Level", "Fatigue", "Brain Fog", "Mobility", "Impact on Mood"],
                "Self-Esteem": ["Self-Worth", "Confidence", "Negative Self-Talk", "Acceptance of Flaws"],
                "Positive Psychology (PERMA)": ["Positive Emotions", "Engagement (Flow)", "Relationships", "Meaning/Purpose", "Accomplishment"],
                "Character Strengths": ["Curiosity", "Gratitude", "Kindness", "Bravery", "Perseverance", "Hope/Optimism"]
            },
            "entries": []
        }

    def save_data(self):
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump(self.data, f, indent=4)
        except IOError as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")

    def add_entry(self, topic, values, note=""):
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "topic": topic,
            "values": values,
            "note": note
        }
        self.data["entries"].append(entry)
        self.save_data()

    def add_topic(self, topic_name):
        if topic_name and topic_name not in self.data["topics"]:
            self.data["topics"][topic_name] = ["General Rating"]
            self.save_data()

    def delete_topic(self, topic_name):
        if topic_name in self.data["topics"]:
            del self.data["topics"][topic_name]
            self.save_data()

    def add_slider(self, topic, slider_name):
        if topic in self.data["topics"] and slider_name and slider_name not in self.data["topics"][topic]:
            self.data["topics"][topic].append(slider_name)
            self.save_data()

    def delete_slider(self, topic, slider_name):
        if topic in self.data["topics"] and slider_name in self.data["topics"][topic]:
            self.data["topics"][topic].remove(slider_name)
            self.save_data()

    def export_to_csv(self, filepath):
        headers = ["Date", "Time", "Topic", "Metric", "Value (0-100)", "Note"]
        try:
            with open(filepath, mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                for entry in self.data["entries"]:
                    dt_str = entry["timestamp"]
                    try:
                        dt_obj = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
                        date_val = dt_obj.strftime("%Y-%m-%d")
                        time_val = dt_obj.strftime("%H:%M:%S")
                    except ValueError:
                        date_val = dt_str
                        time_val = ""
                    topic = entry["topic"]
                    note = entry.get("note", "").replace('\n', ' ')
                    for slider_name, val in entry["values"].items():
                        writer.writerow([date_val, time_val, topic, slider_name, val, note])
            return True, "Export successful!"
        except Exception as e:
            return False, str(e)

class CustomSlider(tk.Frame):
    def __init__(self, parent, label_text, initial_value=50):
        super().__init__(parent, bg="white", pady=10, padx=10, bd=1, relief="solid")
        self.pack(fill="x", pady=5, padx=5)
        header = tk.Frame(self, bg="white")
        header.pack(fill="x")
        self.label = tk.Label(header, text=label_text, font=("Helvetica", 11, "bold"), bg="white", fg=TEXT_COLOR)
        self.label.pack(side="left")
        self.value_label = tk.Label(header, text=str(initial_value), font=("Helvetica", 12, "bold"), bg="white", fg=ACCENT_COLOR)
        self.value_label.pack(side="right")
        style = ttk.Style()
        style.configure("TScale", background="white")
        self.var = tk.DoubleVar(value=initial_value)
        self.scale = ttk.Scale(self, from_=0, to=100, orient="horizontal", variable=self.var, command=self.update_value, style="TScale")
        self.scale.pack(fill="x", pady=(5, 0))

    def update_value(self, value):
        try:
            val = int(float(value))
            self.value_label.config(text=str(val))
        except ValueError:
            pass
    def get_value(self):
        return int(self.var.get())

class MoodTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("950x800")
        self.configure(bg=BG_COLOR)
        self.db = DataManager()
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", padding=6, relief="flat", background=ACCENT_COLOR, foreground="white", font=("Helvetica", 10, "bold"))
        style.map("TButton", background=[("active", "#2980b9")])
        style.configure("Header.TLabel", font=("Helvetica", 18, "bold"), background=BG_COLOR, foreground=THEME_COLOR)

        # Disclaimer Button Style (Red/Warning)
        style.configure("Disclaimer.TButton", padding=6, relief="flat", background="#c0392b", foreground="white", font=("Helvetica", 9, "bold"))
        style.map("Disclaimer.TButton", background=[("active", "#e74c3c")])

        self.container = tk.Frame(self, bg=BG_COLOR)
        self.container.pack(fill="both", expand=True)
        self.show_main_menu()

    def clear_frame(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def _create_scrollable_area(self):
        canvas = tk.Canvas(self.container, bg=BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=BG_COLOR)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        def on_canvas_configure(event):
            canvas.itemconfig(window_id, width=event.width)
        canvas.bind("<Configure>", on_canvas_configure)
        canvas.configure(yscrollcommand=scrollbar.set)
        return canvas, scrollbar, scrollable_frame

    def show_main_menu(self):
        self.clear_frame()
        header = ttk.Label(self.container, text="Mood Tracker & Info Hub", style="Header.TLabel")
        header.pack(pady=30)
        btn_frame = tk.Frame(self.container, bg=BG_COLOR)
        btn_frame.pack(pady=20)

        # Primary Actions
        ttk.Button(btn_frame, text="Add New Entry", command=self.show_entry_selection).pack(fill="x", pady=8, ipadx=20)
        ttk.Button(btn_frame, text="View Graphs & History", command=self.show_history_selection).pack(fill="x", pady=8, ipadx=20)

        # New Info Section
        ttk.Separator(btn_frame, orient='horizontal').pack(fill='x', pady=15)
        ttk.Button(btn_frame, text="Psychoeducation & Info", command=self.show_info_menu).pack(fill="x", pady=8, ipadx=20)

        # Configuration
        ttk.Separator(btn_frame, orient='horizontal').pack(fill='x', pady=15)
        ttk.Button(btn_frame, text="Manage Topics & Sliders", command=self.show_settings).pack(fill="x", pady=8, ipadx=20)
        ttk.Button(btn_frame, text="Export Data to CSV", command=self.export_data_dialog).pack(fill="x", pady=8, ipadx=20)

        # Disclaimer Button
        ttk.Separator(btn_frame, orient='horizontal').pack(fill='x', pady=15)
        ttk.Button(btn_frame, text="READ MEDICAL DISCLAIMER", style="Disclaimer.TButton", command=self.show_disclaimer_dialog).pack(fill="x", pady=8, ipadx=20)

    def show_disclaimer_dialog(self):
        messagebox.showwarning("Important Medical Disclaimer", DISCLAIMER_TEXT)

    # --- INFO HUB ---
    def show_info_menu(self):
        self.clear_frame()
        ttk.Label(self.container, text="Psychoeducation Library", style="Header.TLabel").pack(pady=20)

        canvas, scrollbar, scrollable_frame = self._create_scrollable_area()
        canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")

        tk.Label(scrollable_frame, text="Select a topic to learn more:", bg=BG_COLOR, font=("Helvetica", 12)).pack(pady=10)

        for topic in INFO_CONTENT.keys():
            ttk.Button(scrollable_frame, text=topic, command=lambda t=topic: self.show_info_content(t)).pack(pady=5, fill="x", ipadx=50)

        ttk.Button(self.container, text="Back to Main Menu", command=self.show_main_menu).pack(pady=20)

    def show_info_content(self, topic):
        self.clear_frame()
        content = INFO_CONTENT.get(topic, "No information available.")

        # Header
        header_frame = tk.Frame(self.container, bg=BG_COLOR)
        header_frame.pack(fill="x", padx=20, pady=10)
        ttk.Label(header_frame, text=topic, style="Header.TLabel").pack(side="left")
        ttk.Button(header_frame, text="Back", command=self.show_info_menu).pack(side="right")

        # Text Content
        text_frame = tk.Frame(self.container, bg="white", bd=2, relief="groove")
        text_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Force text color (fg) to match app theme so it's visible on white bg
        text_widget = tk.Text(text_frame, wrap="word", font=("Helvetica", 12), padx=20, pady=20, bg="white", fg=TEXT_COLOR, bd=0)
        text_widget.pack(fill="both", expand=True)
        text_widget.insert("1.0", content)
        text_widget.config(state="disabled")

    # --- TRACKING LOGIC ---
    def show_entry_selection(self):
        self.clear_frame()
        ttk.Label(self.container, text="Select Topic to Track", style="Header.TLabel").pack(pady=20)
        topics = list(self.db.data["topics"].keys())
        if not topics:
            tk.Label(self.container, text="No topics found. Please create one in settings.", bg=BG_COLOR).pack()
            ttk.Button(self.container, text="Back", command=self.show_main_menu).pack(pady=10)
            return
        canvas, scrollbar, scrollable_frame = self._create_scrollable_area()
        canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")
        for topic in topics:
            ttk.Button(scrollable_frame, text=topic, command=lambda t=topic: self.show_tracking_form(t)).pack(pady=5, fill="x", ipadx=50)
        ttk.Button(self.container, text="Back", command=self.show_main_menu).pack(pady=20)

    def show_tracking_form(self, topic):
        self.clear_frame()
        sliders = self.db.data["topics"][topic]
        header_frame = tk.Frame(self.container, bg=BG_COLOR)
        header_frame.pack(fill="x", padx=20, pady=10)
        ttk.Label(header_frame, text=f"New Entry: {topic}", style="Header.TLabel").pack(side="left")
        ttk.Button(header_frame, text="Cancel", command=self.show_main_menu).pack(side="right")
        canvas, scrollbar, scrollable_frame = self._create_scrollable_area()
        canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")
        slider_widgets = {}
        for slider_name in sliders:
            sw = CustomSlider(scrollable_frame, slider_name)
            slider_widgets[slider_name] = sw
        tk.Label(scrollable_frame, text="Notes (Optional):", bg=BG_COLOR, font=("Helvetica", 10, "bold")).pack(anchor="w", padx=5, pady=(20, 5))
        note_entry = tk.Text(scrollable_frame, height=4, width=50)
        note_entry.pack(fill="x", padx=5, pady=5)
        def save():
            values = {name: widget.get_value() for name, widget in slider_widgets.items()}
            note = note_entry.get("1.0", "end-1c")
            self.db.add_entry(topic, values, note)
            messagebox.showinfo("Success", "Entry Saved!")
            self.show_main_menu()
        ttk.Button(scrollable_frame, text="SAVE ENTRY", command=save).pack(pady=20, ipadx=30, ipady=5)

    def show_history_selection(self):
        self.clear_frame()
        ttk.Label(self.container, text="Select Topic to View", style="Header.TLabel").pack(pady=20)
        topics = list(self.db.data["topics"].keys())
        canvas, scrollbar, scrollable_frame = self._create_scrollable_area()
        canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")
        for topic in topics:
            ttk.Button(scrollable_frame, text=topic, command=lambda t=topic: self.show_graph(t)).pack(pady=5, fill="x", ipadx=50)
        ttk.Button(self.container, text="Back", command=self.show_main_menu).pack(pady=20)

    def show_graph(self, topic):
        self.clear_frame()
        nav = tk.Frame(self.container, bg=BG_COLOR)
        nav.pack(fill="x", padx=10, pady=10)
        ttk.Button(nav, text="< Back", command=self.show_history_selection).pack(side="left")
        tk.Label(nav, text=f"History: {topic}", font=("Helvetica", 14, "bold"), bg=BG_COLOR).pack(side="left", padx=20)
        raw_entries = [e for e in self.db.data["entries"] if e["topic"] == topic]
        if not raw_entries:
            tk.Label(self.container, text="No entries found for this topic.", bg=BG_COLOR).pack(pady=50)
            return
        parsed_data = []
        for e in raw_entries:
            try:
                dt = datetime.strptime(e["timestamp"], "%Y-%m-%d %H:%M:%S")
                parsed_data.append((dt, e))
            except ValueError:
                continue
        parsed_data.sort(key=lambda x: x[0])
        if parsed_data:
            dates, valid_entries = zip(*parsed_data)
        else:
            tk.Label(self.container, text="Entries exist but date format is invalid.", bg=BG_COLOR).pack(pady=50)
            return
        sliders_data = {}
        possible_sliders = self.db.data["topics"].get(topic, [])
        for s in possible_sliders:
            sliders_data[s] = []
        for e in valid_entries:
            for s in possible_sliders:
                val = e["values"].get(s, None)
                sliders_data[s].append(val)
        fig = Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)
        has_plotted_data = False
        for slider_name, values in sliders_data.items():
            valid_points = [(d, v) for d, v in zip(dates, values) if v is not None]
            if valid_points:
                pd, pv = zip(*valid_points)
                ax.plot(pd, pv, marker='o', label=slider_name, linewidth=2)
                has_plotted_data = True
        ax.set_ylim(0, 105)
        ax.set_title("Mood Trends over Time")
        ax.set_ylabel("Severity / Rating (0-100)")
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        fig.autofmt_xdate()
        if has_plotted_data:
            ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize='small')
            fig.tight_layout()
        else:
            ax.text(0.5, 0.5, "No numeric data to display yet.", horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        ax.grid(True, linestyle='--', alpha=0.6)
        canvas = FigureCanvasTkAgg(fig, master=self.container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        list_frame = tk.Frame(self.container, bg="white", height=150)
        list_frame.pack(fill="x", padx=10, pady=10)
        list_frame.pack_propagate(False)
        lbl = tk.Label(list_frame, text="Recent Entries Log", font=("bold"), bg="white")
        lbl.pack(anchor="w", padx=5, pady=5)
        txt_list = tk.Text(list_frame, height=5, bg="#f9f9f9", bd=0)
        txt_list.pack(fill="both", padx=5, pady=5)
        for e in reversed(valid_entries[-5:]):
            txt_list.insert("end", f"{e['timestamp']} - {e.get('note', '')}\n")
        txt_list.config(state="disabled")

    def show_settings(self):
        self.clear_frame()
        ttk.Label(self.container, text="Settings", style="Header.TLabel").pack(pady=20)
        cols = tk.Frame(self.container, bg=BG_COLOR)
        cols.pack(fill="both", expand=True, padx=20)
        left_col = tk.LabelFrame(cols, text="Topics", bg=BG_COLOR, padx=10, pady=10)
        left_col.pack(side="left", fill="both", expand=True, padx=5)
        right_col = tk.LabelFrame(cols, text="Sliders in Selected Topic", bg=BG_COLOR, padx=10, pady=10)
        right_col.pack(side="right", fill="both", expand=True, padx=5)
        self.topic_listbox = tk.Listbox(left_col)
        self.topic_listbox.pack(fill="both", expand=True)
        for t in self.db.data["topics"]:
            self.topic_listbox.insert("end", t)
        self.topic_listbox.bind('<<ListboxSelect>>', lambda e: self.update_slider_list())
        btn_t_frame = tk.Frame(left_col, bg=BG_COLOR)
        btn_t_frame.pack(fill="x", pady=5)
        ttk.Button(btn_t_frame, text="+ Add Topic", command=self.add_topic_dialog).pack(side="left", fill="x", expand=True)
        ttk.Button(btn_t_frame, text="- Delete", command=self.delete_topic_btn).pack(side="right", fill="x", expand=True)
        self.slider_listbox = tk.Listbox(right_col)
        self.slider_listbox.pack(fill="both", expand=True)
        btn_s_frame = tk.Frame(right_col, bg=BG_COLOR)
        btn_s_frame.pack(fill="x", pady=5)
        ttk.Button(btn_s_frame, text="+ Add Slider", command=self.add_slider_dialog).pack(side="left", fill="x", expand=True)
        ttk.Button(btn_s_frame, text="- Delete", command=self.delete_slider_btn).pack(side="right", fill="x", expand=True)
        ttk.Button(self.container, text="Back to Main Menu", command=self.show_main_menu).pack(pady=20)

    def update_slider_list(self):
        selection = self.topic_listbox.curselection()
        self.slider_listbox.delete(0, "end")
        if selection:
            topic = self.topic_listbox.get(selection[0])
            sliders = self.db.data["topics"][topic]
            for s in sliders:
                self.slider_listbox.insert("end", s)
    def add_topic_dialog(self):
        name = simpledialog.askstring("New Topic", "Enter topic name:")
        if name:
            self.db.add_topic(name)
            self.show_settings()
    def delete_topic_btn(self):
        selection = self.topic_listbox.curselection()
        if selection:
            topic = self.topic_listbox.get(selection[0])
            if messagebox.askyesno("Confirm", f"Delete topic '{topic}'?"):
                self.db.delete_topic(topic)
                self.show_settings()
    def add_slider_dialog(self):
        selection = self.topic_listbox.curselection()
        if not selection:
            messagebox.showwarning("Select Topic", "Please select a topic on the left first.")
            return
        topic = self.topic_listbox.get(selection[0])
        name = simpledialog.askstring("New Slider", f"Enter slider name for {topic}:")
        if name:
            self.db.add_slider(topic, name)
            self.update_slider_list()
    def delete_slider_btn(self):
        t_sel = self.topic_listbox.curselection()
        s_sel = self.slider_listbox.curselection()
        if t_sel and s_sel:
            topic = self.topic_listbox.get(t_sel[0])
            slider = self.slider_listbox.get(s_sel[0])
            self.db.delete_slider(topic, slider)
            self.update_slider_list()
    def export_data_dialog(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")], title="Export Data")
        if filename:
            success, msg = self.db.export_to_csv(filename)
            if success:
                messagebox.showinfo("Export Success", f"Data exported to:\n{filename}")
            else:
                messagebox.showerror("Export Failed", f"Error:\n{msg}")

if __name__ == "__main__":
    app = MoodTrackerApp()
    app.mainloop()