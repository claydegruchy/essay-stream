# download video as wav and isolate 30 seconds of it, starting at 15 seconds in
./yt-dlp -x --audio-format wav  --downloader ffmpeg --downloader-args "ffmpeg:-ss 300 -t 30" -P "./samples" "https://www.dailymotion.com/video/x8hgyov" 
