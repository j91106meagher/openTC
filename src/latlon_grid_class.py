
import numpy as np

class latlon_grid:
    def __init__(self):
        self.val = []
        self.lat = []
        self.lon = []
        self.latv = []
        self.lonv = []
        self.latd = []
        self.lond = []
        
        self.latvrad = []
        self.lonvrad = []
        self.latll = []
        self.latur = []
        self.lonll = []
        self.lonur = []
        self.vs = []
        self.vst_max = []
        self.vst = []
        self.vst_maxa = []
        self.fn_list = []
        self.rpvst = []
        
    def alloc_grid(self,latur,latll,lonur,lonll,latd,lond):
        
        self.latll = latll
        self.latur = latur
        self.lonll = lonll
        self.lonur = lonur
        self.latd = latd
        self.lond = lond
        
        self.lat = np.arange(latll,latur+latd,latd)
        self.lon = np.arange(lonll,lonur+lond,lond)
        self.val = np.zeros((len(self.lat),len(self.lon)))
        self.latv, self.lonv = np.meshgrid(self.lat, self.lon)
        self.latvrad = np.deg2rad(self.latv)
        self.lonvrad = np.deg2rad(self.lonv)
        
        self.vs = np.zeros((self.latv.shape))
        self.vst_max = np.zeros((self.latv.shape))
        self.vst = np.zeros((self.latv.shape))
        
    def save_vst_max(self,data_path,fn):
        print('saving ',fn)
        np.save(data_path+fn,self.vst_max)
        
    def plot_vst_max(self):
        import matplotlib.pyplot as plt
        
        #plt.subplot(221)
        plt.pcolormesh(self.lonv,self.latv,self.vst_max)
        plt.colorbar()
        
        #plt.title('vst_max trk %d y %d'%(self.track,self.year)) 
            
            
        #plt.ion()
        plt.show()
        #plt.pause(2)
        #plt.close()
        
        
        
    