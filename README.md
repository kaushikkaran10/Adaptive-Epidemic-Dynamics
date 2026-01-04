### Adaptive Modeling of Infectious Disease Dynamics

This project explores how changes in disease transmission caused by public health interventions or behavioral responses affect epidemic dynamics, and how simple adaptive control strategies can respond to those changes.
The focus is conceptual and interpretive rather than predictive the goal is to understand how different intervention strategies shape epidemic trajectories under controlled modeling assumptions.

### Motivation

Epidemic processes are inherently non-stationary. Transmission rates evolve over time due to policy decisions, risk perception, and social behavior. Classical compartmental models often assume constant parameters, which limits their ability to represent real intervention dynamics.

# This project investigates two related questions:

1. How do externally scheduled interventions alter epidemic outcomes compared to an uncontrolled baseline?
2. Can feedback-based adaptive control, where interventions respond to observed infection levels, mitigate epidemic peaks more effectively?

To address these questions, I use a simple but interpretable mathematical modeling framework based on the SIR model.

### Modeling Framework

# SIR Model

The population is divided into three compartments:

S(t) — susceptible

I(t) — infected

R(t) — recovered

The system is governed by:
```
dS/dt = −β(t) · S · I
dI/dt =  β(t) · S · I − γ · I
dR/dt =  γ · I

```

Here, β(t) is a time dependent transmission rate and γ is the recovery rate.
The total population is conserved: S + I + R = 1.

### Transmission Scenarios

Three transmission regimes are considered.

1. Static Baseline

A constant transmission rate β₀ represents an uncontrolled epidemic with no interventions.
This scenario serves as a reference point for comparison.

2. Non-Stationary 
Transmission is reduced at a predetermined time to model an external intervention  followed by partial relaxation:

* Initial phase: high transmission
* Intervention phase: reduced transmission
* Rebound phase: partial recovery of contacts

This captures policy changes that are time-driven rather than state-driven.

3. Adaptive 
In the adaptive scenario, transmission responds dynamically to infection prevalence:

* When infections exceed an upper threshold, transmission is reduced
* When infections fall below a lower threshold, transmission is relaxed
* Updates occur at fixed intervals to reflect delayed policy responses
* Transmission is bounded to avoid unrealistic extremes

Interpretation:
This approximates capacity-based interventions where policy strength responds to healthcare system strain rather than fixed schedules.

### Assumptions and Scope

This model intentionally adopts simplifying assumptions common in compartmental epidemiology:

* Closed population with homogeneous mixing
* Deterministic dynamics (no stochastic noise)
* Permanent immunity after recovery
* Instantaneous policy effects once triggered

As a result, the model is not intended for real-world prediction, but rather for comparative analysis and intuition-building.

### Experimental Design

All scenarios are simulated over a 200-day period with identical initial conditions.
For each scenario, the following metrics are evaluated:

* Peak infection prevalence
* Time of peak infection
* Final attack rate (total proportion infected)
* Approximate epidemic duration

Simulations are performed using SciPy’s ODE solver, and adaptive scenarios are solved in segments to allow periodic policy re-evaluation.

### Outputs

Running the experiments generates:

* SIR trajectory plots for each scenario
* Direct comparison of infection curves, including adaptive thresholds
* Transmission rate evolution over time
* A summary table of key epidemiological metrics

All figures are saved in the figures/ directory.

### Reproducing the Experiments

# Install dependencies:

 ```bash 
pip install -r requirements.txt
```

# Run the experiments:

```bash
python experiments/run_experiments.py
```
The script will execute all scenarios, generate figures, and print summary statistics.

### Project Structure
```
adaptive-epidemic-model/
├── src/
│   ├── sir_model.py         
│   ├── adaptive_control.py  
│   └── simulation.py         
├── experiments/
│   └── run_experiments.py    
├── figures/                  
├── requirements.txt
└── README.md
```
### References

* Kermack & McKendrick (1927), Proceedings of the Royal Society A

* Anderson & May (1991), Infectious Diseases of Humans

* Keeling & Rohani (2008), Modeling Infectious Diseases in Humans and Animals

### Note

This project is a computational modeling exercise, not a forecasting tool.
Parameter values are illustrative, and conclusions should be interpreted in the context of the model’s assumptions.