import logging
import time
import atexit
from datetime import datetime

import psutil
import serial

# Set up log file and logging level
logging.basicConfig(filename='main.log', encoding='utf-8', level=logging.DEBUG)

# CPU monitor class
class CpuMon:
    def __init__(self, arduino):
        self.arduino = arduino
        # Testing stuff
        #self.i = 0

    # Clamp, in case the average value reading goes over 100 or something
    #forlater: maybe clamp below in run_code and log if it happened!?
    def clamp(self, n, minn, maxn):
        # Takes the smaller of the two values n and maxn, then picks the larger between it and minn
        return max(min(maxn, n), minn)

    # Translate ranges
    def translate(self, value, in_min, in_max, out_min, out_max):
        # Figure out how 'wide' each range is
        in_span = in_max - in_min
        out_span = out_max - out_min
        # Convert the in range into a 0-1 range (float)
        valueScaled = float(value - in_min) / float(in_span)
        # Convert the 0-1 range into a value in the out range.
        return out_min + (valueScaled * out_span)

    # Main code of the monitor object
    def run_code(self):
        # If needed - this one gets detailed usage details, per CPU (different times - usr, sys, idle, interrupt, dpc)
        #usages = [usage._asdict() for usage in psutil.cpu_times_percent(interval=1, percpu=True)]

        # Get CPU percentages, with 1 second of interval, per logical CPU. Order of CPUs is consistent as per psutil docs
        usages = psutil.cpu_percent(interval=1, percpu=True)
        # Calculate the average
        avg = sum(usages)/len(usages)
        # Print unpacked list and the average
        print(*usages, avg, sep="\n")
        # Clamp in case it goes out of bounds, though it shouldn't.
        out_val = self.clamp(avg, 0, 100)
        # Translate to the range the Arduino program can use, and cast to int while at it
        out_translated = int(self.translate(out_val, 0, 100, 0, 180))
        # Print output value
        print(out_translated)
        # Blank line for separation
        print()

        # Write the number via serial communication, converted into a string and then into a bytes object
        arduino.write(bytes(str(out_translated), "utf-8"))

        # Testing stuff
        #next_out = [150, 60, 120, 30, 180, 90, 0][self.i%7]
        #print(next_out)
        #arduino.write(bytes(str(next_out), "utf-8"))
        #self.i+=1

# Looping function, runs task ever delay seconds
def loop(delay, task):
    # Set next run time
    next_time = time.time() + delay
    while True:
        # Wait a time
        time.sleep(max(0, next_time - time.time()))
        # Try calling the task
        try:
            task()
        # If there's an exception, log it
        except Exception:
            logging.exception(f"An exception occurred in the monitor method!")
        # Skip a task if we're behind schedule
        next_time += (time.time() - next_time) // delay * delay + delay

# Set up for later, to avoid exceptions in exit handler
arduino = None

# Handler for when the program exits
#forlater: sys.excepthook instead?
@atexit.register
def exit_handler():
    # Log exit
    logging.info(f"Exited. {datetime.now().strftime('%y-%m-%d_%H:%M:%S')}")
    # Close the serial port
    global arduino
    # If it's been opened at all anyway
    if arduino is not None:
        arduino.close()


# Log this when testing!
#logging.info(f"Started testing! {datetime.now().strftime('%y-%m-%d_%H:%M:%S')}")
#print("TESTING PHASE! OUTPUTS PRE-DETERMINED NUMBERS!")

# Log start of program
logging.info(f"Started! {datetime.now().strftime('%y-%m-%d_%H:%M:%S')}")
try:
    # Open serial communication with the Arduino
    arduino = serial.Serial('COM7', 115200, timeout=0.1)
except Exception:
    logging.exception("A problem occurred during serial port setup! Check Arduino connection.")
    exit()
# Wait for the Arduino to reset due to serial port opening
time.sleep(1)
# Create object
monitor = CpuMon(arduino)
# Run the repeating function, giving it the monitor object method to call
try:
    loop(1.5, monitor.run_code)
except Exception:
    logging.exception("A problem occurred in the repeating function!")
    exit()
