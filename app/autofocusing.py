import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from scipy.io import loadmat

def load_mat(filepath):
    holo = loadmat(filepath)
    return holo

def crop_center(img,cropx,cropy):
    y,x = img.shape
    startx = x//2-(cropx//2)
    starty = y//2-(cropy//2)    
    return img[starty:starty+cropy,startx:startx+cropx]

def reconstruct(data, wave_len=None, pitch=None, z=[0]):    
    M, N = data.shape

    F = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(data)))
    B = np.log(np.abs(F))
    plt.imshow(B)
    plt.show()
    F = crop_center(B, 800, 800)
    
    #reconstruc parameters
    zo = z
    wave_len = wave_len
    k = int(2*np.pi/wave_len)
    dx = pitch
    print("Pitch: {}, Lambda: {}, k: {}, z:{}".format(dx, wave_len, k, zo))
    
    Y2, X2 = F.shape
    dy2 = round((M-Y2)/2)
    dx2 = round((N-X2)/2)
    
    cut = np.zeros((Y2+2*dy2, X2+2*dx2), dtype=complex)
    cut[dy2:Y2+dy2, dx2:X2+dx2] = F[:Y2, :X2]
    
    fex = int(1/dx)
    fey = fex
    
    fx = np.linspace(-N/(2*dx*N), N/(2*dx*N), N, endpoint=False)
    fy = np.linspace(-M/(2*dx*M), M/(2*dx*M), M, endpoint=False)  
    
    freq = np.fft.fftfreq(N, dx)
    print(freq)
    
    FX, FY = np.meshgrid(fx, fy)
    d = cut.copy()

    root = 1./(wave_len**2) - (FX)**2 - (FY)**2
    #root *= (root >= 0)
    U = []
    
    for i in range(len(zo)):
        e = np.exp(2 * np.pi * 1j * zo[i] * np.square(root))
        #e = e * (root >= 0)
        G = d * e        
        H = np.fft.fftshift(np.fft.ifft2(np.fft.fftshift(G)))
        U.append(H)
    best_focus = autofocusing(U)
    return cut, U[0]    

def autofocusing(U):
    tc = []
    for u in U:
        value = np.abs(u)
        tamura = np.sqrt(np.std(value)/np.mean(value))
        tc.append(tamura)   
    best_focus = np.where(tc==np.max(np.max(tc)))
    best_focus = np.squeeze(best_focus)
    return best_focus
    

def create_metadata(data, wave_len, pitch):
    if wave_len.ndim > 1:
        wave_len = np.squeeze(wave_len)
    
    if pitch.ndim > 1:
        pitch = np.squeeze(pitch)
    
    coord_x = np.arange(data.shape[0])
    coord_y = np.arange(data.shape[1])
    holo = xr.DataArray(data, coords=[coord_x, coord_y], dims=['x', 'y'])
    holo.attrs['wave_len'] = wave_len
    holo.attrs['pitch'] = pitch
    return holo

mat_file = loadmat('static/saved_holograms/Hol_2D_dice.mat')
holo = create_metadata(mat_file['Hol'], mat_file['wlen'], mat_file['pitch'])

wave_len = holo.attrs['wave_len']
pitch = holo.attrs['pitch']
zo = np.arange(-1.5,1.5,0.1)
spectrum, holo_reconstructed = reconstruct(holo.data, wave_len=wave_len, pitch=pitch, z=[-0.5])

plt.imshow(np.abs(holo_reconstructed))
plt.show()

    
    
    
