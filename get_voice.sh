# download video as wav and isolate 30 seconds of it, starting at 15 seconds in
./yt-dlp -x --audio-format wav  --downloader ffmpeg --downloader-args "ffmpeg:-ss 15 -t 30" -P "./samples" "https://www.youtube.com/watch?v=x4ONi1ROGH8" 
