from itertools import combinations, permutations
from math import comb, factorial


def generate_basis_states(n):
    """
    Generate all valid basis states for n particles across n energy levels.

    Rules:
    - Each particle can occupy one energy level.
    - No duplicate particle in the same basis state.
    - No duplicate energy level in the same basis state.

    Formula: sum_{k=1}^{n} C(n,k) * C(n,k) * k!
    """
    particles = list(range(1, n + 1))
    energy_levels = list(range(n))

    basis_states = []

    for k in range(1, n + 1):
        for chosen_particles in combinations(particles, k):
            for chosen_levels in combinations(energy_levels, k):
                for assigned_levels in permutations(chosen_levels):
                    basis_state = tuple(zip(chosen_particles, assigned_levels))
                    basis_states.append(basis_state)

    return basis_states


def format_basis_state(basis_state):
    ordered_pairs = sorted(basis_state, key=lambda pair: pair[1]) if len(basis_state) > 1 else basis_state
    entries = []

    for index, (particle, level) in enumerate(ordered_pairs):
        particle_label = f"{particle}'" if index > 0 else str(particle)
        entries.append(f"{particle_label},{level}")

    return "|" + ";".join(entries) + "⟩"


def expected_count(n):
    """Closed-form count: sum_{k=1}^{n} C(n,k)^2 * k!"""
    return sum(comb(n, k) ** 2 * factorial(k) for k in range(1, n + 1))


# --- Show basis states for n = 2 ---
n = 2
basis_states = generate_basis_states(n)

print(f"Basis states for n = {n}:\n")
for i, basis_state in enumerate(basis_states, start=1):
    print(f"  {i}. {format_basis_state(basis_state)}")

print(f"\nTotal states: {len(basis_states)}")
print(f"Formula check:       {expected_count(n)}")

# --- Scale across n = 2..5 ---
print("\nScaling:")
for n in range(2, 6):
    count = len(generate_basis_states(n))
    formula = expected_count(n)
    print(f"  n = {n}  →  {count} states  (formula: {formula})")
