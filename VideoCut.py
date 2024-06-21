import functools
from PIL import Image
import moviepy
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QListWidgetItem, QLabel, QFileDialog
from moviepy.audio.AudioClip import AudioClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import VideoFileClip, concatenate_videoclips, transfx, concatenate
from moviepy.video.VideoClip import TextClip, ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.fx.rotate import rotate
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from moviepy.video.fx.speedx import speedx
from moviepy.video.fx.resize import  resize
from moviepy.audio.fx.volumex import volumex
from moviepy.audio.fx.all import volumex
from moviepy.video.fx.crop import crop
import moviepy.editor as mpe
import moviepy.editor as mpy
import urllib.parse

import cv2
import numpy as np
from moviepy.editor import VideoFileClip
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSlider, QLabel
from PyQt5.QtCore import Qt
from ColorBalance import ColorBalance
from Contrast import ContrastWindow

#Definim doate funcțiile pentru a putea să exportam fisierele de tip video

def cut_video(video_name, start_time=0, end_time=None):
    clip = VideoFileClip(video_name)
    if not end_time:
        end_time = clip.duration

    clip = clip.subclip(start_time, end_time)
    dot_index = video_name.rfind('.')
    cut_video_name = video_name[: dot_index] + '_{}_{}'.format(start_time, end_time) + video_name[dot_index:]
    clip.write_videofile(cut_video_name)
    return cut_video_name


def extract_audio(video_name, start_time=0, end_time=None):
    clip = VideoFileClip(video_name)
    if not end_time:
        end_time = clip.duration

    clip = clip.subclip(start_time, end_time)
    dot_index = video_name.rfind('.')
    cut_audio_name = video_name[: dot_index] + '_audio_{}_{}.mp3'.format(start_time, end_time)
    clip.audio.write_audiofile(cut_audio_name)
    return video_name


def rotate_video(video_name, start_time=0, end_time=None, degree=0):
    clip = VideoFileClip(video_name)
    if not end_time:
        end_time = clip.duration

    clip1 = clip.subclip(0, start_time)
    clip2 = clip.subclip(start_time, end_time).rotate(degree)
    # clip3 = clip.subclip(end_time, clip.duration)
    final_clip = concatenate_videoclips([clip1, clip2])
    clip = final_clip

    dot_index = video_name.rfind('.')
    cut_video_name = video_name[: dot_index] + '{}'.format("rotated") + video_name[dot_index:]
    
    # Specificăm codecul (e.g., 'libx264')
    clip.write_videofile(cut_video_name, codec='libx264')
    return cut_video_name


def fade_in(video_name, duration=1, start_time=0, end_time=None):
    clip = VideoFileClip(video_name)
    if not end_time:
        end_time = clip.duration

    new_clip = clip.copy()
    clip = fadein(new_clip, duration)

    dot_index = video_name.rfind('.')
    cut_video_name = video_name[: dot_index] + '{}'.format("fade_in") + video_name[dot_index:]
    clip.write_videofile(cut_video_name)
    return cut_video_name

def fade_out(video_name, duration=1, start_time=0, end_time=None):
    clip = VideoFileClip(video_name)
    if not end_time:
        end_time = clip.duration

    new_clip = clip.copy()
    clip = fadeout(new_clip, duration)

    dot_index = video_name.rfind('.')
    cut_video_name = video_name[: dot_index] + '{}'.format("fade_out") + video_name[dot_index:]
    clip.write_videofile(cut_video_name)
    return cut_video_name


from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

def add_text(video_name, text, fontsize, color, font, start_time=0, end_time=None):
    # Încărcarea videoclipului sursă
    clip = VideoFileClip(video_name)
    
    # Asigură-te că end_time este valid
    if not end_time or end_time > clip.duration:
        end_time = clip.duration
    
    # Calculează durata pentru care va fi afișat textul
    duration = end_time - start_time
    
    # Crearea TextClip-ului
    # 'caption' permite textul să fie în mai multe linii dacă este prea lung
    text_clip = TextClip(text, fontsize=int(fontsize), color=color, font=font, method='caption', size=clip.size)
    
    # Setează poziția textului la centru și durata
    text_clip = text_clip.set_pos('center').set_start(start_time).set_duration(duration)
    
    # Crearea unui videoclip compozit care include videoclipul original și TextClip-ul
    video_with_text = CompositeVideoClip([clip, text_clip])
    
    # Generarea numelui fișierului de ieșire și salvarea videoclipului
    output_filename = f"{video_name.rsplit('.', 1)[0]}_add_text.mp4"
    video_with_text.write_videofile(output_filename, codec='libx264', audio_codec='aac')
    
    return output_filename




import time
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, transfx

def concatenate_video(video_name1, videoSamples, slide_out=False, start_time=0, end_time=None):
    videos = []
    target_resolution = (1280, 720)  # Setează rezoluția țintă (modifică după cum e necesar)

    if not slide_out:
        for v in videoSamples:
            clip = VideoFileClip(v).resize(newsize=target_resolution)  # Redimensionează fiecare clip
            videos.append(clip)
        finalclip = concatenate_videoclips(videos, method="compose")

    else:
        for v in videoSamples:
            clip = VideoFileClip(v).resize(newsize=target_resolution)  # Redimensionează fiecare clip
            videos.append(clip)
        clips = videos
        slided_clips = [CompositeVideoClip([clip.fx(transfx.slide_out, 1, 'bottom')]) for clip in clips]
        slided_clips = [CompositeVideoClip([clip.fx(transfx.slide_in, 1, 'top')]) for clip in slided_clips]
        clips = []
        for v in slided_clips:
            clips.append(v)
        finalclip = concatenate_videoclips(clips, method="compose")
        
        
    
    # video_name1 = str(time.time())
    # cut_video_name = video_name1 + ".mp4"  # Adaugă extensia .mp4 la numele fișierului
    
    # dot_index = video_name.rfind('.')
    # cut_video_name = video_name[: dot_index] + '{}'.format("change_speed") + video_name[dot_index:]
    
    
    dot_index = video_name1.rfind('.')
    cut_video_name = video_name1[:dot_index] + '{}'.format ("with_concatenate") + video_name1[dot_index:]

    finalclip.write_videofile(cut_video_name+".mp4", codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)
    return cut_video_name




from moviepy.editor import VideoFileClip

def remove_piece_video(video_name, start_time, end_time):
    clip = VideoFileClip(video_name)
    # Asigură-te că start_time și end_time sunt în limitele duratei videoclipului
    if start_time >= clip.duration or end_time > clip.duration:
        raise ValueError("start_time or end_time exceeds the duration of the video.")

    clip1 = clip.subclip(0, start_time)
    clip2 = clip.subclip(end_time, clip.duration) if end_time < clip.duration else None

    # Dacă clip2 este None, înseamnă că end_time este la sfârșitul videoclipului, deci returnează doar prima parte
    final_clip = concatenate_videoclips([clip1, clip2]) if clip2 else clip1
    output_video = video_name.replace(".mp4", "_edited.mp4")
    final_clip.write_videofile(output_video, codec="libx264")

    return output_video



from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

def add_photo(video_name, photo_name, start_time, end_time):
    video_clip = VideoFileClip(video_name)
    image_clip = ImageClip(photo_name).set_duration(end_time - start_time).set_start(start_time).set_end(end_time)

    # Poziționează imaginea în centrul videoclipului
    image_clip = image_clip.set_position("center")

    # Creează un nou videoclip cu imaginea suprapusă pe videoclipul original
    final_clip = CompositeVideoClip([video_clip, image_clip])

    dot_index = video_name.rfind('.')
    output_name = video_name[:dot_index] + '_with_photo' + video_name[dot_index:]
    final_clip.write_videofile(output_name, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)
    return output_name


def change_speed(video_name, speed=1, start_time=0, end_time=None):
    clip = VideoFileClip(video_name)
    if not end_time:
        end_time = clip.duration

    clip = clip.set_fps(clip.fps * speed)
    final = clip.fx(speedx, speed)

    dot_index = video_name.rfind('.')
    cut_video_name = video_name[: dot_index] + '{}'.format("change_speed") + video_name[dot_index:]
    final.write_videofile(cut_video_name)
    return cut_video_name

def remove_audio(video_name, start_time=0, end_time=None):
    clip = VideoFileClip(video_name)
    if not end_time:
        end_time = clip.duration

    newaudio = clip.audio.fx(volumex, 0)
    new_clip = clip.set_audio(newaudio)

    dot_index = video_name.rfind('.')
    cut_video_name = video_name[: dot_index] + '{}'.format("remove_audio") + video_name[dot_index:]
    clip.write_videofile(cut_video_name)
    return cut_video_name

def concatenate_with_audio(video_name, audio_name, start_time=0, end_time=None):
    clip = VideoFileClip(video_name)
    if not end_time:
        end_time = clip.duration

    background_music = mpe.AudioFileClip(audio_name)
    new_clip = clip.set_audio(background_music)

    dot_index = video_name.rfind('.')
    cut_video_name = video_name[: dot_index] + '{}'.format("concatenate_audio") + video_name[dot_index:]
    new_clip.write_videofile(cut_video_name, codec='libx264',
                     audio_codec='aac',
                     temp_audiofile='temp-audio.m4a',
                     remove_temp=True)
    return cut_video_name

def add_subclip(video_name1, video_name2, start_time=0, end_time=None):
    clip1 = VideoFileClip(video_name1)
    clip2 = VideoFileClip(video_name2)
    video = CompositeVideoClip([clip1,
                                clip2.set_position(("center", "center"))])

    dot_index = video_name1.rfind('.')
    cut_video_name = video_name1[: dot_index] + '{}'.format("add_subclip") + video_name1[dot_index:]
    video.write_videofile(cut_video_name, codec='libx264',
                          audio_codec='aac',
                          temp_audiofile='temp-audio.m4a',
                          remove_temp=True)
    return cut_video_name

def optim_clip(video_name, subwidth=1, subheight=1, start_time=0, end_time=None):
    clip = VideoFileClip(video_name)
    widt = clip.w*subwidth
    heigh = clip.h*subheight
    clip = crop(clip, x1=((clip.w-widt)/2), y1=((clip.h-heigh)/2), x2=(clip.w - ((clip.w-widt)/2)), y2=(clip.h - ((clip.h-heigh)/2)))

    dot_index = video_name.rfind('.')
    cut_video_name = video_name[: dot_index] + '{}'.format("optimize_video") + video_name[dot_index:]
    clip.write_videofile(cut_video_name, codec='libx264',
                          audio_codec='aac',
                          temp_audiofile='temp-audio.m4a',
                          remove_temp=True)
    return cut_video_name

def brightness(video_name, start_time=0, end_time=None, brightness_factor=1.0):
     
    clip = mpy.VideoFileClip(video_name)
    if not end_time:
        end_time = clip.duration

    subclip = clip.subclip(start_time, end_time)
    # subclip = subclip.resize(width=subwidth * clip.w, height=subheight * clip.h)
    print(brightness_factor)
    final_clip = subclip.fx(mpy.vfx.colorx, brightness_factor)

    dot_index = video_name.rfind('.')
    cut_video_name = video_name[:dot_index] + '{}'.format("_brightness") + video_name[dot_index:]
    final_clip.write_videofile(cut_video_name, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a',
                               remove_temp=True)
    return cut_video_name





 
from moviepy.editor import VideoFileClip
import numpy as np
from skimage import img_as_ubyte, img_as_float, exposure, color

def adjust_contrast(image, factor=1.0):
    # Ajustează contrastul unei imagini
    f = (259 * (factor + 255)) / (255 * (259 - factor))
    contrasted = f * (image - 128) + 128
    return np.clip(contrasted, 0, 255)  # Asigură-te că valorile pixelilor sunt între 0 și 255

def adjust_contrast_and_saturation(image, contrast_factor, saturation_factor):
    # Ajustare contrast
    contrasted = adjust_contrast(image, contrast_factor)
    # Convertire în HSV pentru ajustarea saturației
    hsv = color.rgb2hsv(contrasted / 255.0)  # Normalizează imaginea la intervalul 0-1
    hsv[:, :, 1] *= saturation_factor
    adjusted = color.hsv2rgb(hsv)
    return img_as_ubyte(adjusted)  # Asigură-te că imaginea este între 0 și 255

def change_contrast_video(video_name, start_time=0, end_time=None, contrast_factor=1.0, saturation_factor=1.0):
    clip = VideoFileClip(video_name)
    if not end_time:
        end_time = clip.duration

    subclip = clip.subclip(start_time, end_time)
    final_clip = subclip.fl_image(lambda image: adjust_contrast_and_saturation(image, contrast_factor, saturation_factor))

    dot_index = video_name.rfind('.')
    cut_video_name = video_name[:dot_index] + '_contrast_saturation' + video_name[dot_index:]
    final_clip.write_videofile(cut_video_name, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)
    return cut_video_name






from moviepy.editor import VideoFileClip
import numpy as np
from skimage import img_as_ubyte, img_as_float
from skimage.exposure import rescale_intensity

def color_adjust(image, red, green, blue):
    # Convert image to float for precision in calculations
    image_float = img_as_float(image)

    # Apply color balance adjustments
    image_float[:, :, 0] *= red   # Red channel
    image_float[:, :, 1] *= green # Green channel
    image_float[:, :, 2] *= blue  # Blue channel

    # Clip values to maintain valid range
    image_float = np.clip(image_float, 0, 1)

    # Rescale back to uint8
    corrected = img_as_ubyte(image_float)
    return corrected

def color1(video_name, start_time=0, end_time=None, red=1.0, green=1.0, blue=1.0):
    clip = VideoFileClip(video_name)
    if not end_time:
        end_time = clip.duration

    subclip = clip.subclip(start_time, end_time)
    final_clip = subclip.fl_image(lambda image: color_adjust(image, red, green, blue))

    dot_index = video_name.rfind('.')
    cut_video_name = video_name[:dot_index] + '_colorbalance' + video_name[dot_index:]
    final_clip.write_videofile(cut_video_name, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)
    return cut_video_name

def export_video(self):
    # Deschide fereastra de dialog pentru selectarea fișierului video
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    file_name, _ = QFileDialog.getSaveFileName(self, "Export Video", "", "Video Files (*.mp4);;All Files (*)", options=options)

    if file_name:
        try:
            # Calea către videoclipul original
            original_video_path = self.selected_file_path

            # Aici poți utiliza funcția de concatenare cu sunetul dorită
            concatenated_video_name = concatenate_with_audio(original_video_path, "cale_spre_sunet.mp3", start_time=0, end_time=None)

            # Salvează clipul final
            concatenated_video = VideoFileClip(concatenated_video_name)
            concatenated_video.write_videofile(file_name, codec="libx264", audio_codec="aac")

            self.terminal_output.append(f"Export successful. Video saved at: {file_name}")
        except Exception as e:
            # În caz de eroare, afișează mesajul în terminal
            self.terminal_output.append(f"Export failed. Error: {str(e)}")

    
