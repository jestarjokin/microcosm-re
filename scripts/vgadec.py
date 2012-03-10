def paletteVGA2RGB(val):
    return val << 2 # VGA palette only uses the lower six bits (64 possible colours)

def readGFX(fname, maxpos, hasPalette=False):
    infile = file(fname, 'rb')
    outfile = file(fname + '.raw', 'wb')
    
    # Most GFX files store an entire VGA palette.
    if hasPalette:
        palfile = file(fname + '.act', 'wb')
        for i in xrange(768):
            val = paletteVGA2RGB(ord(infile.read(1)))
            palfile.write(chr(val))
        palfile.close()
    
    while True:
        runlength = ord(infile.read(1))
        
        if runlength == 0xFF:
            break
        
        useRLE = runlength & 0x80
        runlength &= 0x7F
        
        endpos = outfile.tell() + runlength
            
        if endpos >= maxpos:
            runlength -= endpos
            if runlength == 0:
                break
        
        if useRLE:
            val = infile.read(1)
            for i in xrange(runlength):
                outfile.write(val)
        else:
            for i in xrange(runlength):
                val = infile.read(1)
                outfile.write(val)  
    
    # Almost all background GFX are 1 pixel too short. I think the game just fills in
    # any missing info with 0x00. You can confirm yourself; take a screenshot
    # of the normal playing screen, zoom into the very bottom right corner; the
    # last pixel is black when all around is a dark pale green.
    # This is a loop because some image files are missing quite a few pixels.
    while (outfile.tell() < maxpos):
        outfile.write("\x00")
    outfile.close()
    
    
def __main():
    gfxList = [
        ("AERIAL.GFX", 0xFA00, True),
        ("AUTUMN.GFX", 0xFA00, True),
        ("CREDITS.GFX", 0xFA00, True),
        ("CUBES0.GFX", 0xF000, False),
        ("CUBES1.GFX", 0xF000, False),
        ("CUBES2.GFX", 0xF000, False),
        ("CUBES3.GFX", 0xF000, False),
        ("DYING.GFX", 0xFA00, True),
        ("FIRE.GFX", 0xFA00, True),
        ("GALLOWS.GFX", 0xFA00, True), 
        ("IDEOGRAM.VGA", 0x6400, False),
        ("ISOCHARS.VGA", 0x1000, False),
        ("MEN.VGA", 0xF000, False),
        ("MEN2.VGA", 0xF000, False),
        ("PAUSE.GFX", 0xFA00, True),
        ("SCREEN.GFX", 0xFA00, True),
        ("SOUL.GFX", 0xFA00, True),
        ("SPRING.GFX", 0xFA00, True),
        ("SUMMER.GFX", 0xFA00, True),
        ("TITLE.GFX", 0xFA00, True),
        ("WINTER.GFX", 0xFA00, True),
        ("WIZARD.GFX", 0xFA00, True),
        ("WON1.GFX", 0xFA00, True),
        ("WON2.GFX", 0xFA00, True)
    ]
    # Rome
    #gfxList = [("PANIC.GFX", 0xFA00, True)]
    for name, maxRun, hasPal in gfxList:
        print("Decoding " + name + "...")
        readGFX(name, maxRun, hasPal)
    print("Done!")
    
if __name__ == "__main__": __main()