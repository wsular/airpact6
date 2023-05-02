def namelist(self, day):
    if day == 'day1':
        wrf_start  = 7
        wrf_end    = 33
        day_offset = 0
        outdir     = self.outDay1
    elif day == 'day2':
        wrf_start  = 31
        wrf_end    = 57
        day_offset = 1
        outdir     = self.outDay2
    elif day == 'day3':
        wrf_start  = 55
        wrf_end    = 81
        day_offset = 2
        outdir     = self.outDay3
    else:
        print('Incorrect day for creating namelist.')
        exit
    
    # ....Create output directory, if it doesn't already exist.
    if not os.path.exists(outdir + self.datestr):
        os.mkdir(outdir + self.datestr)
    
    
    ###################################### Create environment variable file #############################
    f = open(outdir + self.datestr + '/env.mcip')
    f.write('')
    f.close()
    
    ###################################### Create namelist.mcip #########################################
    # ....Sets all the variables
    # &FILENAMES
    filegd         = outdir + self.datestr + '/GRIDDESC'
    filemm         = [self.WRF + self.datestr + '/wrfout_d3.' + self.datestr + '.f' + str(fnum).zfill(2) + '.0000' for fnum in range(wrf_start, wrf_end+1)]
    ioform         = 1
    
    # &USERDEFS
    lpv            = 0
    lwout          = 1
    luvbout        = 1
    mcip_start     = (self.day1 + timedelta(days=day_offset)).strftime('%Y-%m-%d-%H:%M:%S.0000')
    mcip_end       = (self.day1 + timedelta(days=day_offset+1)).strftime('%Y-%m-%d-%H:%M:%S.0000')
    intvl          = 60
    coordnam       = "LAM_49N121W"
    grdnam         = "AIRPACT_04km"
    btrim          =  -1
    lprt_col       =  0
    lprt_row       =  0
    wrf_lc_ref_lat = 49.000
    
    # &WINDOWDEFS
    x0             = 78
    y0             = 3
    ncolsin        = 285
    nrowsin        = 258
    
    # ....Prints the variables to a namelist file.
    f = open(outdir + self.datestr + '/namelist.mcip', 'x')
                
    f.write(' &FILENAMES' + '\n')
    f.write('  file_gd    = "' + filegd + '"\n')
    f.write('  file_mm    = "')
    for i, fn in enumerate(filemm):
        if i ==0:     # first time through loop
            f.write(fn + '",' + '\n')
        else:
            f.write('               "' + fn + '",' + '\n')
    f.write('  ioform    = ' + str(ioform) + '\n')
    f.write(' &END' +  '\n\n')
    
    f.write(' &USERDEFS' + '\n')
    f.write('  lpv        = ' + str(lpv) + '\n')
    f.write('  lwout      = ' + str(lwout) + '\n')
    f.write('  luvbout    = ' + str(luvbout) + '\n')
    f.write('  mcip_start = "' + mcip_start + '"\n')
    f.write('  mcip_end   = "' + mcip_end + '"\n')
    f.write('  intvl      = ' + str(intvl) + '\n')
    f.write('  coordnam   = "' + str(coordnam) + '"\n')
    f.write('  grdnam     = "' + str(grdnam) + '"\n')
    f.write('  btrim      = ' + str(btrim) + '\n')
    f.write('  lprt_col   = ' + str(lprt_col) + '\n')
    f.write('  lprt_row   = ' + str(lprt_row) + '\n')
    f.write('  wrf_lc_ref_lat = ' + str(wrf_lc_ref_lat) + '\n')
    f.write(' &END' +  '\n\n')

    f.write(' &WINDOWDEFS' + '\n')
    f.write('  x0         = ' + str(x0) + '\n')
    f.write('  y0         = ' + str(y0) + '\n')
    f.write('  ncolsin    = ' + str(ncolsin) + '\n')
    f.write('  nrowsin    = ' + str(nrowsin) + '\n')
    f.write(' &END' +  '\n\n')
    
    f.close()
    
    return
