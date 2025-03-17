# download video as wav and isolate 30 seconds of it, starting at 15 seconds in
./yt-dlp -x --audio-format wav  --downloader ffmpeg --downloader-args "ffmpeg:-ss 180 -t 30" -P "./samples" -o "derekjacobi_illidad1.%(ext)s" "https://www.youtube.com/watch?v=ag2IAxsGChU" 
./yt-dlp -x --audio-format wav  --downloader ffmpeg --downloader-args "ffmpeg:-ss 120 -t 30" -P "./samples" -o "derekjacobi_illidad2.%(ext)s" "https://www.youtube.com/watch?v=ag2IAxsGChU" 
./yt-dlp -x --audio-format wav  --downloader ffmpeg --downloader-args "ffmpeg:-ss 60 -t 30" -P "./samples" -o "derekjacobi_illidad3.%(ext)s" "https://www.youtube.com/watch?v=ag2IAxsGChU" 
