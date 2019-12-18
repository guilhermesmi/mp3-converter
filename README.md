# MP3 Converter
Uses ffmpeg to extract mp3 audio files from mp4 videos. It can also add a sequence number to the files so that you can add to a playlist in a specific order. I've tested it using the video files from the CS6210 - Advanced Operating Systems class from GeorgiaTech.

## How to run the source code:
### Installing dependencies
```bash
pip install -r requirements.txt 
virtualenv create .
source bin/activate
```

### To run it:
```bash
python mp4tomp3.py -h (prints help)
python mp4tomp3.py -i <input folder> -o <output folder>
```

# Tested with:
Video Files Downloaded From: http://d2uz2655q5g6b2.cloudfront.net/ud189/Advanced%20Operating%20Systems%20Videos.zip

