# Foreign Whispers

## Authors

- [animalracer3](https://github.com/AnimalRacer3)
- [johnnymayodev](https://github.com/johnnymayodev)

## Warning

Running on macOS is not recommended. First, ensure that you have downloaded all the [dependancies](#dependencies) (including FFmpeg).
Second, if you're getting an error about FFmpeg not being found, then you need to add FFmpeg to your PATH.

For example, if you installed FFmpeg using [Homebrew](https://brew.sh/), then you can add the following lines of code to **line 5** of `libraries/milestone_2.py`:

```python
ffmpeg_path = "/opt/homebrew/bin/ffmpeg"
os.environ["PATH"] += f":{os.path.dirname(ffmpeg_path)}"
os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path
```

## Dependencies

### Python (pip)

#### Milestone 1

[pytube](https://pytube.io/en/latest/)

[YouTube Transcript/Subtitle API](https://pypi.org/project/youtube-transcript-api/)

```bash
pip install pytube
pip install youtube-transcript-api
```

#### Milestone 2

[MoviePy](https://zulko.github.io/moviepy/)

[openai/whisper](https://github.com/openai/whisper/tree/main)

```bash
pip install moviepy
pip install openai-whisper
```

#### Milestone 3

[argos-translate](https://github.com/argosopentech/argos-translate)

```bash
pip install argostranslate
```

### Command Line Tools

#### Milestone 2

[FFmpeg](https://ffmpeg.org/)

```bash
# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# on Arch Linux
sudo pacman -S ffmpeg

# on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg

# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg
```

## Usage

Windows

```bash
cd \path\to\dir
python ./main.py
```

MacOS/Linux

```bash
cd /path/to/dir
python3 ./main.py
```

Running the script will create new folders in the current directory (where you're running the script from).
