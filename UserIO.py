#from Tkinter import *
import Words as W
# import ALL as A
import random
import Utils as utils

"""
class PracticeGUI:

    def __init__(self, dictionaries):
        self.streak = 0
        self.correct = 0
        self.incorrect = 0
        self.total = 0
        self.accuracy = 0.0
        self.dictionary = {}
        self.used = {}

        self.answer = ''
        self.w = ''

        self.window = Tk()
        self.window.title('Practice Chinese')
        self.window.geometry('300x250')

        self.streak_str = StringVar()
        Label(self.window, textvariable=self.streak_str).pack()

        self.correct_str = StringVar()
        Label(self.window, textvariable=self.correct_str).pack()

        self.incorrect_str = StringVar()
        Label(self.window, textvariable=self.incorrect_str).pack()

        self.total_str = StringVar()
        Label(self.window, textvariable=self.total_str).pack()

        self.accuracy_str = StringVar()
        Label(self.window, textvariable=self.accuracy_str).pack()

        self.last_answer = StringVar()
        Label(self.window, textvariable=self.last_answer).pack()

        self.inp = Entry(self.window)
        self.inp.bind('<Return>', lambda x: self.collect())  # binding the Return event with an handler
        self.inp.pack(side=BOTTOM)

        self.word = StringVar()
        prompt = Label(self.window, textvariable=self.word)
        prompt.pack(side=BOTTOM)

        for d in dictionaries:
            self.dictionary.update(d)

    def updateStats(self):
        self.streak_str.set('Streak: {}'.format(self.streak))
        self.correct_str.set('Correct: {}'.format(self.correct))
        self.incorrect_str.set('Incorrect: {}'.format(self.incorrect))
        self.total_str.set('Total: {}'.format(self.total))
        if self.total == 0.0:
            self.accuracy_str.set('Accuracy: 0.0%')
        else:
            self.accuracy_str.set('Accuracy: {}%'.format((float(self.correct) / float(self.total)) * 100.0))

    def collect(self):
        a = self.inp.get()
        possible = self.answer.split('/')
        if a in possible:
            self.streak += 1
            self.correct += 1
            self.last_answer.set('Last Answer: CORRECT')

            self.dictionary.pop(self.w)
            self.used[self.w] = self.answer
        else:
            self.streak = 0
            self.incorrect += 1
            self.last_answer.set('Last Answer: INCORRECT\n{}: {}'.format(self.w, self.answer))

        self.total += 1
        self.inp.delete(0, END)
        self.updateStats()
        self.setWord()

    def setWord(self):
        if len(self.dictionary.keys()) == 0:
            self.dictionary.update(self.used)
            self.used = {}

        self.w = random.choice(self.dictionary.keys())
        self.answer = self.dictionary[self.w]
        self.word.set(self.w)

    def run(self):
        self.updateStats()
        self.setWord()

        self.window.mainloop()
"""


class PracticeTXT:

    def __init__(self, dictionaries, reverse=False, all=False):
        self.streak = 0
        self.correct = 0
        self.incorrect = 0
        self.total = 0
        self.accuracy = 0.0
        self.dictionary = {}
        self.used = {}

        self.answer = ''
        self.w = ''

        # if all:
        #     self.dictionary = A.allwords
        # else:
        for d in dictionaries:
            self.dictionary.update(d)

        if reverse:
            self.dictionary = {v: k for k, v in self.dictionary.items()}

    def updateStats(self):
        print('\nStreak: {}'.format(self.streak))
        print('Correct: {}'.format(self.correct))
        print('Incorrect: {}'.format(self.incorrect))
        print('Total: {}'.format(self.total))
        print('Remaining: {}'.format(len(self.dictionary.keys())))
        if self.total == 0.0:
            print('Accuracy: 0.0%')
        else:
            print('Accuracy: {}%'.format((float(self.correct) / float(self.total)) * 100.0))

    def collect(self):
        a = input('{}: '.format(self.w))
        possible = self.answer.split('/')
        if a in possible:
            self.streak += 1
            self.correct += 1
            print('Last Answer: CORRECT\n{}: {}'.format(self.w, self.answer))
            utils.find_example_sentence(possible[1])

            self.dictionary.pop(self.w)
            self.used[self.w] = self.answer
        else:
            self.streak = 0
            self.incorrect += 1
            print('Last Answer: INCORRECT\n{}: {}'.format(self.w, self.answer))

        ex_sentence = utils.find_example_sentence(possible)
        print('')
        for s in ex_sentence:
            print(s)
            print('')

        self.total += 1

    def setWord(self):
        if len(self.dictionary.keys()) == 0:
            self.dictionary.update(self.used)
            self.used = {}

        self.w = random.choice(list(self.dictionary.keys()))
        self.answer = self.dictionary[self.w]

    def run(self):
        while True:
            self.updateStats()
            self.setWord()
            self.collect()
        

# vocabSets = [W.numbers, W.time, W.color]
# vocabSets = [W.pronouns, W.common, W.question_word, W.verbs, W.food_drink, W.numbers, W.animals, W.color, W.time,
#             W.size, W.shape, W.direction, W.anatomy, W.nature, W.transportation,
#             W.clothing, W.verbs, W.places, W.restaurant, W.money, W.house, W.technology, W.life, W.academic]
vocabSets = [W.hsk3_3]
practice = PracticeTXT(vocabSets, reverse=True, all=False)
practice.run()
