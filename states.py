from itertools import combinations, product
from math import comb


def generate_basis_states(n):
    """
    Generate all valid basis states for n particles across n vibrational levels.

    Rules:
    - Each particle can occupy one vibrational level.
    - No duplicate particle in the same basis state.
    - Vibrational levels can repeat across different particles.
    - Include only single states and pairwise mixed states.
    - Total vibrational excitation in one basis state is at most n - 1.

    For n = 3, |1,1;3',1⟩ is valid because 1 + 1 = 2,
    while |1,1;3',2⟩ is excluded because 1 + 2 = 3.
    """
    particles = list(range(1, n + 1))
    vibration_levels = list(range(n))
    max_total_vibration = n - 1

    basis_states = []

    for k in range(1, min(n, 2) + 1):
        for chosen_particles in combinations(particles, k):
            for assigned_levels in product(vibration_levels, repeat=k):
                if sum(assigned_levels) > max_total_vibration:
                    continue
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
    """Count states with total vibrational excitation <= n - 1."""
    return sum(comb(n, k) * comb((n - 1) + k, k) for k in range(1, min(n, 2) + 1))


if __name__ == "__main__":
    n = 2
    basis_states = generate_basis_states(n)

    print(f"Basis states for n = {n}:\n")
    for i, basis_state in enumerate(basis_states, start=1):
        print(f"  {i}. {format_basis_state(basis_state)}")

    print(f"\nTotal states: {len(basis_states)}")
    print(f"Formula check:       {expected_count(n)}")

    print("\nScaling:")
    for n in range(2, 6):
        count = len(generate_basis_states(n))
        formula = expected_count(n)
        print(f"  n = {n}  →  {count} states  (formula: {formula})")
