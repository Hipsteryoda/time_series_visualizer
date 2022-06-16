import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from pexpect import split_command_line
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date')

# Clean data
upper = df.quantile(.975)
lower = df.quantile(.025)
df = df[df.value < upper[0]]
df = df[df.value > lower[0]]

def draw_line_plot():

    # Draw line plot
    fig = plt.figure(facecolor='white')
    # fig, ax = plt.subplots(1, 1, figsize=(15, 10), sharey=True)
    ax0 = fig.add_axes(sns.lineplot(data = df, x=pd.to_datetime(df.index), y= 'value', color='red'))
    ax0.set_xlabel('Date')
    ax0.set_ylabel('Page Views')
    ax0.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    fig.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png', bbox_inches='tight')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()

    # Create a datetime column from the index to be used to split apart
    df_bar['date'] = pd.to_datetime(df.index)

    # Create 4 columns for year, month, day, and month_name 
    df_bar['year'] = df_bar['date'].dt.year
    df_bar['month'] = df_bar['date'].dt.month
    df_bar['day'] = df_bar['date'].dt.day
    df_bar['month_name'] = df_bar['date'].dt.month_name()
    
    # # Drop the no longer needed (and duplicate to index) column 'date'
    df_bar.drop('date', axis=1, inplace=True)

    # sort values by year, then month in year
    df_bar.sort_values(by=['year', 'month'], ascending=[False, True], inplace=True)

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(15,10))
    ax = sns.barplot(data=df_bar, y='value', x='year', hue='month_name', palette='tab10', ci=None)
    ax.legend(title='Months', loc='upper left')
    ax.set_ylabel('Average Page Views')
    ax.set_xlabel('Years')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig
    
def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box['date'] = pd.to_datetime(df.index)
    # df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(1, 2, figsize=(20,10), tight_layout=True, facecolor='white')
    ax1 = sns.boxplot(x=df_box.year, y=df_box.value, ax=ax[0])
    ax2 = sns.boxplot(x=df_box.month, y=df_box.value, ax=ax[1], order=month_order)

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')
    ax1.set_title('Year-wise Box Plot (Trend)')

    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')
    ax2.set_title('Month-wise Box Plot (Seasonality)')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
