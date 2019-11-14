import matplotlib.pyplot as plt
%matplotlib inline
import seaborn as sns
sns.set()
sns.set_style('ticks')
# plt.style.use('ggplot')
sns.set(font_scale=1.5)


def sns_count_plot(df_name, col, style):
  '''
  Counts unique values in a given column and plot
  df_name: the dataframe
  col: column name in the df
  style: 'ticks', 'whitegrid'
  '''
  sns.set_palette(['#f6d908', '#cd34b5'])
  sns.set_style(style)
  ax = sns.countplot(x=col, data=df_name)
  _, labels = plt.xticks()
  ax.set_xticklabels(labels, rotation=90)
  ax.set(xlabel=col, ylabel='Count')

def plot_crosstab(df_name, col_a, col_b, num_rows):
    '''
    Plots the cross-tab values between two columns
    num_rows: number of rows to plot

    '''
  df = pd.crosstab(df[col_a], df[col_b], margins=True)
  df.drop('All', axis=0, inplace=True)
  df = df.sort_values(by="All", ascending=False).head(num_rows)
  df.drop('All', axis=1, inplace=True)
  df.plot.bar(stacked=True, figsize=(12, 8), color=sns.color_palette("Paired"))
