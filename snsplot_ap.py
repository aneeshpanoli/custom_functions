import matplotlib.pyplot as plt
%matplotlib inline
import seaborn as sns
import pandas a pd
sns.set()



def sns_count_plot(df_name, col, style, labelx, labely, orientation):
  '''
  Counts unique values in a given column and plot
  df_name: the dataframe
  col: column name in the df
  style: 'ticks', 'whitegrid'
  fig_size: (1, 1)
  orientation: 'h or 'v;
  '''
  sns.set_palette(['#f6d908', '#cd34b5'])
  sns.set(font_scale=1.3)
  sns.set_style(style)
  ax = sns.countplot(x=col, data=df_name, orient=orientation)
  _, labels = plt.xticks()
  ax.set_xticklabels(labels, rotation=90)
  ax.set(xlabel=labelx, ylabel=labely)
  sns.set(rc={'figure.figsize':(16, 10)})

def plot_crosstab(df_name, col_a, col_b, num_rows, style, bar_kind='bar'):
  '''
  style: sns style 'ticks' or whitegrid
  num_rows: pandas hdead(hum_rows) to plot
  col_a and col_b: are crosstabs x and y respectively
  does pandas crosstab and then plots a stacked horizontal or vertical histogram
  bar_kind: barh for horizontal, default is vertical
  '''
  sns.set(font_scale=1.3)
  df_name = pd.crosstab(df_name[col_a], df_name[col_b], margins=True)
  df_name.drop('All', axis=0, inplace=True)
  df_name = df_name.sort_values(by="All", ascending=False).head(num_rows)
  df_name.drop('All', axis=1, inplace=True)
  sns.set_style(style)
  ax = df_name.plot(kind=bar_kind , stacked=True, figsize=(16, 10), color=sns.color_palette("Paired", 20 ))
  ax.set(ylabel="", xlabel="Number of variants")

def sns_violin(df_name, x_col, y_col, x_label, y_label):
  '''
  plots a violin plot
  '''
  sns.set_palette("bright")
  sns.set(font_scale=1.5)
  sns.set_style("whitegrid")
  ax = sns.violinplot(data=df_name, x =x_col, y=y_col)
  _, labels = plt.xticks()
  ax.set_xticklabels(labels, rotation=90)
  ax.set(xlabel=x_label, ylabel=y_label)
  # plt.figure(figsize=(16, 10), dpi=80)
  sns.set(rc={'figure.figsize':(16, 10)})
