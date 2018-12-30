from numpy import append, histogram, arange
import matplotlib.pyplot as plt

path = 'dataCounts/'
fname = 'bolsita'

def readValues(path = './', fname = 'data'):
  if not path.endswith('/'): path += '/'
  if not fname.endswith('.txt'): fname += '.txt'
  f = open(path + fname)
  listOfValues = []
  for l in f.read().splitlines():
    if l.startswith('#'): continue
    if l == '': continue
    listOfValues.append(float(l))
  return listOfValues

def GetDifsVals(vals):
  valdif = []
  for i in range(len(vals)-1):
    valdif.append(vals[i+1]-vals[i])
  return valdif

def GetBins(values, nbins):
  vmax = max(values)
  vmin = min(values)
  bins = arange(vmin, vmax, vmax/nbins)
  bins = append(bins,vmax)
  return bins #histogram(values, bins)

def GetBinsWidth(values, width):
  vmax = max(values)
  bins = arange(0, vmax, width)
  bins = append(bins, bins[-1]+width)
  return bins

def GetCountsInNsecs(vals, nsecs = 10):
  bins = GetBinsWidth(vals, nsecs)
  h = histogram(vals, bins)[0]
  return h



val = readValues(path, fname)
c = GetCountsInNsecs(val)[:-1]
bins = GetBins(c, 40)

plt.hist(c, bins=bins)
plt.xlim(min(bins), max(bins))
plt.show()
'''
val = readValues(path, fname)
difv = GetDifsVals(val)
bins = GetBins(difv, 100)
print bins

plt.hist(difv, bins=bins)
plt.xlim(min(bins), max(bins))
plt.show()
'''
