import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import warnings; warnings.filterwarnings(action='once')

large = 22; med = 16; small = 12
params = {'axes.titlesize': large,
          'legend.fontsize': med,
          'figure.figsize': (16, 10),
          'axes.labelsize': med,
          'axes.titlesize': med,
          'xtick.labelsize': med,
          'ytick.labelsize': med,
          'figure.titlesize': large}
plt.rcParams.update(params)
plt.style.use('seaborn-whitegrid')
sns.set_style("white")

# Version
print(mpl.__version__)  #> 3.0.0
print(sns.__version__)  #> 0.9.0

def marginal_histogram(df, col_1, col_2, label_x, label_y, title_main, dot_color):
  '''
  Plots a scatterplot with marginal histogram
  col_1: x value
  col_2: y value
  dot_color:color in hash
  '''

  # Create Fig and gridspec
  fig = plt.figure(figsize=(16, 10), dpi= 80)
  grid = plt.GridSpec(4, 4, hspace=0.5, wspace=0.2)

  # Define the axes
  ax_main = fig.add_subplot(grid[:-1, :-1])
  ax_right = fig.add_subplot(grid[:-1, -1], xticklabels=[], yticklabels=[])
  ax_bottom = fig.add_subplot(grid[-1, 0:-1], xticklabels=[], yticklabels=[])

  # Scatterplot on main ax
  ax_main.scatter(col_1, col_2, alpha=.9, data=df, s = 100,c=dot_color, edgecolors='white', linewidths=.5)

  # histogram on the right
  ax_bottom.hist(df[col_1], 40, histtype='stepfilled', orientation='vertical', color='deeppink')
  ax_bottom.invert_yaxis()

  # histogram in the bottom
  ax_right.hist(df[col_2], 40, histtype='stepfilled', orientation='horizontal', color='deeppink')

  # Decorations
  ax_main.set(title=title_main, xlabel=label_x, ylabel=label_y)
  ax_main.title.set_fontsize(20)
  for item in ([ax_main.xaxis.label, ax_main.yaxis.label] + ax_main.get_xticklabels() + ax_main.get_yticklabels()):
      item.set_fontsize(14)

  xlabels = ax_main.get_xticks()
  ax_main.set_xticklabels(df['CHROM'].unique())
  sns.set_style("ticks")
  plt.show()
