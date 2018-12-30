import RPi.GPIO as g
import os, sys, time, datetime

runName = ''
runTime = -1
runDesc = ''

def GetData(fname = 'data', pin = 4, deadtime = 0.003):
  # Create file
  #if not fname.endswith('.txt'): fname += '.txt'
  #if os.path.isfile(fname):
  #  os.rename(fname, fname+'.old')
  index = 0
  while os.path.isfile(fname+'_%i.txt'%index): index+=1
  fout = open(fname+'_%i.txt'%index,'w')
  time0 = time.time()
  fout.write('# '+datetime.datetime.utcfromtimestamp(time0).strftime('%Y-%m-%d %H:%M:%S')+'\n')

  # Set up
  g.setmode(g.BCM)
  g.setup(pin, g.IN, pull_up_down = g.PUD_DOWN)

  while 1:
    val = 0
    while not val: val = g.input(pin)
    time.sleep(deadtime)
    a=time.time()-time0
    print a
    fout.write(str(a)+'\n')

GetData()
