$AudioPath = "py_tools\data\self_songbie.mp3"
$VideoPath = "py_tools\output\video\self_songbie.mp4"

$AudioBitrate = "192k"

Write-Host "Audio: $AudioPath"
Write-Host "Video: $VideoPath"

$outputPath = "py_tools\output\sound\self_songbie.mp4"

ffmpeg -y -i "$VideoPath" -i "$AudioPath" -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a $AudioBitrate -shortest "$outputPath"

Write-Host "Done: $outputPath"