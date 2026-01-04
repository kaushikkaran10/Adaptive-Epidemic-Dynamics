"""
Simulation routines for running SIR models under different transmission scenarios
"""

import numpy as np
from sir_model import solve_sir, compute_summary_statistics


def run_static_scenario(t_span, y0, beta_func, gamma, dt=0.1):
    """
    Run SIR simulation with a constant transmission rate.
    """
    # Solve SIR equations
    t, solution = solve_sir(t_span, y0, beta_func, gamma, dt)
    S, I, R = solution[:, 0], solution[:, 1], solution[:, 2]
    
    # Beta is constant, but we store it as array for consistency
    beta_t = np.array([beta_func(ti, 0) for ti in t])
    
    # Compute statistics
    stats = compute_summary_statistics(t, solution)
    
    return {
        't': t,
        'S': S,
        'I': I,
        'R': R,
        'beta': beta_t,
        'stats': stats
    }


def run_nonstationary_scenario(t_span, y0, beta_func, gamma, dt=0.1):
    """
    Run SIR simulation with a predefined time-varying transmission rate.
    """
    # Solve SIR equations (beta varies with time, but is predetermined)
    t, solution = solve_sir(t_span, y0, beta_func, gamma, dt)
    S, I, R = solution[:, 0], solution[:, 1], solution[:, 2]
    
    # Compute time-varying beta
    beta_t = np.array([beta_func(ti, 0) for ti in t])
    
    # Compute statistics
    stats = compute_summary_statistics(t, solution)
    
    return {
        't': t,
        'S': S,
        'I': I,
        'R': R,
        'beta': beta_t,
        'stats': stats
    }


def run_adaptive_scenario(t_span, y0, beta_func, gamma, 
                         control_interval=5, dt=0.1):
    """
    Run simulation with adaptive transmission rate control.
    
   Because of beta depends on the current infection level, the ODE is solved
   in short segments with the control policy updated at fixed intervals.

    """
    # Reset beta function to initial state
    beta_func.reset()
    
    # Initialize storage
    t_start, t_end = t_span
    t_full = []
    S_full = []
    I_full = []
    R_full = []
    beta_full = []
    
    # Current state
    current_y = np.array(y0)
    current_t = t_start
    
    # Solve in segments
    while current_t < t_end:
        # Determine next control evaluation time
        next_t = min(current_t + control_interval, t_end)
        
        # Current infection level for beta function
        current_I = current_y[1]
        
       # Freeze infection level during this control interval
        def beta_wrapper(t, I):
            return beta_func(t, current_I)
        
        # Solve for this segment
        segment_t, segment_sol = solve_sir(
            (current_t, next_t), 
            current_y, 
            beta_wrapper, 
            gamma, 
            dt
        )
        
        # Store results (avoid duplicating boundary points)
        if len(t_full) == 0:
            t_full.extend(segment_t)
            S_full.extend(segment_sol[:, 0])
            I_full.extend(segment_sol[:, 1])
            R_full.extend(segment_sol[:, 2])
            beta_full.extend([beta_func.current_beta] * len(segment_t))
        else:
            # Skip first point (duplicate of previous segment's last point)
            t_full.extend(segment_t[1:])
            S_full.extend(segment_sol[1:, 0])
            I_full.extend(segment_sol[1:, 1])
            R_full.extend(segment_sol[1:, 2])
            beta_full.extend([beta_func.current_beta] * (len(segment_t) - 1))
        
        # Update state for next segment
        current_y = segment_sol[-1]
        current_t = next_t
    
    # Convert to arrays
    t = np.array(t_full)
    S = np.array(S_full)
    I = np.array(I_full)
    R = np.array(R_full)
    beta_t = np.array(beta_full)
    
    # Compute statistics
    solution = np.column_stack([S, I, R])
    stats = compute_summary_statistics(t, solution)
    
    return {
        't': t,
        'S': S,
        'I': I,
        'R': R,
        'beta': beta_t,
        'stats': stats
    }


def run_scenario(scenario_type, t_span, y0, beta_func, gamma, 
                control_interval=5, dt=0.1):
    """
    Unified interface for running any scenario type.
    """
    if scenario_type == 'static':
        return run_static_scenario(t_span, y0, beta_func, gamma, dt)
    elif scenario_type == 'nonstationary':
        return run_nonstationary_scenario(t_span, y0, beta_func, gamma, dt)
    elif scenario_type == 'adaptive':
        return run_adaptive_scenario(t_span, y0, beta_func, gamma, 
                                     control_interval, dt)
    else:
        raise ValueError(f"Unknown scenario type: {scenario_type}")
