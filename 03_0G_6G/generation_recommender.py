import pandas as pd


# ============================================================
# MOBILE COMMUNICATIONS MINI PROJECT 1.3
# VALIDATING AND EXTENDING 0G-6G
# ============================================================


# ------------------------------------------------------------
# 1. GENERATION DATABASE
# ------------------------------------------------------------

generations = {
    "0G": {
        "period": "Pre-cellular era",
        "technology": "Analog mobile radio / push-to-talk",
        "features": "Early mobile radio, large equipment and limited channels",
        "examples": "Vehicle radio, dispatch radio, early mobile radio",
        "services": "Voice communication and dispatch",
        "problem": "Very limited capacity and no automated cellular architecture"
    },

    "1G": {
        "period": "1980s",
        "technology": "Analog cellular",
        "features": "Analog voice and cellular frequency reuse",
        "examples": "Early cellular phones",
        "services": "Mobile voice calls",
        "problem": "Poor security, limited capacity and low voice quality"
    },

    "2G": {
        "period": "1990s",
        "technology": "Digital cellular / GSM",
        "features": "Digital voice, SMS and improved capacity",
        "examples": "GSM phones, Nokia 3310",
        "services": "Voice, SMS and basic data",
        "problem": "Limited data rates for Internet applications"
    },

    "3G": {
        "period": "2000s",
        "technology": "UMTS / WCDMA",
        "features": "Higher mobile data rates and multimedia",
        "examples": "3G smartphones",
        "services": "Mobile Internet and video calling",
        "problem": "Capacity and data-rate limitations as mobile Internet grew"
    },

    "4G": {
        "period": "2010s",
        "technology": "LTE / LTE-Advanced",
        "features": "High-speed packet communication and all-IP networking",
        "examples": "4G LTE smartphones and routers",
        "services": "Mobile broadband, streaming and Internet applications",
        "problem": "Increasing demand for capacity, connected devices and lower latency"
    },

    "5G": {
        "period": "2020s",
        "technology": "5G NR",
        "features": "High-speed broadband, massive IoT and low latency",
        "examples": "5G smartphones, 5G routers and IoT devices",
        "services": "Enhanced mobile broadband, IoT and industrial applications",
        "problem": "Future networks require greater capacity, intelligence and sensing"
    },

    "6G": {
        "period": "Expected around 2030",
        "technology": "IMT-2030 / emerging 6G",
        "features": "AI-native networking, advanced connectivity and integrated sensing",
        "examples": "Future intelligent communication systems",
        "services": "Advanced sensing, immersive communication and intelligent networking",
        "problem": "Still under research and standardization"
    }
}


# ------------------------------------------------------------
# 2. KEYWORDS
# ------------------------------------------------------------

keywords = {

    "0G": [
        "0g",
        "pre cellular",
        "pre-cellular",
        "push to talk",
        "push-to-talk",
        "vehicle radio",
        "mobile radio",
        "dispatch radio",
        "dispatch"
    ],

    "1G": [
        "1g",
        "analog",
        "analogue",
        "analog voice",
        "first generation",
        "cellular voice"
    ],

    "2G": [
        "2g",
        "gsm",
        "sms",
        "digital voice",
        "digital cellular",
        "nokia 3310",
        "nokia 1100",
        "gprs",
        "edge"
    ],

    "3G": [
        "3g",
        "umts",
        "wcdma",
        "hspa",
        "video calling",
        "mobile internet",
        "3g smartphone"
    ],

    "4G": [
        "4g",
        "lte",
        "lte advanced",
        "lte-advanced",
        "mobile broadband",
        "volte",
        "4g router"
    ],

    "5G": [
        "5g",
        "5g nr",
        "massive iot",
        "urllc",
        "network slicing",
        "5g smartphone",
        "5g router"
    ],

    "6G": [
        "6g",
        "imt 2030",
        "imt-2030",
        "ai native",
        "ai-native",
        "integrated sensing",
        "terahertz",
        "future network"
    ]
}


# ------------------------------------------------------------
# 3. RECOMMENDER FUNCTION
# ------------------------------------------------------------

def recommend_generation(statement):

    text = statement.lower()

    scores = {}

    for generation, word_list in keywords.items():

        score = 0

        for keyword in word_list:

            if keyword in text:
                score += 1

        scores[generation] = score

    highest_score = max(scores.values())

    if highest_score == 0:

        return None, scores

    best_generations = [
        generation
        for generation, score in scores.items()
        if score == highest_score
    ]

    if len(best_generations) > 1:

        return "Ambiguous", scores

    return best_generations[0], scores


# ------------------------------------------------------------
# 4. DISPLAY GENERATION INFORMATION
# ------------------------------------------------------------

def display_generation_information(generation):

    if generation not in generations:
        return

    information = generations[generation]

    print("\n")
    print("=" * 65)
    print(f"INFORMATION FOR {generation}")
    print("=" * 65)

    print(f"Period       : {information['period']}")
    print(f"Technology   : {information['technology']}")
    print(f"Features     : {information['features']}")
    print(f"Examples     : {information['examples']}")
    print(f"Services     : {information['services']}")
    print(f"Main problem : {information['problem']}")

    print("=" * 65)


# ------------------------------------------------------------
# 5. AUTOMATIC TEST STATEMENTS
# ------------------------------------------------------------

test_statements = [

    "This system used analog voice communication.",

    "SMS and digital voice became important services.",

    "Mobile Internet and video calling became available.",

    "LTE provides high-speed mobile broadband.",

    "5G supports massive IoT and ultra-reliable low-latency communication.",

    "Future networks may use AI-native communication and integrated sensing.",

    "Mobile communication provides faster Internet."
]


# ------------------------------------------------------------
# 6. RUN AUTOMATIC TESTS
# ------------------------------------------------------------

test_results = []

print("\n")
print("=" * 70)
print("0G-6G GENERATION RECOMMENDER")
print("=" * 70)

for number, statement in enumerate(test_statements, start=1):

    generation, scores = recommend_generation(statement)

    if generation is None:
        generation = "Ambiguous / Unknown"
        confidence = "Low"
        reason = "No generation-specific keyword was detected."

    elif generation == "Ambiguous":
        confidence = "Low"
        reason = "The statement matched more than one generation."

    else:
        confidence = "Keyword-based"
        reason = f"Matched generation-specific keywords for {generation}."

    print(f"\nTest {number}")
    print("Statement:", statement)
    print("Recommendation:", generation)
    print("Confidence:", confidence)
    print("Reason:", reason)

    test_results.append({
        "Test_Number": number,
        "Statement": statement,
        "Recommended_Generation": generation,
        "Confidence": confidence,
        "Reason": reason
    })


# ------------------------------------------------------------
# 7. SAVE TEST RESULTS
# ------------------------------------------------------------

test_results_df = pd.DataFrame(test_results)

with open("test_results.txt", "w", encoding="utf-8") as file:

    file.write("0G-6G GENERATION RECOMMENDER TEST RESULTS\n")
    file.write("=" * 70 + "\n\n")

    for _, row in test_results_df.iterrows():

        file.write(f"Test {row['Test_Number']}\n")
        file.write(f"Statement: {row['Statement']}\n")
        file.write(
            f"Recommended Generation: "
            f"{row['Recommended_Generation']}\n"
        )
        file.write(f"Confidence: {row['Confidence']}\n")
        file.write(f"Reason: {row['Reason']}\n\n")


# ------------------------------------------------------------
# 8. CREATE RESEARCH TABLE
# ------------------------------------------------------------

research_data = []

for generation, information in generations.items():

    research_data.append({
        "Generation": generation,
        "Period": information["period"],
        "Technology": information["technology"],
        "Features": information["features"],
        "Examples": information["examples"],
        "Services": information["services"],
        "Transition_Problem": information["problem"]
    })


research_df = pd.DataFrame(research_data)

research_df.to_csv(
    "generation_research.csv",
    index=False
)

research_df.to_excel(
    "research_table.xlsx",
    index=False
)


# ------------------------------------------------------------
# 9. INTERACTIVE USER SEARCH
# ------------------------------------------------------------

print("\n")
print("=" * 70)
print("INTERACTIVE 0G-6G DEVICE / TECHNOLOGY SEARCH")
print("=" * 70)

print("""
Now you can enter a device, technology, service, or description.

Examples:
  Nokia 3310
  GSM phone with SMS
  LTE smartphone
  5G IoT sensor
  analog mobile phone
  video calling
  AI-native network
  integrated sensing
  push to talk radio

Type 'list' to see all generations.
Type 'exit' to finish.
""")


while True:

    user_input = input("\nEnter device or communication technology: ")

    user_input = user_input.strip()

    if user_input.lower() == "exit":
        print("\nInteractive search finished.")
        break

    if user_input.lower() == "list":

        print("\nAvailable generations:")

        for generation in generations:
            print(f"  {generation}")

        continue

    if user_input == "":
        print("Please enter something.")
        continue

    generation, scores = recommend_generation(user_input)

    # No match
    if generation is None:

        print("\nNo clear generation was detected.")

        print("Try including information such as:")
        print("GSM, SMS, LTE, 3G, 4G, 5G, 6G, analog, UMTS, etc.")

        continue

    # Ambiguous match
    if generation == "Ambiguous":

        print("\nThe input is ambiguous.")
        print("It matched more than one generation.")

        print("\nKeyword scores:")

        for gen, score in scores.items():

            if score > 0:
                print(f"  {gen}: {score}")

        continue

    # Clear match
    print("\nDetected generation:", generation)

    display_generation_information(generation)


# ------------------------------------------------------------
# 10. FINAL MESSAGE
# ------------------------------------------------------------

print("\n")
print("=" * 70)
print("PROJECT 03 COMPLETED")
print("=" * 70)

print("""
Generated files:

1. test_results.txt
2. generation_research.csv
3. research_table.xlsx

""")