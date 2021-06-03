import opensim as osim
from opensim import Vec3
import numpy as np
from helper import quat2sto_single, sto2quat
import helper as h
import time
import os
import sys
from multiprocessing import Process, Queue
import workers # define the worker functions in this .py file

print("Start!")

# Customize real-time kinematics for use by setting flag and looking at corresponding code below.
real_time = False # set to True for using the kinematics in the python script for real-time applications

# Parameters for IK solver
fake_real_time = True # True to run offline, False to record data and run online
log_temp = True # True to log CPU temperature data
log_data = False # if true save all IK outputs, else only use those in reporter_list for easier custom coding
home_dir = '/home/ubuntu/RealTimeKin/' # location of the main RealTimeKin folder
uncal_model = 'Rajagopal_2015.osim'
uncal_model_filename = home_dir + uncal_model
model_filename = home_dir+'calibrated_' + uncal_model
fake_online_data = home_dir+'recordings/'#test_data.npy'#'test_IMU_data.npy'#'MT_012005D6_009-001_orientations.sto'
sto_filename = home_dir+'tiny_file.sto'
visualize = False
### Initataion para
rate = 20.0 # samples hz of IMUs
accuracy = 0.001 # value tuned for accurate and fast IK solver
constraint_var = 10.0 # value tuned for accurate and fast IK solver
init_time = 4.0 # seconds of data to initialize from

# Initialize the quaternions
signals_per_sensor = 6 #should be check
file_cnt = 0
save_dir_init = home_dir+ 'recordings/' # appending folder name here
save_file = '/recording_'
ts_file = '/timestamp_'
script_live = True

#def readIMU(fake_online_data, init_time, signals_per_sensor, save_dir_init,home_dir):
# Load the initialization information about the sensors
tca_inds = []
num_parts = 0
calibrate_sensors = False
parallelize = False
old_lines = []
save_folder = 'test_dir'
sim_len = 600
# Defining the external signal trigger
imu_only = False
with open(home_dir+'0_settings.txt', 'r') as f:
    for cnt, line in enumerate(f):
        old_lines.append(line)
        if cnt == 0:
            body_parts = line.split(',')
            num_parts = len(body_parts)
        elif cnt == 1:
            tca_inds = line.split(',')
            if num_parts != len(tca_inds):
                print("Wrong number of tca_indeces given, doesn't match number of body parts.")
            alt_address_list = []
            tca_inds = tca_inds[:-1]
            for i in range(len(tca_inds)):
                if len(tca_inds[i]) == 1: # alternate
                    tca_inds[i] = int(tca_inds[i])
                    alt_address_list.append(False)
                elif len(tca_inds[i]) > 1:
                    tca_inds[i] = int(tca_inds[i][0])
                    alt_address_list.append(True)
        elif cnt == 2:
            rate = float(line)
            print("Rate:",rate)
        elif cnt == 3:
            cal_word = line.strip()
            if cal_word == 'parallel': # run with extra thread multiprocessing
                parallelize = True
                fake_real_time = False
            elif cal_word == 'online': # run offline with given file path in recordings folder
                fake_real_time = False
            elif cal_word == 'offline':
                fake_real_time = False
                imu_only = True
            else:
                fake_path = cal_word
                fake_real_time = True
        elif cnt == 4:
            cal_word = line.strip()
            save_folder = cal_word
        elif cnt == 5:
            sim_len = float(line)
            print("Sim length:",sim_len)
        elif cnt == 6:
            cal_word = line.strip()
            if cal_word == 'calibrate': # calibrate IMUs at start
                calibrate_sensors = True
f.close()
if calibrate_sensors:
    with open(home_dir+'0_settings.txt', 'w') as f:
        f.writelines(old_lines[:-1])
    f.close()

print(tca_inds)

from JY61P_reading import JY61P, ReadIMU
# import adafruit_tca9548a
import board
import busio
import digitalio
from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice
# trigger = digitalio.DigitalInOut(board.D16) # external signal should be applied to the BCM 16 pin
# trigger.direction = digitalio.Direction.INPUT # this signal will be checked, if 3.3V is applied, recording will be started
# trigger.pull = digitalio.Pull.DOWN # pull this input low at all times
# trigger_status = False # set to true if the trigger is used to start a recording
# Initializing the different methods
button_address = const(0x6F) # I2c address for LED button
sensors_address_list = [0x50,0x51,0x52,0x53,0x54,0x55,0x56,0x57]

# checks for button press, have to wait at least time_min seconds before pressing again

# i2c = busio.I2C(board.SCL, board.SDA)
with busio.I2C(board.SCL, board.SDA) as i2c:
    button = I2CDevice(i2c, button_address)

# test to read one IMU
test_IMUaddress = sensors_address_list[0]
print(ReadIMU(test_IMUaddress))

# int Button
# last_pressed = time.time() - 1.0
# pressed = False
# button_mode(button, 0) # turn button off
# clear_button(button)

# # tca = adafruit_tca9548a.TCA9548A(i2c)
# tca = i2c
# print(tca)


# define sensors
sensor_inds = tca_inds[1:]
alt_address_list = alt_address_list[1:]
sensor_list = []
sensor_ind_list = []
sensor_number = []
sensor_cnt = 0
sensor_rot = []
sensor_rot_type = [0,0,1,1,3,2,2,3,1,1,1,2,2,2] # define rotation types
sensor_labels_full = ['pelvis_imu','torso_imu','femur_l_imu','tibia_l_imu','calcn_l_imu','femur_r_imu','tibia_r_imu','calcn_r_imu','humerus_l_imu','ulna_l_imu','hand_l_imu','humerus_r_imu','ulna_r_imu','hand_r_imu']
sensor_label_list = []

while True:
    for i, s_ind in enumerate(sensor_inds):
        if s_ind != 9: # 9 for not used Sensor in setting
            # print("Start Reading")
            if not fake_real_time:
                if alt_address_list[i]: # if true use alternate address
                    s = ReadIMU(const(0x50))
                else:
                    s = ReadIMU(sensors_address_list[i-1])
                    print(s_ind)
                    print(s.acceleration)
                    print(s.gyro)     
                sensor_list.append(s)
            sensor_ind_list.append(s_ind)
            len_sensor_list = len(sensor_ind_list)
            sensor_number.append(sensor_cnt)
            sensor_cnt += 1
            sensor_rot.append(sensor_rot_type[i]) # say for this number sensor how to rotate it
            sensor_label_list.append(sensor_labels_full[i])
    # print(sensor_list)

    # print(s.acceleration)
    # print(s.gyro)
    # print(len(sensor_list))
    # print(sensor_list)
    time.sleep(1)

def button_mode(button, state, ON=0xFF, OFF = 0x00, LED=0x0F, b_cycle_time=0x1B, b_brightness=0x19, b_off_time=0x1D):
    with button:
        if state == 0: # turn off
            button.write(bytes([b_brightness, OFF]), stop=False)
            button.write(bytes([b_off_time, OFF]), stop=False)
            button.write(bytes([b_cycle_time, OFF]), stop=False)
        elif state == 1: # blink
            button.write(bytes([b_brightness, LED]), stop=False)
            button.write(bytes([b_off_time, ON]), stop=False)
            button.write(bytes([b_cycle_time, ON]), stop=False)
        elif state == 2: # solid red
            button.write(bytes([b_brightness, LED]), stop=False)
            button.write(bytes([b_off_time, OFF]), stop=False)
            button.write(bytes([b_cycle_time, OFF]), stop=False)
        else:
            print("Unknown button state")

def check_button(button, last_pressed, time_min = 1.0, PRESSED = 0x03, OFF = 0x00):
    state = False
    with button:
        button.write(bytes([PRESSED]), stop=False)
        result = bytearray(1)
        button.readinto(result)
        #print(result)
        if result != bytes([OFF]) and (time.time()-last_pressed > time_min): # pressed
            state = True
            last_pressed = time.time()
            button.write(bytes([PRESSED, OFF]), stop=False) # reset
        else:
            button.write(bytes([PRESSED, OFF]), stop=False) # reset
    return state, last_pressed

def clear_button(button, PRESSED = 0x03, OFF = 0x00):
    with button:
        button.write(bytes([PRESSED, OFF]), stop=False) # reset

def calibrating_sensors(cal_dir, gyro_file, button, rate, sensor_list, calibration_time=10.0, signals_per_sensor=6, b_brightness=0x19):
    dt = 1/rate
    num_samples = int(calibration_time//dt)
    num_sensors = len(sensor_list)
    cal_data = np.zeros((num_samples, 6*num_sensors))
    time_start = time.time()
    led_range = 255
    sample_cnt = 0
    while sample_cnt < num_samples:
        cur_time = time.time()
        if cur_time >= time_start + dt: # time for next reading
            time_start = cur_time
            for j, s in enumerate(sensor_list):
                s_off = j*signals_per_sensor
                cal_data[sample_cnt, s_off+3:s_off+6] = s.gyro
            with button:
                button.write(bytes([b_brightness, sample_cnt*8%led_range]), stop=False)
            sample_cnt += 1
    gyro_offset = -1.0*np.mean(cal_data,axis=0)
    np.save(cal_dir+gyro_file, gyro_offset)
