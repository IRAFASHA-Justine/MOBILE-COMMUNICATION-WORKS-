import numpy as np
import matplotlib.pyplot as plt
import csv
import os

# ============================================================
# MINI PROJECT 1.1
# SIMULATING LINK BUDGETS AND COVERAGE RANGE
# ============================================================

# -----------------------------
# Basic link-budget functions
# -----------------------------

def fspl_db(d_km, f_mhz):
    """
    Free-space path loss in dB.

    d_km  = distance in kilometers
    f_mhz = frequency in MHz
    """
    return (
        20 * np.log10(d_km)
        + 20 * np.log10(f_mhz)
        + 32.44
    )


def link_budget_dbm(
    p_tx_dbm,
    g_tx_db,
    l_path_db,
    g_rx_db,
    l_other_db
):
    """
    Calculate received power in dBm.
    """
    return (
        p_tx_dbm
        + g_tx_db
        - l_path_db
        + g_rx_db
        - l_other_db
    )


def maximum_range(distances, received_power, sensitivity):
    """
    Find the largest distance where received power
    is still above receiver sensitivity.
    """
    valid = distances[received_power > sensitivity]

    if len(valid) == 0:
        return 0

    return valid[-1]


def calculate_snr_db(received_power_dbm, noise_floor_dbm):
    """
    Calculate SNR in dB.
    """
    return received_power_dbm - noise_floor_dbm


def db_to_linear(db):
    """
    Convert dB to linear scale.
    """
    return 10 ** (db / 10)


def shannon_capacity(bandwidth_hz, snr_db):
    """
    Shannon capacity:
    C = B log2(1 + SNR)
    """
    snr_linear = db_to_linear(snr_db)

    return bandwidth_hz * np.log2(1 + snr_linear)


# ============================================================
# PARAMETERS
# ============================================================

P_TX = 40              # dBm
G_TX = 15              # dBi
G_RX = 0               # dBi
L_OTHER = 3            # dB
SENSITIVITY = -100     # dBm

REFERENCE_DISTANCE = 1     # km

# Distance from 0.01 km to 100 km
distances = np.logspace(-2, 2, 500)

# Frequencies
bands = {
    "700 MHz": 700,
    "28 GHz": 28000
}


# ============================================================
# MAIN CALCULATION
# ============================================================

results = []

print("\n==============================================")
print(" MINI PROJECT 1.1 - LINK BUDGET SIMULATION")
print("==============================================\n")

for band_name, frequency in bands.items():

    path_loss = fspl_db(distances, frequency)

    received_power = link_budget_dbm(
        P_TX,
        G_TX,
        path_loss,
        G_RX,
        L_OTHER
    )

    max_range = maximum_range(
        distances,
        received_power,
        SENSITIVITY
    )

    reference_path_loss = fspl_db(
        REFERENCE_DISTANCE,
        frequency
    )

    reference_power = link_budget_dbm(
        P_TX,
        G_TX,
        reference_path_loss,
        G_RX,
        L_OTHER
    )

    margin = reference_power - SENSITIVITY

    results.append([
        band_name,
        frequency,
        reference_path_loss,
        reference_power,
        margin,
        max_range
    ])

    print(f"Band: {band_name}")
    print(f"Frequency: {frequency} MHz")
    print(f"Path loss at 1 km: {reference_path_loss:.4f} dB")
    print(f"Received power at 1 km: {reference_power:.4f} dBm")
    print(f"Link margin at 1 km: {margin:.4f} dB")
    print(f"Maximum usable range: {max_range:.4f} km")
    print("----------------------------------------------")


# ============================================================
# SAVE BASIC RESULTS
# ============================================================

with open("results.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "Band",
        "Frequency_MHz",
        "Path_Loss_At_1km_dB",
        "Received_Power_At_1km_dBm",
        "Link_Margin_dB",
        "Maximum_Range_km"
    ])

    writer.writerows(results)


# ============================================================
# MAIN GRAPH
# ============================================================

plt.figure(figsize=(10, 6))

for band_name, frequency in bands.items():

    path_loss = fspl_db(distances, frequency)

    received_power = link_budget_dbm(
        P_TX,
        G_TX,
        path_loss,
        G_RX,
        L_OTHER
    )

    plt.plot(
        distances,
        received_power,
        label=band_name
    )


plt.axhline(
    SENSITIVITY,
    linestyle="--",
    label="Receiver Sensitivity (-100 dBm)"
)

plt.xscale("log")

plt.xlabel("Distance (km)")
plt.ylabel("Received Power (dBm)")

plt.title(
    "Link Budget Comparison: 700 MHz vs 28 GHz"
)

plt.grid(True, which="both")
plt.legend()

plt.tight_layout()

plt.savefig(
    "link_budget_comparison.png",
    dpi=300
)

plt.show()


# ============================================================
# TASK 1
# Increase 28 GHz antenna gain from 15 to 24 dBi
# ============================================================

print("\n==============================================")
print("TASK 1 - 28 GHz ANTENNA GAIN = 24 dBi")
print("==============================================")

frequency = 28000
new_gain = 24

path_loss_28 = fspl_db(
    distances,
    frequency
)

received_power_28_gain = link_budget_dbm(
    P_TX,
    new_gain,
    path_loss_28,
    G_RX,
    L_OTHER
)

old_range = maximum_range(
    distances,
    link_budget_dbm(
        P_TX,
        G_TX,
        path_loss_28,
        G_RX,
        L_OTHER
    ),
    SENSITIVITY
)

new_range = maximum_range(
    distances,
    received_power_28_gain,
    SENSITIVITY
)

print(f"Original 28 GHz range: {old_range:.4f} km")
print(f"New 28 GHz range:      {new_range:.4f} km")
print(f"Range improvement:     {new_range / old_range:.2f} times")


# ============================================================
# TASK 2
# Add 3.5 GHz
# ============================================================

print("\n==============================================")
print("TASK 2 - ADD 3.5 GHz")
print("==============================================")

frequency_35 = 3500

path_loss_35 = fspl_db(
    distances,
    frequency_35
)

received_power_35 = link_budget_dbm(
    P_TX,
    G_TX,
    path_loss_35,
    G_RX,
    L_OTHER
)

range_35 = maximum_range(
    distances,
    received_power_35,
    SENSITIVITY
)

print(f"3.5 GHz maximum range: {range_35:.4f} km")


plt.figure(figsize=(10, 6))

for band_name, frequency in {
    "700 MHz": 700,
    "3.5 GHz": 3500,
    "28 GHz": 28000
}.items():

    path_loss = fspl_db(
        distances,
        frequency
    )

    received_power = link_budget_dbm(
        P_TX,
        G_TX,
        path_loss,
        G_RX,
        L_OTHER
    )

    plt.plot(
        distances,
        received_power,
        label=band_name
    )

plt.axhline(
    SENSITIVITY,
    linestyle="--",
    label="Sensitivity (-100 dBm)"
)

plt.xscale("log")

plt.xlabel("Distance (km)")
plt.ylabel("Received Power (dBm)")
plt.title("700 MHz, 3.5 GHz and 28 GHz Comparison")

plt.grid(True, which="both")
plt.legend()
plt.tight_layout()

plt.savefig(
    "three_band_comparison.png",
    dpi=300
)

plt.show()


# ============================================================
# TASK 3
# Add 8 dB shadowing/fading margin
# ============================================================

print("\n==============================================")
print("TASK 3 - ADD 8 dB SHADOWING / FADING")
print("==============================================")

FADING_MARGIN = 8

task3_results = []

for band_name, frequency in {
    "700 MHz": 700,
    "3.5 GHz": 3500,
    "28 GHz": 28000
}.items():

    path_loss = fspl_db(
        distances,
        frequency
    )

    received_power = link_budget_dbm(
        P_TX,
        G_TX,
        path_loss,
        G_RX,
        L_OTHER + FADING_MARGIN
    )

    range_with_margin = maximum_range(
        distances,
        received_power,
        SENSITIVITY
    )

    task3_results.append([
        band_name,
        range_with_margin
    ])

    print(
        f"{band_name}: "
        f"{range_with_margin:.4f} km"
    )


with open(
    "task3_fading_results.csv",
    "w",
    newline=""
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "Band",
        "Range_With_8dB_Fading_Margin_km"
    ])

    writer.writerows(task3_results)


# ============================================================
# TASK 4
# SNR and Shannon Capacity
# ============================================================

print("\n==============================================")
print("TASK 4 - SNR AND SHANNON CAPACITY")
print("==============================================")

NOISE_FLOOR = -104       # dBm
BANDWIDTH = 10e6         # 10 MHz

capacity_results = {}

for band_name, frequency in {
    "700 MHz": 700,
    "3.5 GHz": 3500,
    "28 GHz": 28000
}.items():

    path_loss = fspl_db(
        distances,
        frequency
    )

    received_power = link_budget_dbm(
        P_TX,
        G_TX,
        path_loss,
        G_RX,
        L_OTHER
    )

    snr = calculate_snr_db(
        received_power,
        NOISE_FLOOR
    )

    capacity = shannon_capacity(
        BANDWIDTH,
        snr
    )

    # Only positive/meaningful SNR region
    capacity = np.maximum(capacity, 0)

    capacity_results[band_name] = capacity

    print(
        f"{band_name}: "
        f"Maximum capacity = "
        f"{np.max(capacity) / 1e6:.2f} Mbps"
    )


plt.figure(figsize=(10, 6))

for band_name, capacity in capacity_results.items():

    plt.plot(
        distances,
        capacity / 1e6,
        label=band_name
    )

plt.xscale("log")

plt.xlabel("Distance (km)")
plt.ylabel("Shannon Capacity (Mbps)")

plt.title(
    "Estimated Shannon Capacity vs Distance"
)

plt.grid(True, which="both")
plt.legend()
plt.tight_layout()

plt.savefig(
    "capacity_vs_distance.png",
    dpi=300
)

plt.show()


# ============================================================
# TASK 5
# Doubling transmit power vs doubling bandwidth
# ============================================================

print("\n==============================================")
print("TASK 5 - POWER VS BANDWIDTH")
print("==============================================")

frequency = 3500

path_loss = fspl_db(
    REFERENCE_DISTANCE,
    frequency
)

# Original received power
original_power = link_budget_dbm(
    P_TX,
    G_TX,
    path_loss,
    G_RX,
    L_OTHER
)

original_snr = (
    original_power
    - NOISE_FLOOR
)

original_capacity = shannon_capacity(
    BANDWIDTH,
    original_snr
)

# Double transmit power
# Doubling power adds approximately 3 dB
doubled_power_dbm = P_TX + 3

power_doubled_received = link_budget_dbm(
    doubled_power_dbm,
    G_TX,
    path_loss,
    G_RX,
    L_OTHER
)

power_doubled_snr = (
    power_doubled_received
    - NOISE_FLOOR
)

power_doubled_capacity = shannon_capacity(
    BANDWIDTH,
    power_doubled_snr
)

# Double bandwidth
bandwidth_doubled = BANDWIDTH * 2

bandwidth_doubled_capacity = shannon_capacity(
    bandwidth_doubled,
    original_snr
)

print(
    f"Original capacity: "
    f"{original_capacity / 1e6:.2f} Mbps"
)

print(
    f"Capacity after doubling Tx power: "
    f"{power_doubled_capacity / 1e6:.2f} Mbps"
)

print(
    f"Capacity after doubling bandwidth: "
    f"{bandwidth_doubled_capacity / 1e6:.2f} Mbps"
)


# ============================================================
# TASK 6
# Qualitative FDD vs TDD note
# ============================================================

print("\n==============================================")
print("TASK 6 - FDD VS TDD NOTE")
print("==============================================")

print("""
FDD uses separate uplink and downlink frequency channels,
so transmission can occur continuously in both directions.

TDD uses the same frequency channel at different times.
Therefore, time is divided between uplink and downlink.

TDD also requires guard periods when changing direction.
These guard periods do not carry useful payload.

Therefore, guard periods and reduced per-direction slot
time reduce the effective transmit duty cycle compared
with an ideal continuously transmitting FDD link.
""")


# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n==============================================")
print("PROJECT 1.1 COMPLETED")
print("==============================================")

print("""
Files generated:

1. results.csv
2. link_budget_comparison.png
3. three_band_comparison.png
4. task3_fading_results.csv
5. capacity_vs_distance.png
""")