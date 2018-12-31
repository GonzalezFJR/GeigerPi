from numpy import append, histogram, arange, average, exp
from math import factorial
import matplotlib.pyplot as plt

# Default values
path = 'test/'
fname = 'KCl'

class RadCounts:

  def SetPath(self, path):
    if not path.endswith('/'): path += '/'
    self.path = path
    
  def SetFileName(self, fname):
    if not fname.endswith('.txt'): fname += '.txt'
    self.fname = fname

  def SetOutDir(self, outdir):
    self.outdir = outdir

  def GetPath(self):
    return self.path

  def GetFileName(self):
    return self.fname

  def GetOutDir(self):
    return self.outdir

  def GetFile(self):
    return self.GetPath()+self.GetFileName()

  def GetValues(self):
    return self.listOfValues

  def ReadValues(self):
    ''' Store the time values from a .txt in a list '''
    f = open(self.GetFile())
    self.listOfValues = []
    if self.verbose >= 1: print 'Reading file: \"%s\"...'%self.GetFile()
    for l in f.read().splitlines():
      if l.startswith('#'): continue
      if l == '': continue
      if self.verbose >= 3: print 'Reading value: %1.2f'%float(l)
      self.listOfValues.append(float(l))
    
  def GetDifsVals(self):
    ''' Get the time differences between a count and the previous one ''' 
    vals = self.GetValues()
    valdif = []
    for i in range(len(vals)-1):
      valdif.append(vals[i+1]-vals[i])
    return valdif

  def GetBins(self, nbins, val = ''):
    ''' Compute the bin edges for a range of values and a given number of bins '''
    values = self.GetValues() if val == '' else val
    vmax = max(values)
    vmin = min(values)
    if nbins < 0: return range(int(vmin), int(vmax)+1)
    bins = arange(vmin, vmax, vmax/nbins)
    bins = append(bins,vmax)
    return bins #histogram(values, bins)

  def GetBinsWidth(self, width, val = ''):
    ''' Compute the bin edges for a range of values and a given bin width '''
    values = self.GetValues() if val == '' else val
    vmax = max(values)
    bins = arange(0, vmax, width)
    bins = append(bins, bins[-1]+width)
    return bins

  def GetCountsInNsecs(self, nsecs = 10):
    ''' Get the histogram of the number of counts per [nsec] seconds '''
    bins = self.GetBinsWidth(nsecs, self.GetValues())
    h = histogram(self.GetValues(), bins)[0]
    return h

  #############################################################################
  ### Drawing functions

  def DrawVals(self):
    ''' Draw an histogram for the times '''
    bins = self.GetBins(100, self.GetValues())
    plt.hist(self.GetValues(), bins=bins)
    plt.xlim(min(bins), max(bins))
    plt.show()
    plt.close()

  def DrawTimeDiffs(self, nbins = 100):
    ''' Draw an histogram for the time differences between consecutive counts '''
    difv = self.GetDifsVals()
    bins = self.GetBins(nbins, difv)
    plt.hist(difv, bins=bins)
    plt.xlim(min(bins), max(bins))
    plt.show()
    plt.close()

  def DrawCountHisto(self, nsec = 10, norm = False, DrawPoisson = False):
    ''' Draw an histogram for number of counts in [nsec] seconds '''
    c = self.GetCountsInNsecs(nsec)[:-1]
    bins = self.GetBins(-1, c)
    mean = average(c)
    if self.verbose >= 1:
      print '>> Calculating statistics of number of counts in %i seconds...'%nsec
      print '>> Average: ', mean
    plt.hist(c, bins=bins, normed = norm)
    plt.xlim(min(bins), max(bins))
    if DrawPoisson:
      num, val = GetPoisson(mean)
      plt.plot([x+0.5 for x in num], val, 'ro')
    plt.show()
    plt.close()

  #############################################################################
  def __init__(self, path = 'test', fname = 'KCl', outDir = './', display = True, verbose = 1):
    self.listOfValues = []
    self.SetPath(path)
    self.SetFileName(fname)
    self.SetOutDir(outDir)
    self.verbose = verbose
    self.display = display
    self.ReadValues()

def GetPoisson(L = 1):
  thr = 0.01
  f = lambda x : (exp(-L)*L**x)/factorial(x)
  pos = 1;
  val = []; num = []
  for n in range(int(L)):
    pos = f(n)
    if pos > thr:
      val.append(pos)
      num.append(n)
  n = int(L); pos = 1
  while pos > 0.01:
    pos = f(n)
    val.append(pos)
    num.append(n)
    n+=1
  print num
  print val
  return num, val
  
#plt.show()
a = RadCounts('test','bkg_big')
#a.DrawVals()
#a.DrawTimeDiffs(nbins = 300)
a.DrawCountHisto(10,True,True)
