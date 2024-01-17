import tkinter as tk
from tkinter import ttk, Canvas, messagebox, font as tkFont
from datetime import datetime, timedelta
import requests
import random
import pygame

class PuzzlePopApp:
    def __init__(self, master):
        self.master = master
        self.master.title("PuzzlePop")
        self.master.geometry("460x640")

        # Set a custom font for the entire application
        custom_font = tkFont.Font(family="Arial", size=12)
        self.master.option_add("*Font", custom_font)
        self.user_score = 0  # Initializing user's score
        self.timer_seconds = 15  # Initializing timer value
        # Initialize pygame for audio
        pygame.init()
        self.timer_label = None
        self.timer_id = None

         # Load background music for the first page
        pygame.mixer.music.load("C:/Users/afrin/Downloads/bagroundmusic.mp3") 
        pygame.mixer.music.play(-1)  # Play in a loop (-1)

        # Creating a canvas for gradient background
        self.canvas = Canvas(master, width=460, height=640)
        self.canvas.pack()

        # Create gradient background
        self.create_gradient("#FFB6C1", "#FFD700")

        # Creating a title label with typewriter effect
        self.heading_text = "PuzzlePop"
        self.heading_id = self.canvas.create_text(230, 256, text="", font=("Arial", 40, "bold"), fill="#333")
        self.question_index = 0  # Initialize question_index

        # Setting a style for the buttons
        style = ttk.Style()
        style.configure('My.TButton', font=("Arial", 16), bg='#FFC0CB', fg="#333", activebackground="#FFB6C1",
                        activeforeground="#333")

        # Callin the typewrite method to start 
        self.typewrite()

         # Initialize correct_answer as an instance variable
        self.correct_answer = ""

        # Adding the new buttons directly on the canvas
        start_button = ttk.Button(
            master, text="Start Playing", command=self.show_category_page, style="My.TButton"
        )
        start_button_id = self.canvas.create_window(230, 370, window=start_button)

        how_to_play_button = ttk.Button(
            master, text="How to Play", command=self.show_how_to_play_page, style="My.TButton"
        )
        how_to_play_button_id = self.canvas.create_window(230, 430, window=how_to_play_button)

        self.question_index = 0
        self.questions = []

        # Creating confetti objects
        self.confetti_colors = ["#F5A9A9", "#F2F5A9", "#A9F5F2", "#A9A9F5"]
        self.confetti = []
        for _ in range(100):
            x = random.randint(0, 460)
            y = random.randint(0, 640)
            size = random.randint(10, 15)
            color = random.choice(self.confetti_colors)
            oval_id = self.canvas.create_oval(x, y, x + size, y + size, fill=color, outline="")
            self.confetti.append((oval_id, x, y, size))

        # Animating the confettis
        self.animate_confetti()
    
    def play_correct_sound(self):
        pygame.mixer.Sound("C:/Users/afrin/Downloads/correct sound.mp3").play() 

    def play_wrong_sound(self):
        pygame.mixer.Sound("C:/Users/afrin/Downloads/wrong sound.mp3").play() 

    def play_quiz_complete_sound(self, file_path):
     pygame.mixer.Sound(file_path).play()

    #Creating a gradient background
    def create_gradient(self, color1, color2):
        num_steps = 100  
        x1, y1, x2, y2 = 0, 0, 460, 640
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color1, outline="")

        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:], 16)
        r_step = (r2 - r1) / num_steps
        g_step = (g2 - g1) / num_steps
        b_step = (b2 - b1) / num_steps

        for i in range(1, num_steps + 1):
            r = int(r1 + i * r_step)
            g = int(g1 + i * g_step)
            b = int(b1 + i * b_step)
            color = f'#{r:02x}{g:02x}{b:02x}'
            y_start = y1 + (i - 1) * (y2 - y1) / num_steps
            y_end = y1 + i * (y2 - y1) / num_steps
            self.canvas.create_rectangle(x1, y_start, x2, y_end, fill=color, outline="")

    #Typewriter effect for the title label
    def typewrite(self):
        if self.question_index <= len(self.heading_text):
            self.canvas.itemconfig(self.heading_id, text=self.heading_text[:self.question_index])
            self.question_index += 1
            self.master.after(150, self.typewrite)
    #Animating confetti
    def animate_confetti(self):
        for oval_id, x, y, size in self.confetti:
            self.canvas.move(oval_id, 0, 2)
            y += 2
            if y >= 640:
                y = -size
                self.canvas.coords(oval_id, x, y, x + size, y + size)
        self.master.after(80, self.animate_confetti)


    def show_how_to_play_page(self):
        # Create How to Play Page
        how_to_play_page = tk.Toplevel(self.master)
        how_to_play_page.title("How to Play")
        
        
        frame = ttk.Frame(how_to_play_page, style='TFrame')  
        frame.pack(expand=True, fill="both")

        
        # Providing instructions on how to play the game
        instructions = (
            "Welcome to PuzzlePop!\n\n"
            "1. Click 'Start Playing' to begin.\n"
            "2. Choose a category and set the difficulty level.\n"
            "3. Answer the trivia questions and see how many you can get right!\n"
            "4. Enjoy the game and have fun!"
        )

        how_to_play_label = ttk.Label(
            frame,
            text=instructions,
            font=("Arial", 14),
            justify="center",
            wraplength=400,
            background="#ffc0cb"
        )
        how_to_play_label.grid(row=0, column=0, pady=40, padx=30,sticky="nsew")

    def show_category_page(self):
        # Create Category Selection Page
        category_page = tk.Toplevel(self.master)
        category_page.title("Category Selection")
        category_page.configure(bg="#ffc0cb")

        # Setting the size of the window
        category_page.geometry("640x300")  

        # Creating style for buttons
        style = ttk.Style()
        style.configure('My.TButton', font=("Arial", 14, "bold"), background="#ffffff", borderwidth=2)

        # heading
        heading_label = tk.Label(category_page, text="Choose The Category:", bg="#ffc0cb",font=("Arial", 18, "bold",))
        heading_label.grid(row=0, columnspan=4, pady=40)

        #buttons for categories
        categories = ["Literature", "Science", "History", "Movies", "Sports", "Songs", "Art", "Animals"]
        for i, category in enumerate(categories):
            button = ttk.Button(
                category_page,
                text=category,
                style='My.TButton',
                command=lambda cat=category: self.show_difficulty_slider(cat)
            )
            button.grid(row=(i // 4) + 1, column=i % 4, padx=15, pady=10)

    def show_difficulty_slider(self, selected_category):
    # Difficulty Selection Page with Slider
     difficulty_page = tk.Toplevel(self.master)
     difficulty_page.title("Difficulty Selection")
     difficulty_page.geometry("400x200")
     difficulty_page.configure(bg="#ffff94")

    # Store the selected category for future use
     self.selected_category = selected_category

    # ttk style for the title label
     style = ttk.Style()
     style.configure('Title.TLabel', font=("Arial", 16, "bold"))

    
    #a slider for difficulty levels
     difficulty_slider = tk.Scale(difficulty_page, from_=0, to=2, orient=tk.HORIZONTAL,
                             label="Choose Your Difficulty Level:", resolution=1, length=300, tickinterval=1,
                             font=("Arial", 12, "bold"),bg="#ffffff")
     difficulty_slider.set(1)
     difficulty_slider.pack()

     #style for the button
     style = ttk.Style()
     style.configure('BigButton.TButton', font=("Arial", 14))

    
     ttk.Button(difficulty_page, text="Start Game", style='BigButton.TButton', padding=5, command=lambda: self.fetch_and_show_questions(difficulty_slider.get())).pack()
     

    def fetch_and_show_questions(self, selected_difficulty): 

    # Fetch questions from the Open Trivia API
       api_url = "https://opentdb.com/api.php"
       params = {
        "amount": 5,
        "category": self.get_category_id(self.selected_category),
        "difficulty": self.get_difficulty_name(selected_difficulty),
        "type": "multiple",}

       response = requests.get(api_url, params=params)
       data = response.json()

      # Process the API response and store questions
       self.questions = data.get("results", [])

       # Reset the question index
       self.question_index = 0

       # Show the first question
       self.show_question_page()

    def start_timer(self):
        if self.timer_seconds > 0:
            # Update the timer label
            self.timer_label.config(text=f"Time Left: {self.timer_seconds}s")

            # Decrement the timer value
            self.timer_seconds -= 1

           
            self.timer_id = self.master.after(1000, self.start_timer)
        else:
            # If time runs out,it will show a message and reveal the correct answer
            self.result_label.config(text=f"Time's up! Correct answer: {self.correct_answer}", fg="red")

            # to Disable radio buttons after time expires
            for child in self.question_page.winfo_children():
                if isinstance(child, tk.Radiobutton):
                    child.config(state=tk.DISABLED)

            # Move to the next question after a delay 
            self.master.after(2000, self.show_next_question)

    def show_question_page(self):
        if self.question_index < len(self.questions):
            # Create Question Page
            if hasattr(self, 'question_page'):
                self.question_page.destroy()

            self.question_page = tk.Toplevel(self.master)
            self.question_page.configure(bg="#ffffff")  
            self.question_page.title(f"Question {self.question_index + 1}")

            question_data = self.questions[self.question_index]
            question_text = question_data["question"]
            options = question_data["incorrect_answers"] + [question_data["correct_answer"]]

            # Set correct_answer as an instance variable
            self.correct_answer = question_data["correct_answer"]
            
            tk.Label(self.question_page, text=question_text, bg="#ffffff", font=("Arial", 14)).pack()

            # Create a StringVar to store the selected answer
            self.selected_option = tk.StringVar()

            for option in options:
                tk.Radiobutton(self.question_page, text=option, variable=self.selected_option, value=option,
                borderwidth=7, padx=15, pady=5, bg="#ffffff").pack()

            # Add a label for displaying the result
            self.result_label = tk.Label(self.question_page, text="",bg="#ffffff", font=("Arial", 12))
            self.result_label.pack()

            # Adding a label to display the timer
            self.timer_label = tk.Label(self.question_page, text=f"Time Left: {self.timer_seconds}s",bg="#ffc0cb", font=("Arial", 12))
            self.timer_label.pack()
 
            # Start the timer
            self.start_timer()

             # Add a button to submit the answer and proceed to the next question
            tk.Button(self.question_page, text="Submit Answer", command=lambda ans=self.correct_answer: self.check_answer(ans)).pack()
            tk.Button(self.question_page, text="Next Question", command=self.show_next_question).pack()

        else:
            self.play_quiz_complete_sound("C:/Users/afrin/Downloads/completed sound.mp3")
            messagebox.showinfo("Game Over", f"Congratulations! You have completed the quiz.\nYour Score: {self.user_score}")
           

    def check_answer(self, correct_answer):
        # Get the selected answer from the radio buttons
        selected_option = self.selected_option.get()

        if selected_option == correct_answer:
            self.result_label.config(text="Correct!", fg="green")
            # Increment the user_score when the answer is correct
            self.user_score += 1
            self.play_correct_sound() 
        else:
            self.result_label.config(text=f"Incorrect! Correct answer: {correct_answer}", fg="red")
            self.play_wrong_sound()  
        
        # Cancel the scheduled timer event
        self.master.after_cancel(self.timer_id)

        # Disable radio buttons after submitting the answer
        for child in self.question_page.winfo_children():
            if isinstance(child, tk.Radiobutton):
                child.config(state=tk.DISABLED)

    def show_next_question(self):
    # Move to the next question only if it hasn't been called before
     if self.question_index < len(self.questions):
        # Move to the next question
        self.question_index += 1

        # Reset the timer
        self.reset_timer()

        # Show the next question
        self.show_question_page()
     else:
        self.play_quiz_complete_sound() 
        # Display Game Over message if all questions are completed
        messagebox.showinfo("Game Over", f"Congratulations! You have completed the quiz.\nYour Score: {self.user_score}")
         


    def reset_timer(self):
        self.timer_seconds = 15

    @staticmethod
    def get_category_id(category_name):
       
        categories = {
            "Movies": 11,
            "Music": 12,
            "World": 22,
            "General": 9
            
        }
        return categories.get(category_name, 9)  # Default to General category if not found

    @staticmethod
    def get_difficulty_name(difficulty_level):
        
        difficulty_names = {0: "easy", 1: "medium", 2: "hard"}
        return difficulty_names.get(difficulty_level, "medium") 
    
    

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzlePopApp(root)
    root.mainloop()
