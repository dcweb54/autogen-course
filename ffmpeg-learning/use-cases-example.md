[1][working] ffmpeg -loop 1 -i ./stocks/image-1.png -vf "zoompan=z='min(zoom+0.005,1.5)':d=125" -t 5 stocks/zoom_test.mp4

[2] [failed] ffmpeg -loop 1 -i ./stocks/image-1.png -vf "zoompan=z='1.1':x='ix+0.5':y='iy+0.5':d=1" -t 6 stocks/ken_burns.mp4

[3][failed] ffmpeg -loop 1 -i ./stocks/image-1.png -vf "zoompan=z=2:x='iw/2-iw/4':y='ih/2-ih/4':d=1" -t 3 stocks/zoom_center.mp4

[4] [failed] ffmpeg -i ./stocks/image-1.png -vf "drawtext=text='Test Watermark':x=10:y=10:fontsize=24:fontcolor=white" stocks/text_burn.jpg

[5] ffmpeg -loop 1 -i ./stocks/image-1.png -vf "zoompan=z='1+0.3*on/100':x='on*2':y='on*1.5':d=100,scale=1920:1080" -t 4 -c:v libx264 -pix_fmt stocks/yuv420p clip1.mp4
