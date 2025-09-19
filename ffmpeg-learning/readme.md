Solution 4: Fast CPU Encoding (Most Reliable)
```bash
ffmpeg -i subject.mp4 -vf "drawtext=fontfile=arial:text='Welcome to My Channel':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=h-100-10*t:enable='between(t,2,8)':borderw=2:bordercolor=black@0.7" -preset veryfast -c:a copy output.mp4

```


Solution 5: Optimized CPU with Multi-threading
```bash
ffmpeg -i subject.mp4 -vf "drawtext=fontfile=arial:text='Welcome to My Channel':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=h-100-10*t:enable='between(t,2,8)':borderw=2:bordercolor=black@0.7" -preset veryfast -threads 0 -movflags +faststart -c:a copy output.mp4

```