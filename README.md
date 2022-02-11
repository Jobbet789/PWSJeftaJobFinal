# PWS of Jefta and Job
Concept version of our PWS

## Contents


- [Requirements](#requirements)
- [Installation](#installation)
- [Hardware](#hardware)
- [Usage](#usage)



## Requirements
- Computer with the latest version of [Python3.8](https://www.python.org/downloads/) or higher
- 2x [WeMos D1 R2](https://www.bol.com/nl/nl/p/wemos-d1-r2-wifi-esp8266-development-board-compatibel-arduino-uno-programma-door-arduino-ide/9200000116017778/?Referrer=ADVNLGOO002013-G-138543199184-S-1075852962178-9200000116017778&gclid=Cj0KCQiAr5iQBhCsARIsAPcwROMzQUkov30lUKaQSTbDEZgABVik9U553W_ns6QulxiIkrJTRPXwjSQaAi3TEALw_wcB)
- 2x [Motor shield](https://nl.grandado.com/products/l298p-motor-shield-motor-drive-voor-arduino-compatibel-met-uno-mega-256?gclid=CjwKCAiA24SPBhB0EiwAjBgkhgb7uzYczjT0Kvx0SfGvSmt7ct4MPyDWNJImiGT-Q5ktwBlaq8umiRoCEfUQAvD_BwE&variant=UHJvZHVjdFZhcmlhbnQ6NDU0MTk3MzE) 
- 2x [Servo motor](https://www.tinytronics.nl/shop/nl/mechanica-en-actuatoren/motoren/servomotoren/td-8120mg-waterproof-digitale-servo-20kg)
- 4x [Motor](https://www.kiwi-electronics.nl/nl/dc-gearbox-motor-tt-motor-200rpm-3-6vdc-10318?language=nl-nl&currency=EUR&gclid=Cj0KCQiAr5iQBhCsARIsAPcwROPnCIS8ol8ayMn3qshUK9gVBRy_SbpInvvR_BZx7rYig0o6aP3OE2saAr85EALw_wcB)
- 2x [Battery pack](https://www.hobbyelectronica.nl/product/batterij-houder-6-x-aa/?gclid=Cj0KCQiAr5iQBhCsARIsAPcwROPKzNZxP8BfrmwYaO6oMUnNCrLyMN9J8ABTJvmzMrMOTWpW5zCiGDEaAoRcEALw_wcB)
- [Jumper cables](https://nl.aliexpress.com/item/1005002000655439.html?spm=a2g0o.productlist.0.0.29c06265j3VcVQ&algo_pvid=e8816a17-b80a-4637-ad54-f4f6d744416c&aem_p4p_detail=202201140106084995587990540620008061504&algo_exp_id=e8816a17-b80a-4637-ad54-f4f6d744416c-1&pdp_ext_f=%7B%22sku_id%22%3A%2212000018371624182%22%7D&pdp_pi=-1%3B1.27%3B-1%3BEUR+1.45%40salePrice%3BEUR%3Bsearch-mainSearch)
- Lego Technic

**Note**: You don't need these specific parts, but make sure: 
- The motor shield fits on the esp8266 that you use.
- You can connect the battery to the esp8266, or the shield.
- You can connect the motor and servo motor to the shield or esp8266.

#### [Back to contents](#contents)


## Installation
Install the four libraries: socket, pygame, esptool and mpfshell

*Execute this below line by line in your terminal. (CMD for Windows)
```bash
pip install pygame
pip install esptool
pip install mpfshell
```

**If you have problems with the installation click the following links**
- [pygame](https://www.pygame.org/wiki/GettingStarted#Pygame%20Installation)
- [esptool](https://docs.espressif.com/projects/esptool/en/latest/esp32/installation.html#installation)
- [mpfshell](https://github.com/wendlers/mpfshell)

Add the SSID and password of your wifi network to [boot.py](WeMos_Files/boot.py), change the following variables.

```py
ssid = ""
passw = ""
```


**Note: Your computer and esp8266 need to be connected to the same WiFi network in order for this to work.**

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



#### Now, flash [Micropython](WeMos_Files/esp8266-20210902-v1.17.bin) on the esp8266.

First, erase the current flash.
If you are on Windows, you can check 'device manager' (probably `COM3 or COM4`), for Linux it's probably `/dev/ttyUSB0`.
```bash
esptool.py --port {port} erase_flash
```
Now, deploy the firmware.
```bash
esptool.py --port {port} --baud 460800 write_flash --flash_size=detect 0 esp8266-20210902-v1.17.bin
```

**If you have any problems with the installation, go to [esp8266 tutorial](https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html)**

After that, put the files: [main.py](WeMos_Files/main.py) & [boot.py](WeMos_Files/boot.py) on the esp8266.
You can use mpfshell for that.

"{port}" is the COM-port you saw in device manager on Windows and probably `ttyUSB0` on Linux
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


