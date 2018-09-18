from latlon_grid_class import latlon_grid
from trackset_class import track_set

wg = latlon_grid()

dt = 30.0 #180.0 #in min
latd = 0.1 #degress
lond = 0.1 #degrees

#latur = 90.0
#latll = -90.0
#lonur = 180.0
#lonll = -180.0

latur = 50.0
latll = 0.0
lonur = 0.0
lonll = -120.0

wg.alloc_grid(latur, latll, lonur, lonll, latd, lond)

data_path = '../data/'
outpath = '../wind_footprints/'
track_fn = 'ebtrk_atlc_1988_2017.txt'

ts = track_set()
ts.read_track_set_ebtrk(track_fn,data_path)
ts.proc_tracks_ebtrk(dt, wg, outpath,400)

print('len tracks',len(ts.tracks))

wg.plot_vst_max()


print ('Finished')

