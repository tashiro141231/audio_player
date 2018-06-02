#!/usr/bin/env python
import rospy
import time
import pyaudio
import wave

from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseActionResult

goal_x = 0
goal_y = 0
audio_num = -1

base_wav_path = '/home/tashiro-y/ros_study'
wr = wave.open('/home/tashiro-y/ros_study/chocolate.wav', "rb")

# base_wav_path = '/home/koyama-h/ros_study'
# wr = wave.open('/home/koyama-h/ros_study/chocolate.wav', "rb")

def GoalCallback(data):
    global goal_x
    global goal_y
    global audio_num
    x = data.pose.position.x
    y = data.pose.position.y

    if x < 1.0 and x > 0 and y > -1.0 and y < 0.0:
        audio_num = 0
    elif x < 1.0 and x > 0 and y > -5.0 and y < -4.0:
        audio_num = 1
    elif x < 5 and x > 4 and y < 0 and y > -1.0:
        audio_num = 2
    elif x < 5 and x > 4 and y > -5.0 and y < -4.0:
        audio_num = 3
    else:
        audio_num = -1
    print("auddio_num = " + str(audio_num))


def callback(in_data, frame_count, time_info, status):
    data = wr.readframes(frame_count)
    return (data, pyaudio.paContinue)


def PlayCallback(data):
    global audio_num
    global wr
    wav_path = base_wav_path + '/receive.wav'
    if audio_num == 0:
        wav_path = base_wav_path + '/receive.wav'
    elif audio_num == 1:
        wav_path = base_wav_path + '/potato.wav'
    elif audio_num == 2:
        wav_path = base_wav_path + '/chocolate.wav'
    elif audio_num == 3:
        wav_path = base_wav_path + '/juice.wav'

    p = pyaudio.PyAudio()
    if data.status.status == 3:
        wr = wave.open(wav_path, "rb")
        stream = p.open(format=p.get_format_from_width(wr.getsampwidth()),
                channels=wr.getnchannels(),
                rate=wr.getframerate(),
                output=True,
                stream_callback=callback)
    while stream.is_active():
        time.sleep(0.1)
    
    stream.stop_stream()
    stream.close()
    wr.close()
    p.terminate()

def AutoPlay():
    rospy.init_node('Audio_player', anonymous=True)
    rospy.Subscriber("/move_base_simple/goal", PoseStamped, GoalCallback)
    rospy.Subscriber("move_base/result", MoveBaseActionResult, PlayCallback) 
    r = rospy.Rate(30)

    while not rospy.is_shutdown():
        r.sleep()

if __name__ == '__main__':
    try:
        AutoPlay()
    except rospy.ROSInterruptException: pass

