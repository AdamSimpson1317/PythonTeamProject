import csv
# from . import plot
import matplotlib.pyplot as plt
import numpy as np

text_file = "book.txt"


def main():
    # Open specified file, read it, pass it to relevant functions for frequency analysis, output analysis.
    opened_file = open(text_file, 'r')
    read_file = opened_file.read().lower()
    word_list = read_file.split()

    word_dictionary = freq_analysis_words(word_list)
    ordered_word_dictionary = sort_word_freq_dict(word_dictionary)

    char_dictionary = freq_analysis_chars(read_file)
    ordered_char_dictionary = sort_char_freq_dict(char_dictionary)

    output_to_csv(ordered_word_dictionary, ordered_char_dictionary)

    for x in ordered_word_dictionary:
        print(str(x))

    for x in ordered_char_dictionary:
        print(str(x))


def freq_analysis_words(word_list):
    # Frequency analysis operation of words on passed parsed file.
    word_freq = [word_list.count(x) for x in word_list]
    plot_freq_analysis_words(word_freq, word_list)
    return dict(list(zip(word_list, word_freq)))


def sort_word_freq_dict(word_dictionary):
    # Sort the word dictionary into descending order.
    order = [(word_dictionary[key],key) for key in word_dictionary]
    order.sort()
    order.reverse()
    return order


def freq_analysis_chars(read_file):
    # Frequency analysis operation of characters on passed parsed file.
    char_freq = [read_file.count(x) for x in read_file]
    plot_freq_analysis_chars(char_freq, read_file)
    return dict(list(zip(read_file, char_freq)))


def sort_char_freq_dict(char_dictionary):
    # Sort the character dictionary into descending order.
    order = [(char_dictionary[key], key) for key in char_dictionary]
    order.sort()
    order.reverse()
    return order


def output_to_csv(ordered_word_dictionary, char_dictionary):
    # Write ordered word and character dictionaries into csv file.
    with open("freq_analysis.csv", "w+") as csv_freq_analysis:
        writer = csv.writer(csv_freq_analysis)
        writer.writerow(ordered_word_dictionary)
        writer.writerow(char_dictionary)


def plot_freq_analysis_words(word_freq, word_list):
    # Take word dictionary as parameter, plot it on bar chart.
    x = np.arange(len(word_list))
    fig, ax = plt.subplots()

    ax.bar(x, word_freq, width=0.60)
    ax.set_ylabel('Frequency')
    ax.set_title('Word frequency analysis')
    ax.set_xticks(x)
    ax.set_xticklabels(word_list, rotation='vertical')

    fig.tight_layout()
    plt.show()


def plot_freq_analysis_chars(char_freq, read_list):
    # Take character dictionary as parameter, plot it on a bar chart.
    x = np.arange(len(read_list))
    fig, ax = plt.subplots()

    ax.bar(x, char_freq, width=0.35)
    ax.set_ylabel('Frequency')
    ax.set_title('Character frequency analysis')
    ax.set_xticks(x)
    ax.set_xticklabels(read_list, rotation='vertical')

    fig.tight_layout()
    plt.show()


main()
