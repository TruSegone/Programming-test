import tkinter as tk
import sqlite3

class SurveyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Survey App")
        self.geometry("400x500")
        self.create_widgets()
        self.connection = sqlite3.connect("survey_data.db")
        self.create_survey_table()

    def create_widgets(self):
        self.fill_survey_button = tk.Button(self, text="Fill out survey", command=self.show_screen2)
        self.fill_survey_button.pack(pady=10)

        self.view_results_button = tk.Button(self, text="View survey results", command=self.show_screen3)
        self.view_results_button.pack(pady=10)

    def create_survey_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS survey (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            surname TEXT,
            first_names TEXT,
            contact_number TEXT,
            date TEXT,
            age INTEGER,
            food TEXT,
            eat_out_rating INTEGER,
            watch_movies_rating INTEGER,
            watch_tv_rating INTEGER,
            listen_radio_rating INTEGER
        )''')
        self.connection.commit()

    def show_screen2(self):
        self.clear_screen()

        self.title_label = tk.Label(self, text="Take our Survey")
        self.title_label.pack(pady=10)

        # Labels and entry fields for personal details
        self.surname_label = tk.Label(self, text="Surname:")
        self.surname_label.pack()
        self.surname_entry = tk.Entry(self)
        self.surname_entry.pack()

        self.first_names_label = tk.Label(self, text="First Names:")
        self.first_names_label.pack()
        self.first_names_entry = tk.Entry(self)
        self.first_names_entry.pack()

        self.contact_number_label = tk.Label(self, text="Contact Number:")
        self.contact_number_label.pack()
        self.contact_number_entry = tk.Entry(self)
        self.contact_number_entry.pack()


        self.date_label = tk.Label(self, text="Date:")
        self.date_label.pack()
        self.date_entry = tk.Entry(self)
        self.date_entry.pack()

        self.age_label = tk.Label(self, text="Age:")
        self.age_label.pack()
        self.age_entry = tk.Entry(self)
        self.age_entry.pack()

        self.food_label = tk.Label(self, text="What is your favourite food?")
        self.food_label.pack()

         # Checkboxes for food options
        self.food_options = ["Pizza", "Pasta", "Pap and Wors", "Chicken stir fry", "Beef stir fry", "Other"]
        self.food_vars = []
        for option in self.food_options:
            var = tk.StringVar()
            checkbox = tk.Checkbutton(self, text=option, variable=var, onvalue="on", offvalue="")
            checkbox.pack()
            self.food_vars.append((var, option))

        self.rating_label = tk.Label(self, text="On a scale of 1 to 5, indicate whether you agree:")
        self.rating_label.pack()

         # Radio buttons for rating options
        self.rating_options = {
            "I like to eat out": tk.IntVar(),
            "I like to watch movies": tk.IntVar(),
            "I like to watch TV": tk.IntVar(),
            "I like to listen to the radio": tk.IntVar()
        }
        for option, var in self.rating_options.items():
            rating_label = tk.Label(self, text=option)
            rating_label.pack()
            rating_option_frame = tk.Frame(self)
            rating_option_frame.pack()
            for i in range(1, 6):
                rating_option = tk.Radiobutton(rating_option_frame, text=str(i), variable=var, value=i)
                rating_option.pack(side="left")

        self.submit_button = tk.Button(self, text="Submit", command=self.submit_survey)
        self.submit_button.pack(pady=10)



    def submit_survey(self):
        surname = self.surname_entry.get()
        first_names = self.first_names_entry.get()
        contact_number = self.contact_number_entry.get()
        date = self.date_entry.get()
        age = self.age_entry.get()
        food = ", ".join(option for var, option in self.food_vars if var.get() == "on")
        eat_out_rating = self.rating_options["I like to eat out"].get()
        watch_movies_rating = self.rating_options["I like to watch movies"].get()
        watch_tv_rating = self.rating_options["I like to watch TV"].get()
        listen_radio_rating = self.rating_options["I like to listen to the radio"].get()

        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO survey (
        surname, first_names, contact_number, date, age, food, eat_out_rating,
        watch_movies_rating, watch_tv_rating, listen_radio_rating
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (surname, first_names, contact_number, date, age, food, eat_out_rating,
        watch_movies_rating, watch_tv_rating, listen_radio_rating))
        self.connection.commit()

        self.clear_screen()

        self.submitted_label = tk.Label(self, text="Survey submitted. Thank you!")
        self.submitted_label.pack(pady=10)

        self.show_screen1()

    def show_screen3(self):
        self.clear_screen()

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM survey")
        survey_data = cursor.fetchall()

        if survey_data:
            self.title_label = tk.Label(self, text="Survey Results")
            self.title_label.pack(pady=10)

            self.results_text = tk.Text(self)
            self.results_text.pack()

            for row in survey_data:
                self.results_text.insert(tk.END, f"Survey ID: {row[0]}\n")
                self.results_text.insert(tk.END, f"Surname: {row[1]}\n")
                self.results_text.insert(tk.END, f"First Names: {row[2]}\n")
                self.results_text.insert(tk.END, f"Contact Number: {row[3]}\n")
                self.results_text.insert(tk.END, f"Date: {row[4]}\n")
                self.results_text.insert(tk.END, f"Age: {row[5]}\n")
                self.results_text.insert(tk.END, f"Food: {row[6]}\n")
                self.results_text.insert(tk.END, f"I like to eat out: {row[7]}\n")
                self.results_text.insert(tk.END, f"I like to watch movies: {row[8]}\n")
                self.results_text.insert(tk.END, f"I like to watch TV: {row[9]}\n")
                self.results_text.insert(tk.END, f"I like to listen to the radio: {row[10]}\n")
                self.results_text.insert(tk.END, "-" * 30)
                self.results_text.insert(tk.END, "\n")


            self.results_text.configure(state="disabled")
        else:
            self.no_results_label = tk.Label(self, text="No survey results found.")
            self.no_results_label.pack(pady=10)

        self.ok_button = tk.Button(self, text="OK", command=self.show_screen1)
        self.ok_button.pack(pady=10)

    def show_screen1(self):
        self.clear_screen()
        self.create_widgets()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = SurveyApp()
    app.mainloop()
