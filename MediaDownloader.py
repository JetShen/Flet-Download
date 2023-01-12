from pytube import YouTube
import requests
import flet as f

def main(page: f.Page):
    def download_yt(e):
        if tex_input.value == "" or tex_input.value == "Enter the link":
            wating_text.value = "Please enter the link"
            page.update()
        else:
            wating_text.value = "Please wait..."
            page.update()
            try:
                link = str(tex_input.value)
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
            except:
                wating_text.value = "Error try again"
                page.update()

    page.title = "Youtube Downloader"
    page.window_height = 500
    page.window_width = 500

    page.add(f.Text(value="Youtube Downloader", color=f.colors.WHITE, size=20))
    wating_text = f.Text(value="", color=f.colors.WHITE, size=20)
    tex_input = f.TextField(value="Enter the link",text_align="left", color=f.colors.WHITE)

    page.add(
        f.Row([
            tex_input,
            f.ElevatedButton("Download YT",on_click=download_yt)
        ]),
        f.Row([wating_text])
        )

f.app(target=main)