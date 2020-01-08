class Tranponder:
    def __init__(self):
        self.id = 0
        self.bitrate = 0
        self.costs = {}
        self.osnr = 0
        self.band = 0
        self.slice_width = 0
        self.slices = []

    def __repr__(self):
        return "\nTransponderid:"+str(self.id)+"\nbitrate:"+str(self.bitrate)+"\ncosts"+str(self.costs)+"\nosnr:"+str(self.osnr)+"\nband"+str(self.band)+"\nslice width:"+str(self.slice_width)+"\nslices:"+str(self.slices)

    def __str__(self):
        return "\nTransponderid:"+str(self.id)+"\nbitrate:"+str(self.bitrate)+"\ncosts"+str(self.costs)+"\nosnr:"+str(self.osnr)+"\nband"+str(self.band)+"\nslice width:"+str(self.slice_width)+"\nslices:"+str(self.slices)
