import re
from pytube import YouTube
import requests
import flet as f
import tweepy
from tweepy import OAuthHandler

# Twitter API
consumer_key = 'Put your Consumer Key'
consumer_secret = 'Put your Consumer Secret'
access_token = 'Put your Access Token'
access_secret = 'Put your Access Secret'
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)


def main(page: f.Page):
    def download_yt(e):
        if yt_input.value == "" or yt_input.value == "Enter the link":
            wating_text.value = "Please enter the link"
            page.update()
        else:
            if not re.match(r"https?:\/\/(www\.)?youtube\.com\/watch\?v=[A-Za-z0-9_-]+", str(yt_input.value)):
                wating_text.value = "Error: link isn't from youtube"
                page.update()
            else:
                wating_text.value = "Please wait..."
                page.update()
                try:
                    link = str(yt_input.value)
                    check = requests.get(link)
                    if check.status_code == 200:
                        yt = YouTube(link)
                        stream = yt.streams.get_highest_resolution()
                        stream.download()
                        wating_text.value = "Download completed!!"
                        page.update()
                    else:
                        wating_text.value = "Error in the link"
                        page.update()
                except Exception as e:
                    wating_text.value = f"Error: {e}"
                    page.update()

    def download_tw(e):
        if tw_input.value == "" or tw_input.value == "Enter the link":
            wating_text.value = "Please enter the link"
            page.update()
        else:
            if not re.match(r"https?:\/\/(www\.)?twitter\.com\/[A-Za-z0-9_-]+\/status\/[A-Za-z0-9_-]+", str(tw_input.value)):
                wating_text.value = "Error: link isn't from twitter"
                page.update()
            else:
                wating_text.value = "Please wait..."
                page.update()
                try:
                    link = str(tw_input.value)
                    tweet_id = link.split('status/')[1]
                    tweet = api.get_status(tweet_id, tweet_mode='extended')
                    if 'extended_entities' in tweet._json:
                        media_array = tweet._json['extended_entities']['media']
                        for i in range(len(media_array[0]['video_info']['variants'])):
                            if media_array[0]['video_info']['variants'][i]['content_type'] == 'video/mp4':
                                video_url= media_array[0]['video_info']['variants'][i]['url']
                        video_data = requests.get(video_url).content
                        with open('video.mp4', 'wb') as handle:
                            handle.write(video_data)
                        wating_text.value = "Download completed!!"
                        page.update()
                    else:
                        wating_text.value = "Error in the link"
                        page.update()
                except Exception as e:
                    wating_text.value = f"Error: {e}"
                    page.update()

    page.title = "Media Downloader"
    page.window_height = 500
    page.window_width = 500

    yt_tittle = f.Text(value="Youtube Downloader", color=f.colors.WHITE, size=20)
    tw_tittle = f.Text(value="Twitter Downloader", color=f.colors.WHITE, size=20)
    wating_text = f.Text(value="", color=f.colors.WHITE, size=20)
    yt_input = f.TextField(value="Enter the link",text_align="left", color=f.colors.WHITE)
    
    tw_input = f.TextField(value="Enter the link",text_align="left", color=f.colors.WHITE)
    page.add(
        f.Row([yt_tittle]),
        f.Row([yt_input,f.ElevatedButton("Download YT",on_click=download_yt)]),
        f.Row([tw_tittle]),
        f.Row([tw_input, f.ElevatedButton("Download TW",on_click=download_tw)]),
        f.Row([wating_text])
        )

f.app(target=main )