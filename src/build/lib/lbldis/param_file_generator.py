import numpy as np

def gen_param(file_name, wnum_start, wnum_end, opd=[1.0], ice_fraction=0, eff_rad_wat=2, eff_rad_ice=10):

    f = open(file_name, 'w')

    f.write('ice fraction %f\n' % (ice_fraction))
    f.write('16     Number of streams\n')
    f.write('-60. 30. 1.0   Solar zenith angle (deg), relative azimuth (deg), solar distance (a.u.)\n')
    f.write('180.\n')
    f.write("%s %s 0.01  v_start, v_end, and v_delta [cm-1]\n" % (wnum_start, wnum_end))
    
    f.write(str(len(opd)) + '               Cloud parameter option flag: 0: reff and numdens, >=1:  reff and tau\n')
    if ice_fraction == 0: #Water cloud
        f.write('1               Number of cloud layers\n')
        f.write('0 1.800  %d 1000. ' % (eff_rad_wat))
    elif ice_fraction == 1:  #Ice cloud
        f.write('1               Number of cloud layers\n')
        f.write('1 1.800  %d 1000. ' % (eff_rad_ice))
    else: #Mixed phase cloud
        f.write('2               Number of cloud layers\n')
        f.write('0 1.800  %d 1000. ' % (eff_rad_wat))
        for op in opd:
            f.write(str(op) + ' ')
        f.write('\n')

        f.write('1 1.800  %d 1000. ' % (eff_rad_ice))

    for op in opd:
        f.write(str(op) + ' ')
    f.write('\n')

    f.write('../aer_lblrtm_v12.9_lnfl_v3.2/lblrtm_v12.9/\n')
    f.write('./solar_src/solar.kurucz.rad.1cm-1binned.full_disk.asc\n')
    f.write('2  Number of scattering property databases\n')
    f.write('./SSP/ssp_db.mie_wat.gamma_sigma_0p100\n')
    f.write('./SSP/ssp_db.mie_ice.gamma_sigma_0p100\n')
    f.write('-270.  Surface temperature (specifying a negative value takes the value from profile)\n')
    f.write('4  Number of surface spectral emissivity lines (wnum, emis)\n')
    f.write('100  0.985\n')
    f.write('700  0.950\n')
    f.write('800  0.970\n')
    f.write('3000 0.985\n')


opd = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 6.0, 8.0]
wat_eff_rad = [2,3,5,7,10,15]
ice_eff_rad = [10,20,30,50,70,100]
microwindows = [("495.5","498"), ("529.9","531.5"), ("558.5","562"),("830","834.5"), ("843","847.5"), ("873.2","875.5"), ("898.5","904.7"), ("1095","1098.2"), ("1113.5","1116.1"), ("1231.3","1232.2")]
mixed_cloud_eff_rad = [(3,20), (3,30),(5,30),(7,20),(7,30),(10,40)]

#For each cloud phase (at various particle effective radii), perform 16 simulations at varying optical depths 
'''
for wat_rad in wat_eff_rad:
    for window in microwindows:
        gen_param('../../Models/lbldis/param_files/simulations/water/wat_%d_um_%s_%s' % (wat_rad, window[0], window[1]), window[0], window[1], opd, ice_fraction=0, eff_rad_wat = wat_rad)

for ice_rad in ice_eff_rad:
    for window in microwindows:
        gen_param('../../Models/lbldis/param_files/simulations/ice/ice_%d_um_%s_%s' % (ice_rad, window[0], window[1]), window[0], window[1], opd, ice_fraction=1, eff_rad_ice = ice_rad)
'''
for rad in mixed_cloud_eff_rad:
    for window in microwindows:
        gen_param('../../Models/lbldis/param_files/simulations/mixed/%d_wat_%d_ice_um_%s_%s' % (rad[0],rad[1], window[0], window[1]), window[0], window[1], opd, ice_fraction=0.5, eff_rad_ice=rad[1] ,eff_rad_wat=rad[0])

