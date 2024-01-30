import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import os

# Load data from CSV file
def chart():
    df = pd.read_csv('../Datasets/stats.csv', encoding='utf-8')

    # Convert 'شهر' column to numeric
    df['شهر'] = pd.to_numeric(df['شهر'], errors='coerce')

    # Assuming 'تحليل' is the column you want to visualize and 'شهر' is the column with months
    analysis_data = df['تحليل']
    months = df['شهر']
    bar_color = '#ffde59'

    # Create bar chart with 'تحليل' on the y-axis and 'شهر' on the x-axis
    fig = go.Figure(data=[go.Bar(x=analysis_data, y=months, marker=dict(color=bar_color))])

    # Customize the layout with increased font sizes
    fig.update_layout(
        xaxis_title='الشهور',
        yaxis_title='الاحصائيات',
        bargap=0.3,       # Adjust the gap between bars
        bargroupgap=0.1,   # Adjust the gap between bar groups
        plot_bgcolor='#fbfbfb',
        paper_bgcolor='#fbfbfb',
        font=dict(
            family="Arial, sans-serif",  # Set font family
            size=30,  # Set font size for axis labels
            color="black",  # Set font color
        ),
        xaxis=dict(
            tickfont=dict(
                size=25  # Set font size for x-axis tick labels
            ),
            tickangle=45,  # Rotate tick labels for better visibility
            showgrid=False,  # Hide gridlines for better aesthetics
            zeroline=False,  # Hide zero line for better aesthetics
            
        ),
        yaxis=dict(
            tickfont=dict(
                size=25  # Set font size for y-axis tick labels
            )
        ),
        margin=dict(b=100) 

    )
    

    # Save the Plotly figure as an image in the specified folder
    images_folder = '../Images'
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    # Full path to save the image in the Images folder
    image_path = os.path.join(images_folder, 'chart.png')
    pio.write_image(fig, image_path, engine='kaleido')

    # Plot!
chart()
