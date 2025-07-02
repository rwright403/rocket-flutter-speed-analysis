import matplotlib.pyplot as plt
import csv

def v_f_v_g_plot():
    x=1

def root_locus_plot(freestream_speeds, omegas):
    real_parts = [omega.real for omega in omegas]
    imag_parts = [omega.imag for omega in omegas]


    # Plot
    plt.figure(figsize=(10, 6))
    sc = plt.scatter(real_parts, imag_parts, c=freestream_speeds, cmap='viridis', s=100, edgecolor='black')

    plt.xlabel("Real(ω) [Damping]")
    plt.ylabel("Imag(ω) [Oscillation Frequency]")
    plt.title("Root Locus of Flutter Modes vs Flow velocity")
    plt.axvline(0, color='red', linestyle='--', label='Neutral Damping')
    plt.grid(True)
    plt.colorbar(sc, label="Flow velocity (U)")
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


"""
### Testing:

# Example data
freestream_speeds = np.array([50, 50, 60, 60, 70, 70])
omegas = np.array([
    complex(-0.15, -20.0),
    complex(-0.12, -11.3),
    complex(-0.05, 0.1),
    complex(-0.01, 4.0),
    complex(0.05, 12.2),
    complex(0.12, 26.0)
])

root_locus_plot(freestream_speeds, omegas)
"""