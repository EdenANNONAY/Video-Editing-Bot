import os 
import subprocess
import random

outroPath = 'Outro/Outro.mp4'
filename='Videos.txt'

# Logo

print('\n\n   ▄█    █▄     ▄██████▄     ▄████████ ███    █▄     ▄████████') 
print('  ███    ███   ███    ███   ███    ███ ███    ███   ███    ███')
print('  ███    ███   ███    ███   ███    ███ ███    ███   ███    █▀')  
print(' ▄███▄▄▄▄███▄▄ ███    ███  ▄███▄▄▄▄██▀ ███    ███   ███')        
print('▀▀███▀▀▀▀███▀  ███    ███ ▀▀███▀▀▀▀▀   ███    ███ ▀███████████') 
print('  ███    ███   ███    ███ ▀███████████ ███    ███          ███') 
print('  ███    ███   ███    ███   ███    ███ ███    ███    ▄█    ███') 
print('  ███    █▀     ▀██████▀    ███    ███ ████████▀   ▄████████▀')  
print('                            ███    ███                        \n\n')

# Video to be edited

video = str(input("Please enter the name of the video :"))
videoOriginal = video


# Function to get length of file

def get_length (input_file) :

    result = subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',input_file],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    return float(result.stdout)

# Function to get a random Audio

def get_audio():


    return "Audio/"+random.choice(os.listdir("Audio"))

def get_format_from_seconds(seconds):

    # Duration in seconds

    result = float(seconds)

    # Get the amount of hours because 
    # there is 3600 seconds in an hour

    resultHour = int(result/3600)

    # Get the amount of minutes left after we took the hours
    # with an euclidian division and modulo
    # then divide it by 60 to get the minutes

    resultMinute = int((result%3600)/60)

    # Get the amount of seconds left  
    # after we took the minutes with an euclidian division 
    # and the modulo operator

    resultSeconds = int(result%60)

    # Properly format in hh:mm:ss

    if(resultHour < 10) :

        resultHour = "0"+str(resultHour)

    
    if(resultMinute < 10) :

        resultMinute = "0"+str(resultMinute)

    
    if(resultSeconds < 10):

        resultSeconds = "0"+str(resultSeconds)

    



    finalResult = str(resultHour)+":"+str(resultMinute)+":"+str(resultSeconds)

    return finalResult





# Set FPS to 26

os.system(f'ffmpeg -i {video} -filter:v fps=fps=32 -y videoFPS.mp4 ')

os.system(f'ffmpeg -i {outroPath} -filter:v fps=fps=32 -y OutroFPS.mp4 ')

outroPath = 'OutroFPS.mp4'
video = 'videoFPS.mp4'

# Change the speed of video to 1.20x

os.system(f'ffmpeg -i {video} -r 39 -filter:v "setpts=0.80*PTS" videoSpeedx120.mp4')

video = 'videoSpeedx120.mp4'

# Cut last 5 seconds of the video 

# Get video length
 
vidLength = get_length(video)


# Cut time 5 seconds before the end

cutTime = vidLength - 5

# Format it in hh:mm:ss

cutTime = get_format_from_seconds(cutTime)

os.system(f'ffmpeg -i {video} -ss 00:00:00 -to {cutTime} -c copy videoResized.mp4')

video = 'videoResized.mp4'

# Mute the video

os.system(f'ffmpeg -i {video} -vcodec copy -an videoMuted.mp4')

video = 'videoMuted.mp4'

# Add outro

# Resize kazam video

os.system(f'ffmpeg -i {video} -vf scale=1280:720,setsar=2049:2048 videoMutedAndResized.mp4')

video = 'videoMutedAndResized.mp4'

file = open(filename,"w")

file.write("file '"+video+"'\n")
file.write("file '"+outroPath+"'")

file.close()

os.system(f'ffmpeg -i {video} -i {outroPath} \
-filter_complex "[0:v:0][1:v:0]concat=n=2:v=1:a=0[outv]" \
-map "[outv]"  videoAndOutro.mp4')


video = 'videoAndOutro.mp4'

# Get a random audio file

audio_list = []
audio_list.append(str(get_audio()))

vidLength = get_length(video)

audioLength = get_length(audio_list[0])

# If the video length is longer than the audio length 
# we add more audio files 

if vidLength > audioLength :

    while (vidLength > audioLength ) :

        # Add a new audio

        newAudio = get_audio()

        for audio in audio_list :
            while(audio == newAudio) :
                newAudio = get_audio()

        audio_list.append(newAudio)


        # Clean the audio length variable

        audioLength = 0

        # Add each audio in audioList to the full 
        # audio length

        for audio in audio_list :

            audioLength+=get_length(audio) 

# Add audio(s) to video



# Concatenate audios

audio_file = open("audios.txt","w")
for audio in audio_list :
    audio_file.write("file '"+audio+"'\n")
audio_file.close()

os.system('ffmpeg -f concat -safe 0 -i audios.txt -c copy mainAudio.mp3')

mainAudio = 'mainAudio.mp3'

os.system(f'ffmpeg -i {video} -i {mainAudio} -c copy -shortest videoWithSound.mp4')

video = 'videoWithSound.mp4'
time_fade_out_start = get_length(video) - 8

# Fade out the audio of our video 

os.system(f'ffmpeg -i {video} -af "afade=t=out:st={time_fade_out_start}:d=8"  Rendu/Rendu_{videoOriginal}')

os.system('rm videoResized.mp4 videoMuted.mp4 videoFPS.mp4 videoAndOutro.mp4 videoMutedAndResized.mp4 videoSpeedx120.mp4 videoWithSound.mp4 OutroFPS.mp4 mainAudio.mp3 Videos.txt audios.txt')