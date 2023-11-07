import time
import sys
import os
from win10toast import ToastNotifier
import keyboard
from threading import Thread


paused = False
# Blocks are in minutes, alternating between work and break.
blocks = [25, 5, 25, 5, 25, 5, 25, 15, 25, 5, 25, 30, 25, 5, 25, 15]

# Converts minutes to hours and minutes.
def intToTime(i):
    return str(int(i/60)) + " hours, " + str(i % 60) + " minutes."

def timer(startPoint):
    pauseTime = 0
    blockStr = "." * int(startPoint / 2)
    
    # using the time blocks assigned as the global variable blocks, iterate through each block and count down from the time in the block. If a start point is specified, start from that block.
    # the global variable paused, which is modified by the pauseAndStop thread, is used to pause the timer.
    # timer uses sys.stdout.write() to write to the same line, and sys.stdout.flush() to flush the buffer.
    for i in blocks if startPoint == 0 else blocks[startPoint:]:
        for remaining in range(i * 60, 0, -1):
            while paused:
                time.sleep(1)
            sys.stdout.write("\r")
            sys.stdout.write("{:02d}:{:02d} remaining.".format(int(remaining/60), remaining % 60))
            if(blocks.index(i) % 2 == 0):
                sys.stdout.write(" Work!     " + blockStr + "                       ")
                
            else:
                sys.stdout.write(" Break!" + blockStr + "                       ")
            sys.stdout.flush()
            time.sleep(1)
            
        # When the timer reaches 0, a notification is sent to the user. If the block is a work block, the notification will be to take a break. If the block is a break block, the notification will be to get back to work.
        toaster = ToastNotifier()
        if(blocks.index(i) % 2 == 0):
            toaster.show_toast("Time to take a break!", "You've been working for " + str(i) + " minutes. Take a break for " + str(blocks[blocks.index(i) + 1]) + " minutes!", duration=5, icon_path="C:\\Users\\lordo\Downloads\\timer_icon_153935.ico")
            blockStr += "."
        else:
            toaster.show_toast("Time to get back to work!", "You've been on break for " + str(i) + " minutes. Get back to work for " + str(blocks[blocks.index(i) + 1]) + " minutes!", duration=5)
    sys.stdout.write("\nYou finished a block of " + intToTime(sum(blocks)) + " Good job!")

# a function ran in a thread that pauses the timer when ctrl+alt+s is pressed, and stops the timer when ctrl+alt+q is pressed.
# uses the keyboard module to detect key presses.
def pauseAndStop():
    global paused
    while True:
        if keyboard.is_pressed("ctrl+alt+s"):
            paused = not paused
            sys.stdout.flush()
            if paused:
                sys.stdout.write("\rPaused. Press ctrl+alt+s to unpause.")
            time.sleep(3)        
        if keyboard.is_pressed("ctrl+alt+q"):
            os._exit(0)

# Prints the total time, work time, and break time.
print("\nTotal time: " + intToTime(sum(blocks)))
print("Total work time: " + intToTime(sum(blocks[::2])))
print("Total break time: " + intToTime(sum(blocks[1::2])))

startPoint = 0
if len(sys.argv) > 1:
    if sys.argv[1] == "-s":
        startPoint = int(input("\nStart point: "))


mode = input("\nRepeat? (y/n): ")
if(mode == "y"):
    mode = True
    blocks.append(5)
else:
    mode = False
    
pauseThread = Thread(target = pauseAndStop).start()
timer(startPoint)
while mode:
    timer(startPoint)