from itertools import combinations, permutations
from math import comb, factorial


def generate_configurations(n):
    """
    Generate all valid configurations for n particles across n energy levels.

    Rules:
    - Each particle can occupy one energy level.
    - No duplicate particle in the same configuration.
    - No duplicate energy level in the same configuration.

    Formula: sum_{k=1}^{n} C(n,k) * C(n,k) * k!
    """
    particles = [f"p{i}" for i in range(1, n + 1)]
    energy_levels = [f"E{i}" for i in range(n)]

    configurations = []

    for k in range(1, n + 1):
        for chosen_particles in combinations(particles, k):
            for chosen_levels in combinations(energy_levels, k):
                for assigned_levels in permutations(chosen_levels):
                    configuration = tuple(zip(chosen_particles, assigned_levels))
                    configurations.append(configuration)

    return configurations


def format_configuration(configuration):
    pairs = ", ".join(f"({particle}, {energy})" for particle, energy in configuration)
    return "{" + pairs + "}"


def expected_count(n):
    """Closed-form count: sum_{k=1}^{n} C(n,k)^2 * k!"""
    return sum(comb(n, k) ** 2 * factorial(k) for k in range(1, n + 1))


# --- Show configurations for n = 2 ---
n = 2
configurations = generate_configurations(n)

print(f"Configurations for n = {n}:\n")
for i, configuration in enumerate(configurations, start=1):
    print(f"  {i}. {format_configuration(configuration)}")

print(f"\nTotal configurations: {len(configurations)}")
print(f"Formula check:       {expected_count(n)}")

# --- Scale across n = 2..5 ---
print("\nScaling:")
for n in range(2, 6):
    count = len(generate_configurations(n))
    formula = expected_count(n)
    print(f"  n = {n}  →  {count} configurations  (formula: {formula})")
