# Foreign-Whispers
An API that accepts a youtube video(s) as input and outputs the video but with spoken and written subtitles to another language of your choosing.

# Docker
## Build
```docker build -t foreign-whispers .```

## Run
```docker run -p 5005:5005 foreign-whispers```

## Run privileged
```docker run --privileged -p 5005:5005 foreign-whispers```