from collections import Counter

def count_feature(df, col, new_col):
  '''Count occurences of features in a df column and sort from high to low
  col: column name to countplot
  new_col: Column name for the new Counts column
  '''
  new_df = pd.DataFrame.from_dict(Counter(df[col]), orient='index',
                                  columns=[new_col]).
                                  sort_values(new_col,
                                  ascending=False).reset_index()
  return new_df
