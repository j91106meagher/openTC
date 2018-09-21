
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
        
        self.ny = []
        self.nx = []
        
        self.track_start_prob = []
        self.track_stop_prob = []
        self.track_start_vst_max_count = []
        self.track_start_vst_max_sumx = []
        self.track_start_vst_max_sumx2 = []
        self.pdist = []
        self.pdlat = []
        self.pdlon = []
        self.pdlat2 = []
        self.pdlon2 = []
        
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
        
        self.track_start_prob = np.zeros((self.latv.shape))
        self.track_stop_prob = np.zeros((self.latv.shape)) 
        self.track_start_vst_max_count = np.zeros((self.latv.shape))
        self.track_start_vst_max_sumx = np.zeros((self.latv.shape))
        self.track_start_vst_max_sumx2 = np.zeros((self.latv.shape))
        
        self.ny = self.latv.shape[0]
        self.nx = self.latv.shape[1]
        
        self.pdist = np.zeros((self.latv.shape))
        self.pdlat = np.zeros((self.latv.shape))
        self.pdlon = np.zeros((self.latv.shape))
        self.pdlat2 = np.zeros((self.latv.shape))
        self.pdlon2 = np.zeros((self.latv.shape))
        
        
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
        
    def save_genesismodel(self,data_path,fn):
        print('saving ',fn)
        print('to ',data_path)
        np.savez(data_path+fn,track_start_prob=self.track_start_prob)
        
    def load_genesismodel(self,data_path,fn):
        npz = np.load(data_path+fn)
        print(npz.files)
        self.track_start_prob = npz['track_start_prob']
        
    def plot_genesismodel(self):
        
        import matplotlib.pyplot as plt 
        #plt.subplot(221)
        plt.pcolormesh(self.lonv,self.latv,self.track_start_prob)
        plt.title('genesis prob')
        plt.colorbar()
        plt.show()
    
    def save_cyclonemodel(self,data_path,fn):
        #fn2 = fn.split('.')[0]
        print('saving ',fn)
        print('to ',data_path)
        np.savez(data_path+fn,pdist=self.pdist,pdlat=self.pdlat,pdlon=self.pdlon,pdlat2=self.pdlat2,pdlon2=self.pdlon2)
        
        
        
        
    