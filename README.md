# PWS of Jefta and Job
Concept version of our PWS

## Contents


- [Requirements](#requirements)
- [Installation](#installation)
- [Hardware](#hardware)
- [Usage](#usage)



## Requirements
- Computer with [python 3.10](http://fumacrom.com/3UIwz)
- 2x [WeMos D1 R2](http://fumacrom.com/3UIdT)
- [Logitech Extreme 3D Pro](http://fumacrom.com/3UId9)
- 2x [Motor shield](http://fumacrom.com/3UIcv) 
- 2x [Servo motor](https://bit.ly/33sM6AV)
- 4x [Motor](http://fumacrom.com/3UIko)
- 2x [Battery pack](http://fumacrom.com/3UIoP)
- [Jumper cables](http://fumacrom.com/3UIpQ)
- Lego Technic

#### [Back to contents](#contents)


## Installation
Install the four libraries: socket, pygame, esptool and mpfshell

```bash
pip install socket
pip install pygame
pip install esptool
pip install mpfshell
```

Add the SSID and password of your wifi network to [boot.py](WeMos_Files/boot.py), change the following variables.

```py
ssid = ""
passw = ""
```


**Note: Your computer and esp8266 need to be connected to the same WiFi network in order for this to work**

If you use another shield, change the pin numbers in [main.py](WeMos_Files/main.py) according to this table.

|Pin|Number|
|---|------|
|D0|16|
|D1|5|
|D2|4|
|D3|0|
|D4|2|
|D5|14|
|D6|12|
|D7|13|
|D8|15|
|RX|3|
|TX|1|



#### Now, flash [Micropython](WeMos_Flies/esp8266-20210902-v1.17.bin) on the esp8266.

First, uninstall the current flash.
If you are on Windows, the port is probably `COM3`, for Linux it's probably `/dev/ttyUSB0`
```bash
esptool.py --port {port} erase_flash
```
Now, deploy the firmware.
```bash
esptool.py --port {port} --baud 460800 write_flash --flash_size=detect 0 esp8266-20210902-v1.17.bin
```

After that, put the files: [main.py](WeMos_Files/main.py) & [boot.py](WeMos_Files/boot.py) on the esp8266.
You can use mpfshell for that.

"{port}" is probably `COM3` on Windows and `ttyUSB0` on Linux
Open the terminal in the folder where the files are located

Windows:
_Run CMD as administrator_
```bash
mpfshell
open {port}
put main.py
put boot.py
```

Linux:
```bash
sudo mpfshell
open {port}
put main.py
put boot.py
```

**Note: Do this on all two esp8266's**

#### [Back to contents](#contents)



## Hardware
### Single wheel
<img src="Images/Single_Wheel.jpeg" width="400">

### Empty frame
<img src="Images/Top_of_Car_Empty.jpeg" width="400">

### The wheels put together
<img src="Images/Front_of_Car.jpeg" width="400">

### How the WeMos' get connected
<img src="Images/WeMos_Focussed.jpeg" width="400">

1. Put the shield ontop of the WeMos and connect the jumper cables according to the following table.
2. Connect the brows wire of the servo to a ground pin, the middle one to a 5V pin and the other wire to the D3 pin.
3. Connect a batterypack to a shield or esp8266.
4. Connect two motors to a shield. _Connect the second motor the same way as the first motor._

**Note: If the motors go to the wrong direction, swap the black cable with the red cable.**



### Everything put together
<img src="Images/Top_of_Car.jpeg" width="400">

#### [Back to contents](#contents)


## Usage

1. Download [this file](Computer_Files/computerMainV3.py).
2. Execute the file while connected to a joystick.
3. Click the connect button.
4. Reset the esp8266's.

After that, you can control the car with the joystick.

#### [Back to contents](#contents)


