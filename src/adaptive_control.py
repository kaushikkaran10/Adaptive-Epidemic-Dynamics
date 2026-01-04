"""
Transmission rate control mechanisms for the SIR model.

Includes static, externally scheduled, and feedback-based adaptive
transmission rate scenarios.
"""

import numpy as np


class StaticBeta:
    """
    Constant transmission rate scenario.

    Serves as a baseline with no interventions or behavioral changes.
    """
    
    def __init__(self, beta_0=0.5):
        self.beta_0 = beta_0
    
    def __call__(self, t, I):
        """
        Return transmission rate at time t.
        """
        return self.beta_0


class NonStationaryBeta:
    """
    Non-stationary transmission rate with external interventions.
    
    Models a scenario where public health interventions are implemented
    at predetermined times, regardless of epidemic state. This represents
    scheduled policy changes.
    """
    
    def __init__(self, beta_0=0.5, intervention_time=50, 
                 intervention_reduction=0.6, rebound_time=None, 
                 rebound_factor=0.5):
        self.beta_0 = beta_0
        self.intervention_time = intervention_time
        self.intervention_reduction = intervention_reduction
        self.rebound_time = rebound_time
        self.rebound_factor = rebound_factor
        
        # Compute transmission rates at different phases
        self.beta_intervention = beta_0 * (1 - intervention_reduction)
        if rebound_time is not None:
            # Rebound is partial increase from intervention level
            self.beta_rebound = self.beta_intervention + \
                                (beta_0 - self.beta_intervention) * rebound_factor
        else:
            self.beta_rebound = self.beta_intervention
    
    def __call__(self, t, I):
        """
        Return transmission rate at time t based on intervention schedule.
        """
        if t < self.intervention_time:
            return self.beta_0
        elif self.rebound_time is None or t < self.rebound_time:
            return self.beta_intervention
        else:
            return self.beta_rebound


class AdaptiveBeta:
    """
    Adaptive transmission rate with feedback-based control.
    
    Represents a reactive policy making where intervention strength
    responds to a observed infection levels, similar to capacity-based
    public health responses,

    Biological Interpretation
    -------------------------
    The adaptive control uses simple infection thresholds to mimic
    capacity-based public health responses. When a infection levels rise
    above a critical level (~15%), transmission is reduced to represent
    a stronger interventions. As infections decline, transmission is
    further relaxed, reflecting reopening or behavioral fatigue.
    
    """
    
    def __init__(self, beta_0=0.5, upper_threshold=0.15, 
                 lower_threshold=0.05, reduction_factor=0.4,
                 increase_factor=0.2, beta_min=0.1, beta_max=0.7):
        self.beta_0 = beta_0
        self.upper_threshold = upper_threshold
        self.lower_threshold = lower_threshold
        self.reduction_factor = reduction_factor
        self.increase_factor = increase_factor
        self.beta_min = beta_min
        self.beta_max = beta_max
        
        # Current transmission rate (will be updated adaptively)
        self.current_beta = beta_0
    
    def __call__(self, t, I):
        """
        Return transmission rate based on current infection level.
        """
        # Adaptive control logic
        if I > self.upper_threshold:
            # Strengthen interventions (reduce transmission)
            self.current_beta *= (1 - self.reduction_factor)
        elif I < self.lower_threshold:
            # Relax interventions (increase transmission)
            self.current_beta *= (1 + self.increase_factor)
        
        # Apply safety bounds
        self.current_beta = np.clip(self.current_beta, self.beta_min, self.beta_max)
        
        return self.current_beta
    
    def reset(self):
        self.current_beta = self.beta_0
