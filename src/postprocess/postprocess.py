import matplotlib.pyplot as plt
import csv

def v_f_v_g_plot(df):
    """
    Plots Velocity vs Frequency and Velocity vs Damping for each mode.
    """
    modes = df['mode'].unique()
    modes.sort()

    _, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

    for mode in modes:
        mode_df = df[df['mode'] == mode].sort_values('speed')
        ax1.plot(mode_df['speed'], mode_df['freq'], marker='o', label=f"Mode {mode}")
        ax2.plot(mode_df['speed'], mode_df['damping'], marker='o', label=f"Mode {mode}")

    ax1.set_ylabel("Frequency [Hz]")
    ax1.set_title("Velocity vs Frequency (V-f)")
    ax1.grid(True)
    ax1.legend()

    ax2.set_xlabel("Velocity [m/s]")
    ax2.set_ylabel("Damping Ratio")
    ax2.set_title("Velocity vs Damping (V-g)")
    ax2.axhline(0, color='red', linestyle='--', label='Neutral Damping')
    ax2.grid(True)
    ax2.legend()

    plt.tight_layout()
    plt.show()

def root_locus_plot(df):
    """
    Plot the root locus from a DataFrame containing flutter analysis results.
    Expects columns: 'real', 'imag', 'speed'
    """
    real_parts = df['real']
    imag_parts = df['imag']
    speeds = df['speed']

    plt.figure(figsize=(10, 6))
    sc = plt.scatter(
        real_parts, imag_parts,
        c=speeds,
        cmap='viridis',
        s=100,
        edgecolors='black'
    )

    plt.xlabel("Real(λ) [Damping]")
    plt.ylabel("Imag(λ) [Oscillation Frequency]")
    plt.title("Root Locus of Flutter Modes vs Flow Velocity")
    plt.axvline(0, color='red', linestyle='--', label='Neutral Damping')
    plt.grid(True)
    cbar = plt.colorbar(sc)
    cbar.set_label("Flow Velocity (U)")
    plt.legend()
    plt.tight_layout()
    plt.show()

def write_flutter_results_to_csv(freestream_speeds, omegas, filename):

    with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["flow_velocity [m/s]", "real frequency component [rad/s]", "imag frequency component [rad/s]"])
            
            for u, omega in zip(freestream_speeds, omegas):
                writer.writerow([u, omega.real, omega.imag])
        
    print(f"Flutter results written to '{filename}'")