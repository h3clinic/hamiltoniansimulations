from itertools import combinations, permutations
from math import comb, factorial


def generate_states(n):
    """
    Generate all valid configurations for n particles across n energy levels.

    Rules:
    - Each particle can occupy one energy level.
    - No duplicate particle in the same configuration.
    - No duplicate energy level in the same configuration.

    Formula: sum_{k=1}^{n} C(n,k) * C(n,k) * k!
    """
    particles = list(range(1, n + 1))
    energy_levels = list(range(n))

    states = []

    for size in range(1, n + 1):
        for chosen_particles in combinations(particles, size):
            for chosen_levels in combinations(energy_levels, size):
                for level_order in permutations(chosen_levels):
                    state = tuple(zip(chosen_particles, level_order))
                    states.append(state)

    return states


def expected_count(n):
    """Closed-form count: sum_{k=1}^{n} C(n,k)^2 * k!"""
    return sum(comb(n, k) ** 2 * factorial(k) for k in range(1, n + 1))


# --- Show states for n = 2 ---
n = 2
states = generate_states(n)

print(f"States for n = {n}:\n")
for i, state in enumerate(states, start=1):
    print(f"  {i}. {state}")

print(f"\nTotal possibilities: {len(states)}")
print(f"Formula check:       {expected_count(n)}")

# --- Scale across n = 2..5 ---
print("\nScaling:")
for n in range(2, 6):
    count = len(generate_states(n))
    formula = expected_count(n)
    print(f"  n = {n}  →  {count}  (formula: {formula})")
