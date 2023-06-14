import streamlit as st
import plot_likert
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

st.set_page_config(layout="wide")

#### Plot code for likert 100% stacked bar chart taken from: https://www.kaggle.com/code/dradamjones/100-stacked-bar-chart-from-likert-scale-data and adapted


plt.style.use('ggplot')
plt.subplots(3, 1, height_ratios=[5, 5, 2], figsize=(5, 10), dpi=(300))
# plt.subplots_adjust(hspace=1)

def plot_likert_from_dict(plt, results, columns, plot_name, plot_index, ax1=None):

  data = pd.DataFrame.from_dict(results)
  data.columns = columns

  if ax1 is None:
    plt.subplot(3, 1, plot_index)
  else:
    plt.subplot(3, 1, plot_index, sharex=ax1)
  
  #read the data
  df = data[::-1] # flip order so in the later plot it will be top-bottom as in the data
  # df.columns

  #change the order so question with most agree is at the top
  #df = df.sort_values(by=['l_sa'])

  # df = df.sort_values(['Questoin'], ascending=False)

  #populate the variables from the csv
  questions = df["Question"]
  strongdisagree = df["Strongly disagree"]
  disagree = df["Disagree"]
  neutral = df["Neutral"]
  agree = df["Agree"]
  strongagree = df["Strongly agree"]

  ind = [x for x, _ in enumerate(questions)]

  #calculate the percentages for the 100% stacked bars
  total = strongdisagree+disagree+neutral+agree+strongagree
  proportion_strongdisagree = np.true_divide(strongdisagree, total) * 100
  proportion_disagree = np.true_divide(disagree, total) * 100
  proportion_neutral = np.true_divide(neutral, total) * 100
  proportion_agree = np.true_divide(agree, total) * 100
  proportion_strongagree = np.true_divide(strongagree, total) * 100

  plt.subplots_adjust(right=4, bottom=0.03)

  #plot the bars
  plt.barh(ind, proportion_strongagree, label='Strongly agree', color='#1b617b',  left=proportion_strongdisagree+proportion_disagree+proportion_neutral+proportion_agree)
  plt.barh(ind, proportion_agree, label='Agree', color='#879caf',   left=proportion_strongdisagree+proportion_disagree+proportion_neutral)
  plt.barh(ind, proportion_neutral, label='Neutral', color='#e7e7e7',   left=proportion_strongdisagree+proportion_disagree)
  plt.barh(ind, proportion_disagree, label='Disagree', color='#e28e8e',   left=proportion_strongdisagree)
  plt.barh(ind, proportion_strongdisagree, label='Strongly disagree', color='#c71d1d')

  #set the axes
  plt.yticks(ind, questions)
  #plt.ylabel("Questions")
  #plt.xlabel("Responses")
  #plt.title("Survey Responses")
  plt.xlim=1.0

  #fine tune the labels
  ax=plt.gca()
  if plot_index == 3:
    plt.setp(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())
  else:
    for tick in ax.xaxis.get_major_ticks():
        tick.tick1line.set_visible(False)
        tick.tick2line.set_visible(False)
        tick.label1.set_visible(False)
        tick.label2.set_visible(False)
  ax.grid(color='black', linestyle='-', axis="x", linewidth=1)
  ax.set_facecolor('white')
  plt.tick_params(labelsize=40)
  plt.xticks(fontsize=25)
  if plot_index == 1:
    ## flip order of legend and display at top
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(
        handles[::-1],
        labels[::-1],
        bbox_to_anchor=(0.5, 1.02),
        loc="lower center",
        borderaxespad=0,
        frameon=False,
        ncol=5,
        fontsize="25",
    )
  return ax
  # plt.savefig(f'{plot_name}.pdf', bbox_inches='tight')

  # st.pyplot(plt)

category_names = ['Strongly disagree', 'Disagree',
                  'Neutral', 'Agree', 'Strongly agree']
columns = ["Question","Strongly disagree","Disagree","Neutral","Agree","Strongly agree"]

results = [
# guided test amplification
    ['Q1 The Control Flow Graph of methods is easy to understand.', 0, 0, 1, 2, 9,],
    ['Q2 The Control Flow Graph of methods provides valuable information.', 0, 0, 0, 4, 8,],
    ['Q3 The interaction with the Control Flow Graph effectively assists you in conveying your expectations for the test cases.', 0, 0, 0, 10, 2,],
    ['Q4 The test generation results displayed with the Control Flow Graph are clear and easy to understand.', 0, 0, 0, 9, 3,],
    ['Q5 The the Control Flow Graph and branch/line coverage is helpful when you select test cases.', 0, 0, 2, 5, 5,],
]
ax1 = plot_likert_from_dict(plt, results, columns, "guided_test_amplification", 1)


results = [
# open test amplification
    ['Q6 The instruction coverage and corresponding code highlighting is easy to understand.', 1, 1, 2, 2, 6,],
    ['Q7 The test generation result displayed with additional instruction coverage is clear and easy to understand.', 0, 1, 4, 5, 2,],
    ['Q8 The test case information provides valuable information.', 1, 1, 2, 5, 3,],
    ['Q9 The modifications applied to test cases are helpful when you select test cases.', 0, 2, 2, 4, 4,],
    ['Q10 The instruction coverage and highlighting code are helpful when you select test cases.', 0, 0, 2, 5, 5,],
]

plot_likert_from_dict(plt, results, columns, 'plot', 2, ax1)

results = [
# general
    ['Q11 The amplified test cases provided by TestCube satisfy your expectations.', 0, 0, 0, 9, 3,],
    ['Q12 You would want to use TestCube to help you write tests in the future.', 0, 0, 1, 4, 7],
]

plot_likert_from_dict(plt, results, columns, 'plot', 3, ax1)

plt.savefig(f'questions.pdf', bbox_inches='tight', pad_inches=0.0)
st.pyplot(plt)


####### PLOT COMPARISON QUESTIONS #######


plt.style.use('ggplot')
plt.subplots(3, 1, height_ratios=[1, 1, 2], dpi=(300))
plt.subplots_adjust(hspace=1)

def plot_three_likert(plt, results, category_names, plot_name, plot_index, ax1):

  if ax1 is None:
    plt.subplot(3, 1, plot_index)
  else:
    plt.subplot(3, 1, plot_index, sharex=ax1)


  data = pd.DataFrame.from_dict(results)
  data.columns = ["Question"] + category_names

  #read the data
  df = data[::-1] # flip order so in the later plot it will be top-bottom as in the data
  # df.columns

  #change the order so question with most agree is at the top
  #df = df.sort_values(by=['l_sa'])

  # df = df.sort_values(['Questoin'], ascending=False)

  #populate the variables from the csv
  questions = df["Question"]
  c0 = df[category_names[0]]
  c1 = df[category_names[1]]
  c2 = df[category_names[2]]
  
  ind = [x for x, _ in enumerate(questions)]
  
  #calculate the percentages for the 100% stacked bars
  total = c0+c1+c2
  proportion_c0 = np.true_divide(c0, total) * 100
  proportion_c1 = np.true_divide(c1, total) * 100
  proportion_c2 = np.true_divide(c2, total) * 100
  
  plt.subplots_adjust(right=4, bottom=0.03)

  #plot the bars
  plt.barh(ind, proportion_c2, label=category_names[2], color='#0076C2', left=proportion_c0+proportion_c1)
  plt.barh(ind, proportion_c1, label=category_names[1], color='#FFB81C', left=proportion_c0)
  plt.barh(ind, proportion_c0, label=category_names[0], color='#EF60A3',)

  #set the axes
  plt.yticks(ind, questions)
  #plt.ylabel("Questions")
  #plt.xlabel("Responses")
  #plt.title("Survey Responses")
  plt.xlim=1.0

  #fine tune the labels
  ax=plt.gca()
  ax.grid(color='black', linestyle='-', axis="x", linewidth=1)
  if plot_index == 3:
    plt.setp(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())
  else:
    for tick in ax.xaxis.get_major_ticks():
        tick.tick1line.set_visible(False)
        tick.tick2line.set_visible(False)
        tick.label1.set_visible(False)
        tick.label2.set_visible(False)

  ax.set_facecolor('white')
  plt.tick_params(labelsize=40)
  plt.xticks(fontsize=25)
  ## flip order of legend and display at top
  handles, labels = ax.get_legend_handles_labels()
  ax.legend(
      handles[::-1],
      labels[::-1],
      bbox_to_anchor=(0.5, 1.02),
      loc="lower center",
      borderaxespad=0,
      frameon=False,
      ncol=5,
      fontsize="25",
  )
  return ax

category_names = ['Instruction Coverage', 'Neutral','Branch Coverage']
results = [
    ['Q13 Which type of coverage is easier to understand?', 0, 0, 12],
]
ax1 = plot_three_likert(plt, results, category_names, 'plot_coverage_type', 1, None)

category_names = ['Text', 'Neutral','Control Flow Graph']
results = [
  ['Q14 Which display form of coverage is easier to understand?', 2, 1, 9],
]

ax2 = plot_three_likert(plt, results, category_names, 'plot_coverage_representation', 2, ax1)

category_names = ['Open Test Amplification', 'Neutral','User-Guided Test Amplification']
results = [
    ['Q15 Which type of test amplification helps you select the amplified test cases more?', 1, 1, 10],
    ['Q16 Which type of test amplification is more helpful for you to generate test cases?', 2, 3, 7],
]

ax3 = plot_three_likert(plt, results, category_names, 'plot_technique_difference', 3, ax1)

plt.savefig(f'comparisons.pdf', bbox_inches='tight', pad_inches=0.0)
st.pyplot(plt)
