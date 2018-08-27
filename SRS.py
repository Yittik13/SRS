from datetime import date
from subprocess import call
from Words import *
import Utils as utils
import csv
import sys


class SRS:

    def __init__(self):
        self.streak = 0
        self.correct = 0
        self.incorrect = 0
        self.total = 0
        self.accuracy = 0.0

        self.char_file = 'srs_char.csv'
        self.main_file = 'srs.csv'
        self.out_file = 'srsout.csv'

    def update_csv_file(self, dictionary, fmode='a'):
        """
        Update the main csv file with new words
        Default category is 1
        Default file mode is append ('a')
        Only use file mode 'w' to overwrite entire file

        'pinyin/chinese/pinyin2/chinese2/...': 'english definition',
         0      1       2       3
        """
        f = open(self.main_file, fmode)
        writer = csv.writer(f)

        for k in dictionary:
            if '/' not in k:
                print('Missing \'/\'; Word:', k)
            else:
                split = k.split('/')
                chinese = ''
                pinyin = ''
                ptoggle = False
                ctoggle = False
                for c, s in enumerate(split):
                    # Pinyin is always even index
                    if c % 2 == 0:
                        if ptoggle:
                            pinyin += '/'
                        else:
                            ptoggle = not ptoggle
                        pinyin += s

                    # Chinese is odd index
                    else:
                        if ctoggle:
                            chinese += '/'
                        else:
                            ctoggle = not ctoggle
                        chinese += s

                english = dictionary[k]
                writer.writerow([chinese, pinyin, english, 1, date.today()])
        f.close()

    def review_cards(self, num_cards=30, shuffle=False):
        """
        Iterate though file to review cards based on category and last review date
        Categories
        1 - Little memory - Review again
        2 - Fair memory - Review in 1 day
        3 - Good memory - Review in 2 days
        4 - Excellent memory - Review in 5 days
        5 - Perfect memory - Review in 10 days

        CSV File format
           0        1       2        3              4
        Chinese, Pinyin, English, Category, Date Last Reviewed
        """
        print('\nStarting review session with {} cards'.format(num_cards))
        if shuffle:
            utils.shuffle_file(self.main_file)
        in_f = open(self.main_file, 'r')
        out_f = open(self.out_file, 'w')
        reader = csv.reader(in_f)
        writer = csv.writer(out_f)
        today = date.today()

        for row in reader:
            chinese = row[0]
            pinyin = row[1]
            english = row[2]
            category = int(row[3])
            rdate = utils.extract_date(row[4])

            # This card should be reviewed
            if self.total < num_cards and self.show(category, today, rdate):
                self.print_stats()
                try_again = True
                first_try = True
                while try_again:
                    str = english
                    a = input('{}: '.format(str))
                    possible = chinese.split('/')
                    if a in possible:
                        print('Last Answer: CORRECT\n{}: {}'.format(english, (chinese + '/' + pinyin)))
                        ex_sentence = utils.find_example_sentence(possible)
                        print('')
                        for s in ex_sentence:
                            print(s)
                            print('')
                        self.correct += 1
                        self.streak += 1
                        if category < 5:
                            category += 1
                        writer.writerow([chinese, pinyin, english, category, today])
                        try_again = False

                    else:
                        if first_try:
                            first_try = False
                            print('First Try, Last Answer: INCORRECT')
                        else:
                            print('Last Answer: INCORRECT\n{}: {}'.format(english, (chinese + '/' + pinyin)))
                            ex_sentence = utils.find_example_sentence(possible)
                            print('')
                            for s in ex_sentence:
                                print(s)
                                print('')
                            self.streak = 0
                            self.incorrect += 1
                            category = 1
                            writer.writerow([chinese, pinyin, english, category, today])
                            try_again = False
                self.total += 1


            # This card does not need to be reviewed yet
            else:
                writer.writerow(row)
        in_f.close()
        out_f.close()


    def review_characters(self, num_cards=10, shuffle=False):
        """
        Iterate though file to review cards based on category and last review date
        Categories
        1 - Little memory - Review again
        2 - Fair memory - Review in 1 day
        3 - Good memory - Review in 2 days
        4 - Excellent memory - Review in 5 days
        5 - Perfect memory - Review in 10 days

        CSV File format
           0        1       2        3              4
        Chinese, Pinyin, English, Category, Date Last Reviewed
        """
        print('\nStarting review session with {} cards'.format(num_cards))
        if shuffle:
            utils.shuffle_file(self.char_file)
        in_f = open(self.char_file, 'r')
        out_f = open(self.out_file, 'w')
        reader = csv.reader(in_f)
        writer = csv.writer(out_f)
        today = date.today()

        for row in reader:
            chinese = row[0]
            pinyin = row[1]
            english = row[2]
            category = int(row[3])
            rdate = utils.extract_date(row[4])

            # This card should be reviewed
            if self.total < num_cards and self.show(category, today, rdate):
                self.print_stats()
                try_again = True
                first_try = True
                while try_again:
                    a = input('{}: '.format(chinese))
                    possible = chinese.split('/')
                    if a in possible:
                        print('Last Answer: CORRECT\n{}: {}'.format((chinese + '/' + pinyin), english))
                        ex_sentence = utils.find_example_sentence(possible)
                        print('')
                        for s in ex_sentence:
                            print(s)
                            print('')
                        # if ex_sentence:
                        #     print(ex_sentence)
                        self.correct += 1
                        self.streak += 1
                        if category < 5:
                            category += 1
                        writer.writerow([chinese, pinyin, english, category, today])
                        try_again = False

                    else:
                        if first_try:
                            first_try = False
                            print('First Try, Last Answer: INCORRECT')
                        else:
                            print('Last Answer: INCORRECT\n{}: {}'.format((chinese + '/' + pinyin), english))
                            ex_sentence = utils.find_example_sentence(possible)
                            print('')
                            for s in ex_sentence:
                                print(s)
                                print('')
                            # if ex_sentence:
                            #     print(ex_sentence)
                            self.streak = 0
                            self.incorrect += 1
                            category = 1
                            writer.writerow([chinese, pinyin, english, category, today])
                            try_again = False
                self.total += 1


            # This card does not need to be reviewed yet
            else:
                writer.writerow(row)
        in_f.close()
        out_f.close()

    def show(self, category, today, last_review):
        delta = utils.days_apart(last_review, today)
        if category < 1 or category > 5:
            print('BAD CATEGORY')
            return False
        if category == 1:
            return True
        if category == 2 and delta >= 2:
            return True
        if category == 3 and delta >= 4:
            return True
        if category == 4 and delta >= 8:
            return True
        if category == 5 and delta >= 16:
            return True
        return False

    def print_stats(self):
        print('\nStreak: {}'.format(self.streak))
        print('Correct: {}'.format(self.correct))
        print('Incorrect: {}'.format(self.incorrect))
        print('Total: {}'.format(self.total))
        if self.total == 0.0:
            print('Accuracy: 0.0%')
        else:
            print('Accuracy: {}%'.format((float(self.correct) / float(self.total)) * 100.0))

    def cleanup(self, f):
        # Make sure files are same length to avoid data loss
        if utils.compare_file_length(f, self.out_file):
            # Update original file to new file
            call(['rm', f])
            call(['mv', self.out_file, f])
        else:
            print('Files are different length')

    def deck_stats_words(self):
        """
        Show deck stats
        """
        total_cards = 0
        cat_count = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        total_need_review = 0

        today = date.today()
        f = open(self.main_file, 'r')
        reader = csv.reader(f)

        for row in reader:
            category = int(row[3])
            rdate = utils.extract_date(row[4])

            total_cards += 1
            if self.show(category, today, rdate):
                total_need_review += 1
            cat_count[category] += 1

        print('\n---------- Word Deck Statistics ----------')
        print('Total Cards: {:4d}'.format(total_cards))
        print('To Review:   {:4d}, {:0.2f}%'.format(total_need_review, (float(total_need_review) / total_cards) * 100.0))
        print('Category 1:  {:4d}, {:0.2f}%'.format(cat_count[1], (float(cat_count[1]) / total_cards) * 100.0))
        print('Category 2:  {:4d}, {:0.2f}%'.format(cat_count[2], (float(cat_count[2]) / total_cards) * 100.0))
        print('Category 3:  {:4d}, {:0.2f}%'.format(cat_count[3], (float(cat_count[3]) / total_cards) * 100.0))
        print('Category 4:  {:4d}, {:0.2f}%'.format(cat_count[4], (float(cat_count[4]) / total_cards) * 100.0))
        print('Category 5:  {:4d}, {:0.2f}%'.format(cat_count[5], (float(cat_count[5]) / total_cards) * 100.0))
        print('------------------------------------------')

    def deck_stats_chars(self):
        """
        Show deck stats
        """
        total_cards = 0
        cat_count = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        total_need_review = 0

        today = date.today()
        f = open(self.char_file, 'r')
        reader = csv.reader(f)

        for row in reader:
            category = int(row[3])
            rdate = utils.extract_date(row[4])

            total_cards += 1
            if self.show(category, today, rdate):
                total_need_review += 1
            cat_count[category] += 1

        print('\n------- Character Deck Statistics --------')
        print('Total Cards: {:4d}'.format(total_cards))
        print('To Review:   {:4d}, {:0.2f}%'.format(total_need_review, (float(total_need_review) / total_cards) * 100.0))
        print('Category 1:  {:4d}, {:0.2f}%'.format(cat_count[1], (float(cat_count[1]) / total_cards) * 100.0))
        print('Category 2:  {:4d}, {:0.2f}%'.format(cat_count[2], (float(cat_count[2]) / total_cards) * 100.0))
        print('Category 3:  {:4d}, {:0.2f}%'.format(cat_count[3], (float(cat_count[3]) / total_cards) * 100.0))
        print('Category 4:  {:4d}, {:0.2f}%'.format(cat_count[4], (float(cat_count[4]) / total_cards) * 100.0))
        print('Category 5:  {:4d}, {:0.2f}%'.format(cat_count[5], (float(cat_count[5]) / total_cards) * 100.0))
        print('------------------------------------------')



if __name__ == '__main__':

    arg_STATS = '-s'
    arg_REVIEW_WORDS = '-rw'
    arg_REVIEW_CHARS = '-rc'
    arg_HELP = '-h'
    arg_APPEND = '-a'
    args = [arg_STATS, arg_REVIEW_WORDS, arg_REVIEW_CHARS, arg_HELP, arg_APPEND]
    if len(sys.argv) < 2 or sys.argv[1] not in args or sys.argv[1] == arg_HELP:
        print('Usage: python SYS.py OPTION')
        print('OPTIONS:')
        print('-s            \tShow deck statistics')
        print('-rw [num cards]\tStart review session (words) with (optional) number of cards. Default 30 cards')
        print('-rc [num cards]\tStart review session (chars) with (optional) number of cards. Default 30 cards')
        print('-h            \tShow usage')
        print('-a            \tAppend new words to srs file')
    elif sys.argv[1] == arg_REVIEW_WORDS:
        srs = SRS()
        if len(sys.argv) == 3:
            try:
                num = int(sys.argv[2])
                srs.review_cards(num, shuffle=True)
            except ValueError:
                print('Non numeric argument')
        else:
            srs.review_cards(shuffle=True)
        srs.cleanup(srs.main_file)
        srs.deck_stats_words()
    elif sys.argv[1] == arg_REVIEW_CHARS:
        srs = SRS()
        if len(sys.argv) == 3:
            try:
                num = int(sys.argv[2])
                srs.review_characters(num)
            except ValueError:
                print('Non numeric argument')
        else:
            srs.review_characters()
        srs.cleanup(srs.char_file)
        srs.deck_stats_chars()
    elif sys.argv[1] == arg_STATS:
        srs = SRS()
        srs.deck_stats_words()
        srs.deck_stats_chars()
    elif sys.argv[1] == arg_APPEND:
        ri = input('Update SRS file? (y/n): ')
        if ri.lower().startswith('y'):
            srs = SRS()
            srs.update_csv_file()
        else:
            sys.exit(0)


    # vocab_sets = [adverbs, common, question, question_word, numbers, time, math, people, food_drink,
    #               sound, color, shape, size, direction, anatomy, clothing, nature, transportation, household_items,
    #               animals, family, academic, house, technology, money, adjectives, verbs, restaurant, places,
    #               new2, new3, new4, new5, new6, new7]
    #
    # d = utils.combine(vocab_sets)
    # srs.update_csv_file(d, fmode='w')
