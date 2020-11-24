import numpy as np
import xarray as xr
import warnings
import itertools


class Hologram:
    def __init__(self, experiment=None, data=None, wave_len=None, pitch=None):
        self.experiment = experiment
        self.data = data
        self.wave_len = wave_len
        self.pitch = pitch
        self.dataArray = None
        
        if data is not None:
            self.create_metadata()


    def create_metadata(self):
        coord_x = None
        coord_y = None
        data_ = []
        
        holo = xr.DataArray(self.data)
        
        if self.wave_len is not None:
            if self.wave_len.ndim > 1:
                self.wave_len = np.squeeze(wave_len)

        if self.pitch is not None:
            if self.pitch.ndim > 1:
                self.pitch = np.squeeze(pitch)

        if self.data is not None:
            data_ = self.data
            coord_x = np.arange(data_.shape[0])
            coord_y = np.arange(data_.shape[1])
            holo = xr.DataArray(data_, coords=[coord_x, coord_y], dims=['x', 'y'])
        
        holo.attrs['wave_len'] = self.wave_len
        holo.attrs['pitch'] = self.pitch
        holo.attrs['experiment'] = self.experiment
        self.dataArray = holo
        
    def update_data(self, data):
        coord_x = np.arange(data.shape[0])
        coord_y = np.arange(data.shape[1])
        out = xr.DataArray(data, coords=[coord_x, coord_y], dims=['x','y'])
        out.attrs['wave_len'] = self.wave_len
        out.attrs['pitch'] = self.pitch
        out.attrs['experiment'] = self.experiment
        self.dataArray = out
    
    def update_attrs(self, attrslist):
        out = self.dataArray.copy()
        for key, val in attrslist.items():
            if val is not None:
                self.dataArray.attrs[key] = val
                
        for attr in attrslist:
            if not hasattr(self.dataArray, attr):
                self.dataArray.attrs[attr] = None
        
        
    def set_wavelen(self, wave_len):
        self.dataArray.attrs['wave_len'] = wave_len
        
    def set_pitch(self, pitch):
        self.dataArray.attrs['pitch'] = pitch
        
    def set_experiment(self, experiment):
        self.dataArray.attrs['experiment'] = experiment