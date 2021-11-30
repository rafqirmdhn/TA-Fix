# import modules
import csv
import argparse
import math
import traceback
import matplotlib.pyplot as plt

Accel_Scale     = 1
Gyro_Scale      = 1

time_diff       = 1 

def dist(a, b):
    return math.sqrt((a * a) + (b * b)) 
 
def get_x_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return math.degrees(radians)
 
def get_y_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return -math.degrees(radians)

def get_z_rotation(x,y,z):
    radians = math.atan2(z, dist(x,y))
    return math.degrees(radians)

def Write_Output():
    global pitch_list, roll_list, yaw_list, n_data

    with open('output.csv', mode='w', newline='') as csv_file:
        fieldnames = ['pitch', 'roll', 'yaw']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        
        for i in range(n_data):
            writer.writerow({'pitch': pitch_list[i], 'roll': roll_list[i], 'yaw': yaw_list[i]})

# parser
parser = argparse.ArgumentParser()
parser.add_argument("-g", "--gyro", help = "Specify Gyroscope data")
parser.add_argument("-a", "--accel", help = "Specify Accelerometer data")
args = parser.parse_args()

print ()
print ("********************")
print ("Complementary Filter")
print ("********************")
print ()

if(args.gyro != None and args.accel != None):
    try:
        print("Gyro data filepath: ", args.gyro)
        print("Accel data filepath: ", args.accel)

        # List that contains data
        gyro_x      = []
        gyro_y      = []
        gyro_z      = []

        accel_x     = []
        accel_y     = []
        accel_z     = []

        pitch_list  = []
        roll_list   = []
        yaw_list   = []

        n_data      = 0
        pitch       = 0
        roll        = 0
        yaw         = 0

        # Extract gyro data
        with open(args.gyro) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter = ',')
            line_count = 0
            # Iterates through rows
            for row in csv_reader:
                try:
                    if line_count > 0:
                        gyro_x.append((float(row[1])/Gyro_Scale)*57.2958)
                        gyro_y.append((float(row[2])/Gyro_Scale)*57.2958)
                        gyro_z.append((float(row[3])/Gyro_Scale)*57.2958)

                        n_data += 1

                    line_count += 1
                except:
                    pass
        # Extract accel data
        with open(args.accel) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter = ',')
            line_count = 0
            # Iterates through rows
            for row in csv_reader:
                try:
                    if line_count > 0:
                        accel_x.append(float(row[1])/Accel_Scale)
                        accel_y.append(float(row[2])/Accel_Scale)
                        accel_z.append(float(row[3])/Accel_Scale)
                    line_count += 1
                except:
                    pass

        K = 0.98
        K1 = 1 - K

        last_x = get_x_rotation(accel_x[0], accel_y[0], accel_z[0])
        last_y = get_y_rotation(accel_x[0], accel_y[0], accel_z[0])
        last_z = get_z_rotation(accel_x[0], accel_y[0], accel_z[0])

        gyro_offset_x = gyro_x[0]
        gyro_offset_y = gyro_y[0]
        gyro_offset_z = gyro_z[0]

        gyro_total_x = last_x - gyro_offset_x
        gyro_total_y = last_y - gyro_offset_y
        gyro_total_z = last_z - gyro_offset_z

        roll_list.append(last_x)
        pitch_list.append(last_y)
        yaw_list.append(last_z)
            
        for i in range(1, n_data):
            gyro_x[i] -= gyro_offset_x
            gyro_y[i] -= gyro_offset_y
            gyro_z[i] -= gyro_offset_z

            gyro_x_delta = (gyro_x[i] * time_diff)
            gyro_y_delta = (gyro_y[i] * time_diff)
            gyro_z_delta = (gyro_z[i] * time_diff)

            gyro_total_x += gyro_x_delta
            gyro_total_y += gyro_y_delta
            gyro_total_z += gyro_z_delta

            rot_x = get_x_rotation(accel_x[i], accel_y[i], accel_z[i])
            rot_y = get_y_rotation(accel_x[i], accel_y[i], accel_z[i])
            rot_z = get_z_rotation(accel_x[i], accel_y[i], accel_z[i])

            last_x = K * (last_x + gyro_x_delta) + (K1 * rot_x)
            last_y = K * (last_y + gyro_y_delta) + (K1 * rot_y)
            last_z = K * (last_z + gyro_z_delta) + (K1 * rot_z)
    
            roll_list.append(last_x)
            pitch_list.append(last_y)
            yaw_list.append(last_z)

        Write_Output()

        plt.title('Complementary Filter')
        #plt.plot(roll_list, 'g', label = 'Roll')
        #plt.plot(pitch_list, 'b', label = 'Pitch')
        plt.plot(yaw_list, 'r', label = 'yaw')
        plt.legend(loc='upper left')
        plt.show()

        print ()
        print ("*************************************************")
        print ("    Task Finished, Check for output files.       ")
        print ("*************************************************")
        print ()
        
    except:
        print ()
        print ("*************************************************")
        print ("                   Error!                        ")
        print ("*************************************************")
        print (traceback.format_exc())
    
# Must specify filepath!
else:
    print("Please specify a filepath that contains data!")

