from speakAndSpell.aiVoice import AiVoice
from youtubesearchpython import VideosSearch
import vlc, yt_dlp

MEDIA_QUALITIES = [
    "ultralow",
    "low",
    "medium",
]

instance = vlc.Instance("--no-xlib -q > /dev/null 2>&1")

class VideoPlayer(AiVoice):
    def __init__(self, voice_path, cache_path, volume:int = 100):
        self.player = instance.media_player_new()

        self.setVolume(volume)

        super().__init__(instance, self.player, voice_path, cache_path)

    def generate_stream_url(self, url):
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

    def pause(self):
        self.player.pause()

    def getVolume(self):
        return self.volume
    
    def setVolume(self, volume:int):
        self.volume = volume
        self.player.audio_set_volume(volume)
    
    def say(self, text:str, quality:str="ultra_fast"):
        self.player.set_media(vlc.Media(super().generateVoice(text, quality)))
        self.play()