# Import necessary libraries
from wordcloud import WordCloud  # For generating word clouds
import arabic_reshaper  # For reshaping Arabic text
from bidi.algorithm import get_display  # For handling bidi text (Arabic)
import matplotlib.pyplot as plt  # For plotting word clouds
import pandas as pd  # For data manipulation
import plotly.graph_objects as go  # For creating interactive visualizations
import plotly.io as pio  # For saving Plotly figures as images
import os  # For file and directory operations
import Preprocessing  # Assuming Preprocessing module contains custom preprocessing functions


# Function to create a word cloud from a list of terms
def CreateWordCloud(depressed_Terms, ImageName):
    # Join the list of terms into a single string
    depressed_wordcloud_text = " ".join(depressed_Terms)
    
    # Preprocess the text
    depressed_wordcloud_text = Preprocessing.remove_repeated_words(depressed_wordcloud_text)
    depressed_wordcloud_text = Preprocessing.remove_stopwords(depressed_wordcloud_text)
    
    # Reshape and handle bidi text (for Arabic)
    reshaped_text = arabic_reshaper.reshape(depressed_wordcloud_text)
    bidi_text = get_display(reshaped_text)
    
    # Generate Word Cloud
    if not depressed_wordcloud_text:
        print("No depressed tweets found")
    else:
        wordcloud_depressed = WordCloud(
            width=800, height=400, background_color='#fbfbfb',
            font_path='../Fonts/NotoNaskhArabic-Medium.ttf',  # Path to Arabic font
            max_words=50,  # Maximum number of words in the cloud
            collocations=False  # Disable collocations
        ).generate(bidi_text)

        # Plot the Word Cloud
        plt.figure(figsize=(10, 5), facecolor='#fbfbfb')
        plt.imshow(wordcloud_depressed, interpolation='bilinear')
        plt.axis('off')
        
        # Save the Word Cloud as an image
        imagePath = "../Images/" + ImageName + ".png"
        print(imagePath)
        plt.savefig(imagePath)  # Save the plot as an image
        plt.show()  # Display the plot


# Function to create a bar chart from CSV data
def chart():
    # Read data from CSV file
    df = pd.read_csv('../Datasets/stats.csv', encoding='utf-8')

    # Convert 'شهر' column to numeric
    df['شهر'] = pd.to_numeric(df['شهر'], errors='coerce')

    # Extract data for visualization
    analysis_data = df['تحليل']  # Data for analysis
    months = df['شهر']  # Months for x-axis
    bar_color = '#ffde59'  # Color for bars

    # Create bar chart using Plotly
    fig = go.Figure(data=[go.Bar(x=analysis_data, y=months, marker=dict(color=bar_color))])

    # Customize the layout
    fig.update_layout(
        xaxis_title='الشهور',  # X-axis title
        yaxis_title='الاحصائيات',  # Y-axis title
        bargap=0.3,  # Gap between bars
        bargroupgap=0.1,  # Gap between groups of bars
        plot_bgcolor='#fbfbfb',  # Plot background color
        paper_bgcolor='#fbfbfb',  # Paper background color
        font=dict(
            family="Arial, sans-serif",  # Font family
            size=30,  # Font size for axis labels
            color="black",  # Font color
        ),
        xaxis=dict(
            tickfont=dict(
                size=25  # Font size for x-axis tick labels
            ),
            tickangle=45,  # Rotate tick labels for better visibility
            showgrid=False,  # Hide gridlines
            zeroline=False,  # Hide zero line
        ),
        yaxis=dict(
            tickfont=dict(
                size=25  # Font size for y-axis tick labels
            )
        ),
        margin=dict(b=100)  # Bottom margin
    )

    # Save the Plotly figure as an image
    images_folder = '../Images'
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    # Full path to save the image
    image_path = os.path.join(images_folder, 'chart.png')
    pio.write_image(fig, image_path, engine='kaleido')

