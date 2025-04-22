import tkinter as tk
import json
import random

#loading from file example
#def load_flashcards():
   # with open('flaschards.json', 'r') as file:
   #     return json.load(file)['cards']

#set of flashcards loaded from file
#flashcards = load_flashcards()
#TODO- class for flashcards
curr_card = 0

#app window
app = tk.Tk()
class Home(tk.Frame):
    app.title("🧠 Our AI Flashcard Generator!")
    app.geometry("400x300")

    home = tk.Label(app, text = "🧠 Our AI Flashcard Generator!")
    study_flashcard = tk.Button(app, text = "Study Flashcards", #command = lambda : controller.show_frame(StudyFlashcards)
                                )
    study_flashcard.pack(pady = 10)

#question display to screen
#commented out until file name is entered
#question = tk.Label(app, text=flashcards[curr_card]['question'])
#hardcoded example

class StudyFlashcards(tk.Frame):
    question = tk.Label(app, text="What is the color of plants")
    question.pack(pady=20)

answer_entered = tk.Entry(app)
answer_entered.pack(pady=20)


#function to check provided answer with answer from file
def is_answer_entered_correct():
    answer = answer_entered.get()
    #if answer.lower() == flashcards[curr_card]['answer'].lower():
        #result.config(text = "Correct", fg = "green")
    if answer.lower() == 'green':
        result.config(text="Correct", fg="green")
    else:
        #result.config(text=f"Wrong, the correct answer is {flashcards[curr_card]['answer']}", fg="red")
        result.config(text=f"Wrong, the correct answer is green")


enter_button = tk.Button(app, text="Check input", command = is_answer_entered_correct)
enter_button.pack(pady = 10)


result = tk.Label(app, text='')
result.pack(pady =20)
app.mainloop()