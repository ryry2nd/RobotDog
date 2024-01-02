from youtubesearchpython import VideosSearch
import vlc, yt_dlp, pyttsx3

MEDIA_QUALITIES = [
    "ultralow",
    "low",
    "medium",
]

voice = pyttsx3.init()

instance = vlc.Instance("--no-xlib -q > /dev/null 2>&1")

class VideoPlayer:
    def __init__(self, volume:int = 100):
        self.player = instance.media_player_new()
        self.setVolume(volume)

    def _generate_stream_url(self, url):
        ydl_opts = {"quiet": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url_list = []
            counter = -1
            for format in info["formats"]:
                video_format = format["format"]
                video_format_short = video_format[
                    video_format.find("(") + 1 : video_format.find(")")
                ]
                if (
                    (video_format[2] == " " or "audio only" in video_format)
                    and not ("DASH" in video_format)
                    and not (
                        counter > -1
                        and video_format_short == url_list[counter]["video_format"]
                    )
                ):
                    url_list.append(
                        {
                            "stream_url": format["url"],
                            "video_format": video_format_short,
                        }
                    )
                    counter += 1

        break_out_flag = False
        for index in range(2):
            if break_out_flag:
                break
            for item in url_list:
                if item["video_format"] == MEDIA_QUALITIES[2 - index]:
                    url = item["stream_url"]
                    break_out_flag = True
                    break
        return url

    def setVid(self, title):
        results = VideosSearch(title, limit=1).result()["result"]
        self.player.set_media(
            instance.media_new(self.generate_stream_url(results[0]["link"]))
        )

    def setFile(self, file):
        self.player.set_media(vlc.Media(file))

    def play(self):
        self.player.play()

    def getVolume(self):
        return self.volume
    
    def setVolume(self, volume:int):
        self.volume = volume
        self.player.audio_set_volume(volume)
        voice.setProperty('volume', volume/100)

    def say(self, text:str):
        voice.stop()
        voice.say(text)
        voice.runAndWait()
    
    def stop(self):
        self.player.pause()