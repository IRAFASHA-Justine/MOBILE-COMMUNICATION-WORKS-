import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# MINI PROJECT 1.2
# COMPARING FDD AND TDD RESOURCE UTILIZATION
# UNDER TRAFFIC ASYMMETRY
# ============================================================


# ------------------------------------------------------------
# 1. FIXED SYSTEM PARAMETERS
# ------------------------------------------------------------

# Total capacity available to the system
TOTAL_CAPACITY = 100.0

# FDD has two independent fixed-capacity channels.
# Each direction receives half of the total capacity.
FDD_DL_CAPACITY = TOTAL_CAPACITY / 2
FDD_UL_CAPACITY = TOTAL_CAPACITY / 2

# TDD uses the same total capacity but shares it in time.
TDD_GUARD_FRACTIONS = [0.02, 0.05, 0.10]

# Traffic scenarios: Downlink : Uplink
SCENARIOS = {
    "50:50": (0.50, 0.50),
    "70:30": (0.70, 0.30),
    "80:20": (0.80, 0.20),
    "90:10": (0.90, 0.10)
}


# ------------------------------------------------------------
# 2. FDD SIMULATION
# ------------------------------------------------------------

def simulate_fdd(dl_demand, ul_demand):
    """
    Simulate FDD.

    FDD has fixed capacity:
        DL = 50
        UL = 50

    Demand is expressed as a fraction of total traffic.

    The available capacity in each direction cannot
    be transferred to the other direction.
    """

    # Assume total offered demand = TOTAL_CAPACITY
    total_demand = TOTAL_CAPACITY

    dl_requested = dl_demand * total_demand
    ul_requested = ul_demand * total_demand

    # Actual traffic delivered
    dl_delivered = min(dl_requested, FDD_DL_CAPACITY)
    ul_delivered = min(ul_requested, FDD_UL_CAPACITY)

    total_delivered = dl_delivered + ul_delivered

    utilization = total_delivered / TOTAL_CAPACITY

    return {
        "DL_Throughput": dl_delivered,
        "UL_Throughput": ul_delivered,
        "Total_Throughput": total_delivered,
        "Utilization": utilization * 100
    }


# ------------------------------------------------------------
# 3. TDD SIMULATION
# ------------------------------------------------------------

def simulate_tdd(dl_demand, ul_demand, guard_fraction):
    """
    Simulate TDD.

    TDD can dynamically change its DL/UL slot ratio
    according to the traffic demand.

    Guard-period overhead reduces the useful capacity.
    """

    # Useful fraction after guard overhead
    useful_fraction = 1 - guard_fraction

    # Total useful capacity
    useful_capacity = TOTAL_CAPACITY * useful_fraction

    # Match the TDD allocation to the traffic demand
    dl_allocation = dl_demand
    ul_allocation = ul_demand

    # Calculate available capacity per direction
    dl_capacity = useful_capacity * dl_allocation
    ul_capacity = useful_capacity * ul_allocation

    # Offered traffic
    total_demand = TOTAL_CAPACITY

    dl_requested = dl_demand * total_demand
    ul_requested = ul_demand * total_demand

    # Delivered traffic
    dl_delivered = min(dl_requested, dl_capacity)
    ul_delivered = min(ul_requested, ul_capacity)

    total_delivered = dl_delivered + ul_delivered

    utilization = total_delivered / TOTAL_CAPACITY

    return {
        "DL_Throughput": dl_delivered,
        "UL_Throughput": ul_delivered,
        "Total_Throughput": total_delivered,
        "Utilization": utilization * 100
    }


# ------------------------------------------------------------
# 4. RUN MAIN SCENARIOS
# ------------------------------------------------------------

results = []

main_guard_fraction = 0.05

for scenario, (dl_ratio, ul_ratio) in SCENARIOS.items():

    fdd = simulate_fdd(dl_ratio, ul_ratio)

    tdd = simulate_tdd(
        dl_ratio,
        ul_ratio,
        main_guard_fraction
    )

    results.append({
        "Scenario": scenario,
        "DL_Demand_%": dl_ratio * 100,
        "UL_Demand_%": ul_ratio * 100,

        "FDD_DL_Throughput": fdd["DL_Throughput"],
        "FDD_UL_Throughput": fdd["UL_Throughput"],
        "FDD_Total_Throughput": fdd["Total_Throughput"],
        "FDD_Utilization_%": fdd["Utilization"],

        "TDD_DL_Throughput": tdd["DL_Throughput"],
        "TDD_UL_Throughput": tdd["UL_Throughput"],
        "TDD_Total_Throughput": tdd["Total_Throughput"],
        "TDD_Utilization_%": tdd["Utilization"],

        "TDD_Guard_%": main_guard_fraction * 100
    })


# Convert results to DataFrame
results_df = pd.DataFrame(results)


# ------------------------------------------------------------
# 5. PRINT MAIN RESULTS
# ------------------------------------------------------------

print("\n")
print("=" * 75)
print("FDD VS TDD RESOURCE UTILIZATION")
print("=" * 75)

print("\nSystem Parameters:")
print(f"Total capacity: {TOTAL_CAPACITY}")
print(f"FDD DL capacity: {FDD_DL_CAPACITY}")
print(f"FDD UL capacity: {FDD_UL_CAPACITY}")
print(f"TDD guard overhead: {main_guard_fraction * 100:.1f}%")

print("\nMain Results:")
print(results_df.to_string(index=False))


# ------------------------------------------------------------
# 6. SAVE MAIN RESULTS
# ------------------------------------------------------------

results_df.to_csv(
    "results.csv",
    index=False
)

print("\nMain results saved to:")
print("results.csv")


# ------------------------------------------------------------
# 7. PLOT UTILIZATION COMPARISON
# ------------------------------------------------------------

scenarios = results_df["Scenario"]

fdd_utilization = results_df["FDD_Utilization_%"]
tdd_utilization = results_df["TDD_Utilization_%"]

x = np.arange(len(scenarios))
width = 0.35

plt.figure(figsize=(10, 6))

plt.bar(
    x - width / 2,
    fdd_utilization,
    width,
    label="FDD"
)

plt.bar(
    x + width / 2,
    tdd_utilization,
    width,
    label="TDD"
)

plt.xlabel("Traffic Asymmetry (DL:UL)")
plt.ylabel("Utilization (%)")
plt.title("FDD vs TDD Resource Utilization")
plt.xticks(x, scenarios)
plt.ylim(0, 110)
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.legend()

plt.tight_layout()

plt.savefig(
    "fdd_tdd_comparison.png",
    dpi=300
)

plt.show()

print("\nPlot saved to:")
print("fdd_tdd_comparison.png")


# ------------------------------------------------------------
# 8. TEST DIFFERENT TDD GUARD PERIODS
# ------------------------------------------------------------

guard_results = []

for guard_fraction in TDD_GUARD_FRACTIONS:

    for scenario, (dl_ratio, ul_ratio) in SCENARIOS.items():

        tdd = simulate_tdd(
            dl_ratio,
            ul_ratio,
            guard_fraction
        )

        guard_results.append({
            "Scenario": scenario,
            "DL_Demand_%": dl_ratio * 100,
            "UL_Demand_%": ul_ratio * 100,
            "Guard_Overhead_%": guard_fraction * 100,
            "TDD_DL_Throughput": tdd["DL_Throughput"],
            "TDD_UL_Throughput": tdd["UL_Throughput"],
            "TDD_Total_Throughput": tdd["Total_Throughput"],
            "TDD_Utilization_%": tdd["Utilization"]
        })


guard_df = pd.DataFrame(guard_results)


# ------------------------------------------------------------
# 9. PRINT GUARD PERIOD RESULTS
# ------------------------------------------------------------

print("\n")
print("=" * 75)
print("TDD GUARD-PERIOD ANALYSIS")
print("=" * 75)

print("\n")
print(guard_df.to_string(index=False))


# ------------------------------------------------------------
# 10. SAVE GUARD PERIOD RESULTS
# ------------------------------------------------------------

guard_df.to_csv(
    "guard_period_results.csv",
    index=False
)

print("\nGuard-period results saved to:")
print("guard_period_results.csv")


# ------------------------------------------------------------
# 11. GUARD PERIOD COMPARISON PLOT
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

for guard in TDD_GUARD_FRACTIONS:

    subset = guard_df[
        guard_df["Guard_Overhead_%"] == guard * 100
    ]

    plt.plot(
        subset["Scenario"],
        subset["TDD_Utilization_%"],
        marker="o",
        label=f"{guard * 100:.0f}% guard"
    )

plt.xlabel("Traffic Asymmetry (DL:UL)")
plt.ylabel("TDD Utilization (%)")
plt.title("Effect of TDD Guard Period on Resource Utilization")
plt.ylim(0, 105)
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()

plt.tight_layout()

plt.savefig(
    "guard_period_comparison.png",
    dpi=300
)

plt.show()

print("\nGuard-period plot saved to:")
print("guard_period_comparison.png")


# ------------------------------------------------------------
# 12. FIND THE FDD/TDD CROSSOVER
# ------------------------------------------------------------

print("\n")
print("=" * 75)
print("FDD VS TDD INTERPRETATION")
print("=" * 75)

for _, row in results_df.iterrows():

    difference = (
        row["TDD_Utilization_%"]
        - row["FDD_Utilization_%"]
    )

    print(
        f"{row['Scenario']}: "
        f"FDD = {row['FDD_Utilization_%']:.1f}%, "
        f"TDD = {row['TDD_Utilization_%']:.1f}%, "
        f"TDD-FDD = {difference:.1f}%"
    )


# ------------------------------------------------------------
# 13. SUMMARY
# ------------------------------------------------------------

print("\n")
print("=" * 75)
print("SUMMARY")
print("=" * 75)

print("""
FDD:
- Uses two independent fixed channels.
- Each direction has a fixed 50% capacity.
- Capacity that is unused in one direction cannot be
  transferred to the other direction.

TDD:
- Uses one shared channel.
- The DL/UL slot ratio can be changed according to traffic.
- Guard periods reduce the amount of time available for
  useful data transmission.

With symmetric traffic (50:50), FDD has an advantage
because it does not lose capacity to TDD guard periods.

As downlink traffic becomes more asymmetric, TDD can
reallocate more resources toward the downlink.

Increasing guard-period overhead reduces TDD's effective
utilization and therefore reduces the benefit of flexible
resource allocation.
""")

print("\nAll Project 02 calculations completed successfully.")