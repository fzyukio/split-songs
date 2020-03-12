# split-song

## Install python
- Recommend python 3.5+ or python 2.7+, but should work with most versions 
- If on Windows, don't forget to check the option "Add python to the PATH environment variable"
- On Linux/Mac, you know what to do
- After installation, check that it can be called by opening a terminal and type `python --version`.
If you see `Python 2.x.x` or `Python 3.x.x` you're good to go

## Run the script
- Using git `git checkout https://github.com/fzyukio/split-songs.git` or download ZIP file at `https://github.com/fzyukio/split-songs/archive/master.zip`
- If you download the ZIP file, extract it. Let's say you extract it to `C:\Koe\split-songs\`
- Open a terminal and `cd "C:\Koe\split-songs" `
- Let's say your WAV file is located at "C:\Users\John\My Music\long song.wav", and you want to split it into smaller WAVs
of length 10 seconds each, with 1 second overlap between two consecutive chunks, you will run the command as following:

```bash
python main.py --input="C:\Users\John\My Music\long song.wav" --length=10 --overlap=1
```
- The program will split this WAV into `long song__1.wav`, `long song__2.wav`, etc...
- If there are says 14 chunks, their enumeration will be zero padded as `long song__01.wav`,..., `long song__14.wav`
- If there are says 120 chunks, their enumeration will be three zero padded i.e. `long song__001.wav`,...,`long song__123.wav`

