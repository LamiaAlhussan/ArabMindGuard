import tweepy
import configparser
import csv


def fetch_and_save_tweets(username, userFile):
    # read cofing
    user_Found = False
    tweetlength = True
    api_key = "9Kmm50JN2cJld3BHJswQfKXwe"
    api_key_secret = "hcyo5IQp542gSUcWebPCLJjgJQdKgUYpRGboGQ2PK0WjAvPQGH"

    access_token = "537587465-W8l66TWKsaABEJ3OZbaZrbuT7VVmiSjMVajOVUAX"
    access_token_secret = "Iw9cibATU63XPCwAko3fRQyckasjAbawUMg4Yh4YlGLri"

    bearer_token = "AAAAAAAAAAAAAAAAAAAAAO%2BGrQEAAAAAj8viy8t%2Fc7fdHaS%2Bk30GItmQyvA%3DUZHtddyXZIWNGcPEr8yBwcqH06VvvdFmdfVayQNZ7ugqHHdii1"

    # auth
    client = tweepy.Client(
        bearer_token,
        api_key,
        api_key_secret,
        access_token,
        access_token_secret,
        wait_on_rate_limit=True,
    )

    user = None
    try:
        user = client.get_user(username=username)
        if user is not None and user.data is not None:
            user_Found = True

    except Exception as e:
        user_Found = False

    if user_Found and user.data:
        user_id = user.data.id

        # Extract tweets
        tweets = client.get_users_tweets(
            user_id,
            tweet_fields=["context_annotations", "created_at", "geo"],
            max_results=100,
            exclude=["replies", "retweets"],
        )

        if tweets is None or tweets.data is None:
            tweetlength = False

        else:
            if len(tweets.data) < 100:
                tweetlength = False
            # Specify the CSV file name
            else:

                userFile = "../Datasets/" + userFile

                with open(userFile, "a", newline="", encoding="utf-8") as csvfile:
                    # Create a CSV writer object
                    csv_writer = csv.writer(csvfile)

                    # Write each tweet to the CSV file
                    csv_writer.writerow(["Tweets"])
                    for tweet in tweets.data:
                        # Write the cleaned data to the CSV file
                        text = tweet.text.replace("\n", " ")
                        csv_writer.writerow([text])
                # Close the CSV file
                print(f"Tweets from {username} saved to {userFile}")
    return user_Found, tweetlength
