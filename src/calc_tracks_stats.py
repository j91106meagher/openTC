from trackset_class import track_set
from latlon_grid_class import latlon_grid


dt = 30.0 #180.0 #in min
latd = 0.1 #degress
lond = 0.1 #degrees
latur = 90.0
latll = -90.0
lonur = 180.0
lonll = -180.0

Lgenesis = 210*1000 #length scale in meters
Ltrack = 210*1000



if True:
    
   
    outpath= '../data/grid_stats/'
    data_path = '../data/'
    track_fn = 'hurdat2.txt'
    #http://www.aoml.noaa.gov/hrd/hurdat/hurdat2.html
    #w3m -dump http://www.aoml.noaa.gov/hrd/hurdat/hurdat2.html > hurdat2.txt
    
    trackset = 'HURDAT'
    #trackset = 'EBTRK'
    debug = False
    print('starting',trackset)

    latur = 51.0
    latll = 5.0
    lonur = -10.0
    lonll = -110.0
    
    year1 = 1851
    year2 = 2017
    
    wg = latlon_grid()
    wg.alloc_grid(latur, latll, lonur, lonll, latd, lond)
    
    ts = track_set()
    if trackset == 'EBTRK':
        ts.read_track_set_ebtrk(track_fn,data_path)
        #ts.proc_tracks_ebtrk(dt, wg, outpath)
    elif (trackset == 'HURDAT'):
        print('read hurdat')
        ts.read_hurdat_set(track_fn, data_path, debug)
        ##ts.proc_tracks_hurdat(dt, wg, outpath,year1,year2)
        ts.prep_tracks(False)
        
        ts.genesis_kernel(wg,year1,year2,Lgenesis,debug = True)
        wg.save_genesismodel(data_path,'genesis_model.npz')
        
        #ts.latlon_kernel(wg,year1,year2,Ltrack,debug=True)
        #wg.save_cyclonemodel(data_path,'latlon_kernel_model.npz')
        
    
    print('len track_set',len(ts.tracks))
    
    
    
    print('Finished')