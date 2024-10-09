import numpy as np
import random

def run_simulation_v4():
    x = 1000  # number of rows
    y = 1000  # number of columns
    worlds = np.random.choice([0, 1], size=(x, y))  # Create a 1000x1000 grid with p randomly assigned

    results = []
    num_simulations = 5  # Number of simulations to run

    for _ in range(num_simulations):
        while True:
            # Alice's and Bob's opinions
            alice_threshold = random.uniform(0, 1)  # Alice's threshold for p being true in her row
            alice_opinion = "greater" if random.random() < 0.5 else "less"
            
            bob_threshold = random.uniform(0, 1)  # Bob's threshold for p being true in his column
            bob_opinion = "greater" if random.random() < 0.5 else "less"

            # Step 4: Filter the worlds based on Alice's and Bob's opinions
            if alice_opinion == "greater":
                alice_rows = [i for i in range(x) if np.mean(worlds[i, :]) >= alice_threshold]
            else:
                alice_rows = [i for i in range(x) if np.mean(worlds[i, :]) <= alice_threshold]

            if bob_opinion == "greater":
                bob_columns = [j for j in range(y) if np.mean(worlds[:, j]) >= bob_threshold]
            else:
                bob_columns = [j for j in range(y) if np.mean(worlds[:, j]) <= bob_threshold]

            # Step 5: Combine Alice's and Bob's knowledge to locate the remaining worlds
            if not alice_rows or not bob_columns:
                remaining_worlds = []
            else:
                remaining_worlds = [(i, j) for i in alice_rows for j in bob_columns]

            # Step 6: Calculate the conditional probability that p is true given each expert's opinion
            if len(remaining_worlds) > 0:
                alice_conditional_prob = np.mean([worlds[i, j] for i, j in remaining_worlds])
                bob_conditional_prob = alice_conditional_prob
            else:
                alice_conditional_prob = 0
                bob_conditional_prob = 0

            # Ensure that Alice and Bob's conditional beliefs do not reduce their thresholds
            alice_condition_met = (alice_opinion == "greater" and alice_conditional_prob >= alice_threshold) or \
                                 (alice_opinion == "less" and alice_conditional_prob <= alice_threshold)

            bob_condition_met = (bob_opinion == "greater" and bob_conditional_prob >= bob_threshold) or \
                               (bob_opinion == "less" and bob_conditional_prob <= bob_threshold)

            # If both conditions are met, break the loop
            if alice_condition_met and bob_condition_met:
                break

        # Step 7: Calculate the probability that p is true in the remaining worlds
        if len(remaining_worlds) == 0:
            probability_p_true = 0  # No remaining worlds, p can't be true
        else:
            true_worlds = sum([worlds[i, j] for i, j in remaining_worlds])
            probability_p_true = true_worlds / len(remaining_worlds)

        # Collect the results for this simulation
        results.append({
            "alice_opinion": f"p {'≥' if alice_opinion == 'greater' else '≤'} {alice_threshold:.3f} in selected rows",
            "bob_opinion": f"p {'≥' if bob_opinion == 'greater' else '≤'} {bob_threshold:.3f} in selected columns",
            "remaining_worlds_count": len(remaining_worlds),
            "probability_p_true": probability_p_true,
            "alice_condition_maintained": alice_condition_met,
            "alice_conditional_probability": alice_conditional_prob,
            "bob_condition_maintained": bob_condition_met,
            "bob_conditional_probability": bob_conditional_prob
        })

    # Output the results for all simulations
    for idx, result in enumerate(results, 1):
        print(f"\nSimulation {idx} Results:")
        print(result["alice_opinion"])
        print(result["bob_opinion"])
        print(f"Remaining worlds count: {result['remaining_worlds_count']}")
        print(f"Probability that p is true in the remaining worlds: {result['probability_p_true']}")
        print(f"Alice's condition maintained: {result['alice_condition_maintained']}, Probability for Alice: {result['alice_conditional_probability']}")
        print(f"Bob's condition maintained: {result['bob_condition_maintained']}, Probability for Bob: {result['bob_conditional_probability']}")

# Run the simulation
run_simulation_v4()