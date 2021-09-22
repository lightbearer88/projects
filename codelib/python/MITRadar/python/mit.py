# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 21:12:40 2021

@author: Ian Lam
@contact: ianlam3@cunet.carleton.ca

This module is for all the functions required to process the MIT 'Build Your
Own Radar' Cantenna project. This Python version was adapted from the original
MATLAB code.
"""

import scipy.io.wavfile as wav
import numpy as np
import scipy.signal as sg
import matplotlib.pyplot as plt

#Speed of light in m/s
c = 3e8 

def read_file(filename):
    """
    

    Parameters
    ----------
    filename : string
        String of input .wav file.

    Returns
    -------
    fs : int
        Sampling frequency in Hz.
    signal2 : array
        2D array

    """
    
    fs, signal = wav.read(filename)
    
    signal2 = signal/32767
    
    return fs, signal2

def sig_trig(signal_wav):
    trig = -1*signal_wav[:,0]
    s = -1*signal_wav[:,1]
    
    return s, trig

def read_trigger(trig, s, fs, N):
    """
    

    Parameters
    ----------
    trig : ndarray
        Real 1D array of triggered edges.
    s : ndarray
        Real 1D array of signals that triggered off trig.
    fs : int
        Sampling frequency in Hz.
    N : float
        Number of sampling points per pulse

    Returns
    -------
    sif : ndarray
        Reshaped 2D array with range bins as columns and sweeps as rows.
    time : ndarray
        Time stamps which mark the start of each triggered sweep.

    Notes
    -----
    Trigger off rising edge of sync pulse. Step through signals. 
    If trig > thresh and average of 11 signals before it has trig < thresh, 
    then trigger.

    """
    
    count = 0
    thresh = 0
    start = trig > thresh

    sif = []
    time = []
    t = np.arange(200,200+int(N),1)
    sif = np.zeros(len(t))

    for ii in np.arange(100,len(start)-int(N),1):
    
    # calculate mean of the chunck of start
    # defined by start[ii-11:ii], lower bound inclusive, upper bound exclusive
    # this part OK
        tmean = np.mean(start[ii-11:ii])
    
        if start[ii] == 1 and tmean ==0:
            count = count + 1
            # compared first instance when the if statement is true
            # with that of MATLAB and it matches.
            # this part should be OK
            sif = np.vstack([sif,s[ii:ii+int(N)]])
            time.append(ii*1/fs)
        
    sif = np.delete(sif, (0), axis=0)
    
    
    return sif, time

def subtract_dc(sif_in):
    """
    

    Parameters
    ----------
    sif_in : ndarray
        Reshaped 2D array with range bins as columns and sweeps as rows.

    Returns
    -------
    sif_out : ndarray
        sif_in but with the DC component subtracted away.

    """
    
    ave = np.mean(sif_in, axis=0)
    sif_out = sif_in - ave
    
    return sif_out

def hilbert_transform(sif_in):
    """
    
    Parameters
    ----------
    sif_in : ndarray
        Reshaped 2D array with range bins as columns and sweeps as rows.

    Returns
    -------
    sif_out : ndarray
        Complex-valued 2D array with range bins as columns and sweeps as rows.

    """
    
    sif_out = sg.hilbert(sif_in, axis=1)
    
    return sif_out

def read_data_RTI(file_in, pw, fstart, fstop, clutter=False):
    """
    

    Parameters
    ----------
    file_in : str
        Input .wav file.
    pw : double
        Pulse width [s].
    fstart : double
        Start frequency [Hz].
    fstop : double
        Stop frequency [Hz].

    Returns
    -------
    fig : Figure
        Figure containing the RTI plot.
    ax : axes.Axes
        Axes object of the RTI plot.
    
    Notes
    -----
    This function is adapted directly from the MATLAB code of the same name.
    RTI = Range-Time Intensity plot

    """
    fs, signal = read_file(file_in)
    
    N = pw * fs
    BW = fstop - fstart
    f = np.arange(fstart, fstop, N/2)
    rr = c/(2*BW)
    max_range = rr*N/2

    s, trig = sig_trig(signal)

    sif, time = read_trigger(trig, s, fs, N)

    sif_ave = subtract_dc(sif)
    
    zpad = 8*N/2
    
    #Does not matter if take fft or ifft
    v = 20*np.log10(np.abs(np.fft.ifft(sif_ave,n=int(zpad),axis=1)))
    #v = 20*np.log10(np.abs(np.fft.fft(sif_ave,n=int(zpad),axis=1)))
    
    v2 = v[: , 0 : int(v.shape[1]/2)]
    mv2 = np.amax(v2)
    
    range_bin = np.arange(0,v2.shape[1],1)
    range_m = np.linspace(0,max_range,v2.shape[1])
    
    fig, ax = plt.subplots()
    
    # Make RTI plot without clutter rejection
    if not clutter:
        
        cf = ax.pcolormesh(range_m, 
                           time, 
                           v2-mv2,
                           shading='gouraud',cmap='seismic',
                           vmin=-80, vmax=0)
        ax.set_title("RTI without clutter rejection")
        ax.set_xlabel("Range [m]")
        ax.set_ylabel("Time [s]")
        fig.colorbar(cf, ax=ax).set_label("Magnitude [dB]")
    
    # Make RTI plot with clutter rejection
    if clutter:
        
        
        sif2 = sif_ave[1:int(v.shape[0]), : ] - sif_ave[0:int(v.shape[0]-1),: ]
        vc = 20*np.log10(np.abs(np.fft.ifft(sif2,n=int(zpad),axis=1)))
        vc2 = vc[: , 0 : int(vc.shape[1]/2)]
        mvc2 = np.amax(vc2)
        
        time_pad = np.zeros( (1,vc2.shape[1]),dtype=int )
        
        vc2 = np.vstack([vc2, time_pad])
        
        range_m2 = np.linspace(0,max_range,vc2.shape[1])
        
        cf = ax.pcolormesh(range_m2, 
                           time, 
                           vc2-mvc2,
                           shading='gouraud', cmap='seismic',
                           vmin=-80, vmax=0)
        ax.set_title("RTI with clutter rejection")
        ax.set_xlim(0,5)
        ax.set_xlabel("Range [m]")
        ax.set_ylabel("Time [s]")
        fig.colorbar(cf, ax=ax).set_label("Magnitude [dB]")
    
    return fig,ax

def read_data_doppler(file_in, pw, fc):
    """
    

    Parameters
    ----------
    file_in : str
        Input .wav file.
    pw : double
        Pulse width [s]
    fc : double
        Transmit center frequency [Hz]

    Returns
    -------
    fig : Figure
        Figure containing the time-Doppler plot.
    ax : axes.Axes
        Axes object of the time-Doppler plot.
    
    Notes
    -----
    This function is adapted directly from the MATLAB code of the same name.

    """
    
    fs, signal = read_file(file_in)
    
    N = int(pw*fs);  # # of samples per pulse
    
    s, trig = sig_trig(signal)
    
    sig_length = len(s)
    num_chunks = round(sig_length/N)
    
    sif = []
    
    
    for ii in range(0,num_chunks-1):
        start_chunk = int(ii*N)
        end_chunk = int((ii+1)*N)
        sif.append(s[start_chunk:end_chunk])
    
    sif2 = np.array(sif)
    
    sif_ave = sif2 - np.mean(s)
    
    zpad = int(8*N/2)
    
    sif_ave_fft = 20*np.log10(abs(np.fft.ifft(sif_ave, zpad, axis=1)))
    
    
    half_point = int(np.size(sif_ave_fft, axis = 1)/2)
    
    data = sif_ave_fft[:, 0:half_point]
    
    max_data = np.amax(data)
    
    # Calculate velocity
    delta_f = np.linspace(0, fs/2, int(np.size(data, axis=1)))
    wavelength=c/fc
    velocity = delta_f*wavelength/2
    
    # Calculate time
    time = np.linspace(1, pw*np.size(data,axis=0), np.size(data,axis=0))
    
    
    # Make plot
    fig, ax = plt.subplots()
    cf = ax.pcolormesh(velocity,
                       time, 
                       data-max_data,
                       shading='gouraud',cmap='seismic', vmin=-30, vmax=0)
    ax.set_title("Time vs Doppler")
    ax.set_xlim(0,40)
    ax.set_xlabel("Velocity [m/s]")
    ax.set_ylabel("Time [s]")
    fig.colorbar(cf, ax=ax).set_label("Magnitude [dB]")
    
    print("Done")
    
    return fig, ax

