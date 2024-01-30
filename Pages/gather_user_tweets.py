import tweepy
import configparser
import csv


# read cofing
def fetch_and_save_tweets (username, userFile):
    user_Found = True
    tweetlength = True
    api_key = '9Kmm50JN2cJld3BHJswQfKXwe'
    api_key_secret = 'hcyo5IQp542gSUcWebPCLJjgJQdKgUYpRGboGQ2PK0WjAvPQGH'

    access_token = '537587465-W8l66TWKsaABEJ3OZbaZrbuT7VVmiSjMVajOVUAX'
    access_token_secret = 'Iw9cibATU63XPCwAko3fRQyckasjAbawUMg4Yh4YlGLri'

    bearer_token = 'AAAAAAAAAAAAAAAAAAAAAO%2BGrQEAAAAAj8viy8t%2Fc7fdHaS%2Bk30GItmQyvA%3DUZHtddyXZIWNGcPEr8yBwcqH06VvvdFmdfVayQNZ7ugqHHdii1'

    # auth
    client = tweepy.Client(
        bearer_token,
        api_key,
        api_key_secret,
        access_token,
        access_token_secret,
        wait_on_rate_limit=True,
    )

    # Specify the username of the desired user
    user = None
    try:
        user = client.get_user(username=username)
    # Rest of your code here if the function call is successful
    except Exception as e:
        user_Found = False
    # Handle the error or perform necessary actions here


    if user is None:
        user_Found = False
    else:
        user_id = user.data.id
            # Construct the query with the user's tweets
            # query = f'from:{username} lang:ar -is:retweet -is:reply'

            # Extract tweets
        tweets = client.get_users_tweets(
                user_id,
                tweet_fields=['context_annotations', 'created_at', 'geo'],
                max_results=10, exclude=['replies', 'retweets'])
        print('tweet length:',len(tweets.data))
        if len(tweets.data)<10:
            tweetlength =False
        # Specify the CSV file name
        else:
            print(tweets)
            print('-------------------')
            csv_file_name = "../Datasets/tweets_from_user.csv"

            # Open the CSV file in write mode
            with open(csv_file_name, "a", newline="", encoding="utf-8") as csvfile:
                # Create a CSV writer object
                csv_writer = csv.writer(csvfile)

                # Write each tweet to the CSV file
                for tweet in tweets.data:
                    # Write the cleaned data to the CSV file
                    text = tweet.text.replace('\n', ' ')
                    csv_writer.writerow([text])
                
            userFile = '../Datasets/'+userFile
                    
            with open(userFile, "a", newline="", encoding="utf-8") as csvfile:
                # Create a CSV writer object
                csv_writer = csv.writer(csvfile)

                # Write each tweet to the CSV file
                csv_writer.writerow(['Tweets'])
                for tweet in tweets.data:
                    # Write the cleaned data to the CSV file
                    text = tweet.text.replace('\n', ' ')
                    csv_writer.writerow([text])
            # Close the CSV file
            print(f"Tweets from {username} saved to {userFile}")
    return user_Found,tweetlength
