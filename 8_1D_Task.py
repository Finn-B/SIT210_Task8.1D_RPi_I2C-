
import time
import smbus
import random


# LCD SCREEN DEFINITIONS 
bus = smbus.SMBus(1)
adr = 0x31
Set_row = 4
Set_col = 20

################################################
# FUNCTIONS
################################################

# SENDS TEXT TO I2C BUS.
def Send(data):
    for a in range(0, len(data)):
        bus.write_byte(adr, ord(data[a]))


# LCD COMMANDS. NOTE ALL COMMANDS ARE PRECEEEDED BY ESCAPE
def Cmd(command):
    bus.write_byte(adr, 27)
    bus.write_byte(adr, command)
    time.sleep(0.05)


# MOVES CURSER TO POSITION (ROW, COLUMN)
def CursorRC(row, col):
    Cmd(0x24)
    bus.write_byte(adr, row)
    bus.write_byte(adr, col)


# SETS THE SCREEN BOUNDARIES IN TERMS OF NUMBER OF ROWS AND COLUMNS. STARTS AT 1
def setrc(row, col):
    Cmd(0x30)
    bus.write_byte(adr, row)
    Cmd(0x31)
    bus.write_byte(adr, col)


#UPDATES THE DUTY CYCLE AND DISTANCE PARAMETERS ON LCD
def display(dc, dis):
    CursorRC(2, 1)  # Go to row 2 column 1
    Cmd(0x53)  # clear line
    Send(dc)  # Send Duty Cycle to lcd
    CursorRC(3, 1)  # Go to row 3 column 1
    Cmd(0x53)  # clear line
    Send(dis)  # Send Distance to lcd

# SETUP

setrc(Set_row, Set_col)  # SET LCD SIZE ROW AND COLUMNS

Cmd(0x50)  # clear screen
CursorRC(1, 1)  # Go to row 1 column 1
Send('-----------')  # Send characters to lcd
CursorRC(4, 1)  # Go to row 4 column 1
Send('-----------')  # Send characters to lcd

# MAIN LOOP

try:
    
    while 1:
        dc = "Duty Cycle: " + str(random.randrange(0, 100, 1)) + " %"  # generates the string package for duty cycle which includes the random number between 0 - 100.
        dist = "Dist: " + str(random.randrange(0, 30, 1)) + " cm"  # generates the string package for distance which includes the random number between 0 - 30.
        display(dc, dist)  # calls display to update duty cycle and distance values on lcd.
        
        print("-----------")  # prints the duty cycle and distance values.
        print(dc)
        print(dist)
        print("-----------")
        
        time.sleep(0.5)
        
except KeyboardInterrupt:
    GPIO.cleanup()
