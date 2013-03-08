for i in *.flv
do
  ffmpeg -i "$i" -acodec libmp3lame -ac 2 -ab 128 -vn -y "`basename "$i" .flv`.mp3"
done
