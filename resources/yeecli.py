import logging
import sys
import time
from yeelight import *

def hex_color_to_rgb(color):
	"Convert a hex color string to an RGB tuple."
	color = color.strip("#")
	try:
		red, green, blue = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
	except:
		red, green, blue = (255, 0, 0)
	return red, green, blue

bulb = Bulb(sys.argv[1], 55443, 'smooth', 500, True)

DICT_MAPPING = {'sleep' : SleepTransition,\
	'HSV' : HSVTransition, \
	'RGB' : RGBTransition, \
	'TEMP' : TemperatureTransition, \
	}

if sys.argv[2] == 'brightness':
	bulb.set_brightness(sys.argv[3])
elif sys.argv[2] == 'temperature':
	bulb.set_color_temp(sys.argv[3])
elif sys.argv[2] == 'hsv':
	bulb.set_hsv(sys.argv[3], sys.argv[4])
elif sys.argv[2] == 'flow':
	translist = sys.argv[5].split(';')
	list =[]
	for transition in translist:
		elements = transition.split(',')
		if elements[0] in DICT_MAPPING:
			effect = DICT_MAPPING(elements[0])
			if elements[0] == 'hsv':
				list.append(effect(arglist[1],arglist[2],arglist[3],arglist[4]))
			elif elements[0] == 'rgb' :
				list.append(effect(arglist[1],arglist[2],arglist[3],arglist[4],arglist[5]))
			elif elements[0] == 'temp' :
				list.append(effect(arglist[1],arglist[2],arglist[3]))
			else:
				list.append(effect(arglist[1]))
		else:
			print "Not an effect"
	flow = Flow(int(sys.argv[3]),Flow.actions.off,list)
	bulb.start_flow(flow)
elif sys.argv[2] == 'rgb':
	red, green, blue = hex_color_to_rgb(sys.argv[3])
	bulb.set_rgb(red, green, blue)
elif sys.argv[2] == 'toggle':
	bulb.toggle()
elif sys.argv[2] == 'cron':
	bulb.cron_add(enums.CronType.off, sys.argv[3])
elif sys.argv[2] == 'turn':
	if sys.argv[3] == 'on':
		bulb.turn_on()
	elif sys.argv[3] == 'off':
		bulb.turn_off()
elif sys.argv[2] == 'stop':
	bulb.stop_flow()
else:
	print bulb.get_properties()
