"""
Run and compare SIR simulations under static, non-stationary,
and adaptive transmission scenarios.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
import matplotlib.pyplot as plt
from adaptive_control import StaticBeta, NonStationaryBeta, AdaptiveBeta
from simulation import run_scenario


# Model parameters 
GAMMA = 0.1           
BETA_0 = 0.5           
T_SPAN = (0, 200)      
Y0 = [0.99, 0.01, 0.0]  

# Non-stationary scenario parameters
INTERVENTION_TIME = 50     
INTERVENTION_REDUCTION = 0.6 
REBOUND_TIME = 100         
REBOUND_FACTOR = 0.5        

# Adaptive scenario parameters
UPPER_THRESHOLD = 0.15    
LOWER_THRESHOLD = 0.05    
REDUCTION_FACTOR = 0.4    
INCREASE_FACTOR = 0.2     
CONTROL_INTERVAL = 5      


def run_all_scenarios():
    """
    Execute all three epidemic scenarios.
    """
    print("Running simulations...")
    
    scenarios = {}
    
    # Scenario 1: Static transmission rate
    print("Static scenario complete")
    beta_static = StaticBeta(beta_0=BETA_0)
    scenarios['static'] = run_scenario(
        'static', T_SPAN, Y0, beta_static, GAMMA
    )
    print(f"  ✓ Peak infection: {scenarios['static']['stats']['peak_infection']:.3f}")
    print(f"  ✓ Peak time: {scenarios['static']['stats']['peak_time']:.1f} days")
    print()
    
    # Scenario 2: Non-stationary transmission rate
    print("Non-stationary transmission rate")
    print(f"  Intervention at day {INTERVENTION_TIME}: β reduced by {INTERVENTION_REDUCTION*100:.0f}%")
    print(f"  Rebound at day {REBOUND_TIME}: β partially recovers")
    beta_nonstat = NonStationaryBeta(
        beta_0=BETA_0,
        intervention_time=INTERVENTION_TIME,
        intervention_reduction=INTERVENTION_REDUCTION,
        rebound_time=REBOUND_TIME,
        rebound_factor=REBOUND_FACTOR
    )
    scenarios['nonstationary'] = run_scenario(
        'nonstationary', T_SPAN, Y0, beta_nonstat, GAMMA
    )
    print(f"  ✓ Peak infection: {scenarios['nonstationary']['stats']['peak_infection']:.3f}")
    print(f"  ✓ Peak time: {scenarios['nonstationary']['stats']['peak_time']:.1f} days")
    print()
    
    # Scenario 3: Adaptive transmission rate
    print("Scenario 3: Adaptive feedback control")
    print(f"  Upper threshold: I > {UPPER_THRESHOLD:.2f}")
    print(f"  Lower threshold: I < {LOWER_THRESHOLD:.2f}")
    print(f"  Control interval: {CONTROL_INTERVAL} days")
    beta_adaptive = AdaptiveBeta(
        beta_0=BETA_0,
        upper_threshold=UPPER_THRESHOLD,
        lower_threshold=LOWER_THRESHOLD,
        reduction_factor=REDUCTION_FACTOR,
        increase_factor=INCREASE_FACTOR
    )
    scenarios['adaptive'] = run_scenario(
        'adaptive', T_SPAN, Y0, beta_adaptive, GAMMA,
        control_interval=CONTROL_INTERVAL
    )
    print(f"  ✓ Peak infection: {scenarios['adaptive']['stats']['peak_infection']:.3f}")
    print(f"  ✓ Peak time: {scenarios['adaptive']['stats']['peak_time']:.1f} days")
    print()
    
    return scenarios


def plot_sir_curves(scenarios, save_path):
    """Plot SIR compartment trajectories for each scenario."""
    fig, axes = plt.subplots(3, 3, figsize=(15, 12))
    scenario_names = ['static', 'nonstationary', 'adaptive']
    scenario_titles = ['Static β', 'Non-Stationary β', 'Adaptive β']
    compartments = ['S', 'I', 'R']
    colors = ['#2E86AB', '#A23B72', '#F18F01']
    
    for i, (name, title) in enumerate(zip(scenario_names, scenario_titles)):
        results = scenarios[name]
        t = results['t']
        
        for j, compartment in enumerate(compartments):
            ax = axes[i, j]
            ax.plot(t, results[compartment], color=colors[j], linewidth=2)
            ax.set_xlabel('Time (days)', fontsize=11)
            ax.set_ylabel(f'{compartment}(t)', fontsize=11)
            ax.grid(True, alpha=0.3)
            ax.set_xlim(0, T_SPAN[1])
            ax.set_ylim(0, 1)
            
            # Add title only to top row
            if i == 0:
                ax.set_title(f'{compartment} Compartment', fontsize=12, fontweight='bold')
            
            # Add scenario label to first column
            if j == 0:
                ax.text(-0.35, 0.5, title, transform=ax.transAxes,
                       fontsize=12, fontweight='bold', rotation=90,
                       verticalalignment='center')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {save_path}")


def plot_infection_comparison(scenarios, save_path):
    """
    Compare infection curves across all scenarios.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    scenario_names = ['static', 'nonstationary', 'adaptive']
    scenario_labels = ['Static β', 'Non-Stationary β', 'Adaptive β']
    colors = ['#2E86AB', '#A23B72', '#F18F01']
    linestyles = ['-', '--', '-.']
    
    for name, label, color, ls in zip(scenario_names, scenario_labels, colors, linestyles):
        results = scenarios[name]
        ax.plot(results['t'], results['I'], 
               label=label, color=color, linewidth=2.5, linestyle=ls)
    
    # Add threshold lines for adaptive scenario
    ax.axhline(y=UPPER_THRESHOLD, color='red', linestyle=':', 
              linewidth=1.5, alpha=0.5, label='Upper threshold')
    ax.axhline(y=LOWER_THRESHOLD, color='green', linestyle=':', 
              linewidth=1.5, alpha=0.5, label='Lower threshold')
    
    ax.set_xlabel('Time (days)', fontsize=13)
    ax.set_ylabel('Infected Proportion I(t)', fontsize=13)
    ax.set_title('Comparison of Infection Dynamics', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=11, loc='upper right')
    ax.set_xlim(0, T_SPAN[1])
    ax.set_ylim(0, max([scenarios[s]['I'].max() for s in scenario_names]) * 1.1)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {save_path}")


def plot_beta_evolution(scenarios, save_path):
    """
    Display how transmission rate β(t) evolves over time.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    scenario_names = ['static', 'nonstationary', 'adaptive']
    scenario_labels = ['Static β', 'Non-Stationary β', 'Adaptive β']
    colors = ['#2E86AB', '#A23B72', '#F18F01']
    linestyles = ['-', '--', '-.']
    
    for name, label, color, ls in zip(scenario_names, scenario_labels, colors, linestyles):
        results = scenarios[name]
        ax.plot(results['t'], results['beta'], 
               label=label, color=color, linewidth=2.5, linestyle=ls)
    
    ax.set_xlabel('Time (days)', fontsize=13)
    ax.set_ylabel('Transmission Rate β(t)', fontsize=13)
    ax.set_title('Evolution of Transmission Rate', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=11, loc='upper right')
    ax.set_xlim(0, T_SPAN[1])
    ax.set_ylim(0, BETA_0 * 1.1)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {save_path}")


def print_summary_table(scenarios):
    """
    Print a formatted table comparing key statistics.
    """
    print("\n" + "="*70)
    print("SUMMARY STATISTICS")
    print("="*70)
    print(f"{'Metric':<30} {'Static':<12} {'Non-Stat':<12} {'Adaptive':<12}")
    print("-"*70)
    
    metrics = [
        ('Peak Infection', 'peak_infection', '.4f'),
        ('Peak Time (days)', 'peak_time', '.1f'),
        ('Final Attack Rate', 'final_size', '.4f'),
        ('Epidemic Duration (days)', 'duration', '.1f')
    ]
    
    for metric_name, stat_key, fmt in metrics:
        row = f"{metric_name:<30}"
        for scenario in ['static', 'nonstationary', 'adaptive']:
            value = scenarios[scenario]['stats'][stat_key]
            formatted_value = f"{value:{fmt}}"
            row += f"{formatted_value:<12}"
        print(row)
    
    print("="*70)


def main():
    """Main execution function."""
    
    # Create figures directory if it doesn't exist
    fig_dir = os.path.join(os.path.dirname(__file__), '..', 'figures')
    os.makedirs(fig_dir, exist_ok=True)
    
    # Run all scenarios
    scenarios = run_all_scenarios()
    
    # Generate visualizations
    print("\nGenerating visualizations...")
    plot_sir_curves(scenarios, os.path.join(fig_dir, 'sir_curves.png'))
    plot_infection_comparison(scenarios, os.path.join(fig_dir, 'infection_comparison.png'))
    plot_beta_evolution(scenarios, os.path.join(fig_dir, 'beta_evolution.png'))
    
    # Print summary statistics
    print_summary_table(scenarios)
    
    print("\n✓ All experiments completed successfully!")


if __name__ == '__main__':
    main()
