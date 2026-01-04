"""
SIR is a compartmental model.

Implements a basic SIR model with a time-varying transmission rate which is,
used to study non-stationary epidemic dynamics.


Mathematical Model:
    dS/dt = -β(t) · S · I
    dI/dt = β(t) · S · I - γ · I
    dR/dt = γ · I
"""

import numpy as np
from scipy.integrate import odeint


def sir_derivatives(y, t, beta_func, gamma, current_I=None):
    """
    Compute derivatives for the SIR model at time t.
    """
    S, I, R = y
    
    # Get time-varying transmission rate
    I_for_beta = current_I if current_I is not None else I
    beta_t = beta_func(t, I_for_beta)
    
    # SIR equations
    dS_dt = -beta_t * S * I
    dI_dt = beta_t * S * I - gamma * I
    dR_dt = gamma * I
    
    return [dS_dt, dI_dt, dR_dt]


def solve_sir(t_span, y0, beta_func, gamma, dt=0.1):
    """
    Solve the SIR model over a given time span.
    
    Uses scipy.integrate.odeint to numerically integrate the SIR equations.
    """

def compute_summary_statistics(t, solution):
    """
    Computed the epidemiological summary statistics from the simulation results.
    """
    S, I, R = solution[:, 0], solution[:, 1], solution[:, 2]
    
    # Peak infection
    peak_idx = np.argmax(I)
    peak_infection = I[peak_idx]
    peak_time = t[peak_idx]
    
    # Final size 
    final_size = R[-1]
    
    # Duration 
    threshold = 0.001 * peak_infection
    duration_idx = np.where(I[peak_idx:] < threshold)[0]
    if len(duration_idx) > 0:
        duration = t[peak_idx + duration_idx[0]] - t[0]
    else:
        duration = t[-1] - t[0] 
    
    return {
        'peak_infection': peak_infection,
        'peak_time': peak_time,
        'final_size': final_size,
        'duration': duration
    }
