import matplotlib.pyplot as plt
import numpy as np


def plot_freq_analysis_words(ordered_word_dictionary):
    # Take word dictionary as parameter, plot it on pie chart
    x = np.arange(len(ordered_word_dictionary))
    width = 0.35
    fig, ax = plt.subplots()

    ax.set_ylabel('Frequency')
    ax.set_title('Word frequency analysis')
    ax.set_xticks(x)
    ax.set_xticklabels(ordered_word_dictionary)

    fig.tight_layout()
    plt.show()


def plot_freq_analysis_chars(ordered_char_dictionary):
    # Take character dictionary as parameter, plot it on a pie chart.
    x = np.arange(len(ordered_char_dictionary))
    width = 0.35
    fig, ax = plt.subplots()

    ax.set_ylabel('Frequency')
    ax.set_title('Character frequency analysis')
    ax.set_xticks(x)
    ax.set_xticklabels(ordered_char_dictionary)

    fig.tight_layout()
    plt.show()
