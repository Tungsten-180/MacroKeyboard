import typing
import os

import evdev
from evdev import ecodes

#############################################Imports^

if os.getuid() != 0:
  print("You aren't root, retry with sudo")
  os._exit(0)
##Exit if not sudo^^

device_to_bind:str = "Logitech Wireless Keyboard PID:4023"
#device for script to capture

#Setup code
#################################################################################

found_keyboard:bool = False


while found_keyboard==False: ###finds user set device
  devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
  devicepath = ""
  for device in devices:
    if device.name == device_to_bind:
      found_keyboard = True
      os.system("echo Found Keyboard on {}".format(device.path))
      devicepath = device.path
      break
  if found_keyboard == False:
    os.system("echo Couldn't find device!")



device = evdev.InputDevice(devicepath)#grabs device
device.grab()#device level input


def run(device)->None:
    for event in device.read_loop():
      if event.type == ecodes.EV_KEY:
          keyEvent = evdev.categorize(event)
          if keyEvent.keystate == keyEvent.key_down:
              try:
                  keybind[keyEvent.keycode](True)
              except Exception as e:
                  # os.system("echo {}".format(e)) 
                  os.system("echo {} is not bound".format(keyEvent.keycode))

#above gets keyboards setup
###############################################################################
#configure and modify below

##define functions that cant be lamda below
def push(key:int)->None:
  with evdev.uinput.UInput() as ui:
          ui.write(ecodes.EV_KEY, key, 1)
          ui.syn()

def push_combo(keys:list[int])->None:
  with evdev.uinput.UInput() as ui:
    for k in keys:
      ui.write(ecodes.EV_KEY, k, 1)
    keys.reverse()
    for k in keys:
      ui.write(ecodes.EV_KEY, k, 0)
    ui.syn()





##Example keymap below(esc quits, numpad is passed through as if numlock is on)
keybind = {
  "KEY_ESC":lambda x: os._exit(0),
  #########################################  KEYPAD
  "KEY_KP1":lambda x: push(ecodes.KEY_1),
  "KEY_KP2":lambda x: push(ecodes.KEY_2),
  "KEY_KP3":lambda x: push(ecodes.KEY_3),
  "KEY_KP4":lambda x: push(ecodes.KEY_4),
  "KEY_KP5":lambda x: push(ecodes.KEY_5),
  "KEY_KP6":lambda x: push(ecodes.KEY_6),
  "KEY_KP7":lambda x: push(ecodes.KEY_7),
  "KEY_KP8":lambda x: push(ecodes.KEY_8),
  "KEY_KP9":lambda x: push(ecodes.KEY_9),
  "KEY_KP0":lambda x: push(ecodes.KEY_0),
  "KEY_KPENTER":lambda x: push(ecodes.KEY_KPENTER),
  "KEY_KPDOT":lambda x: push(ecodes.KEY_KPDOT),
  "KEY_KPPLUS":lambda x: push(ecodes.KEY_KPPLUS),
  "KEY_KPMINUS":lambda x: push(ecodes.KEY_KPMINUS),
  "KEY_KPSLASH":lambda x: push(ecodes.KEY_KPSLASH),
  "KEY_KPASTERISK":lambda x: push(ecodes.KEY_KPASTERISK),
  ########################################################  KEYPAD
   
  }



run(device)
