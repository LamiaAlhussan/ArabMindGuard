import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import os



# Load data from CSV file
def chart():
    df = pd.read_csv('stats.csv', encoding='utf-8')

    # Convert 'شهر' column to numeric
    df['شهر'] = pd.to_numeric(df['شهر'], errors='coerce')

    # Assuming 'تحليل' is the column you want to visualize and 'شهر' is the column with months
    analysis_data = df['تحليل']
    months = df['شهر']
    bar_color = '#ffde59'

    # Create bar chart with 'تحليل' on the y-axis and 'شهر' on the x-axis
    fig = go.Figure(data=[go.Bar(x=analysis_data, y=months,marker=dict(color=bar_color))])

    # Customize the layout
    fig.update_layout(
        xaxis_title='الشهور',
        yaxis_title='الاحصائيات',
        bargap=0.2,       # Adjust the gap between bars
        bargroupgap=0.1,   # Adjust the gap between bar groups
        plot_bgcolor='#fbfbfb',
        paper_bgcolor='#fbfbfb',
    )


    # Create the folder if it doesn't exist

    # Save the Plotly figure as an image in the specified folder
    pio.write_image(fig,'chart.png',engine='kaleido')

    # Plot!
