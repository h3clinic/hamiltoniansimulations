from itertools import combinations, permutations
from math import comb, factorial


def generate_basis_states(n, max_vibration=None):
    """
    Generate basis states |particle,vibration⟩.

    Rules:
    - particles/sites are 1..n.
    - vibrations are 0..max_vibration.
    - each basis state uses distinct particles.
    - each basis state uses distinct vibration levels.
    - all occupancies k = 1..min(n, max_vibration + 1) are included.
    - particles remain in ascending order; vibration assignments are permuted.
    """
    if max_vibration is None:
        max_vibration = n - 1

    particles = list(range(1, n + 1))
    vibrations = list(range(0, max_vibration + 1))
    max_occupancy = min(len(particles), len(vibrations))

    basis_states = []

    for k in range(1, max_occupancy + 1):
        for chosen_particles in combinations(particles, k):
            for chosen_vibrations in combinations(vibrations, k):
                for vibration_order in permutations(chosen_vibrations):
                    basis_state = tuple(zip(chosen_particles, vibration_order))
                    basis_states.append(basis_state)

    return basis_states


def format_basis_state(basis_state):
    entries = []

    for index, (particle, level) in enumerate(basis_state):
        particle_label = f"{particle}'" if index > 0 else str(particle)
        entries.append(f"{particle_label},{level}")

    return "|" + ";".join(entries) + "⟩"


def expected_count(n, max_vibration=None):
    """Count basis states: Σ C(n,k) C(max_vibration+1,k) k!."""
    if max_vibration is None:
        max_vibration = n - 1

    max_occupancy = min(n, max_vibration + 1)
    return sum(
        comb(n, k) * comb(max_vibration + 1, k) * factorial(k)
        for k in range(1, max_occupancy + 1)
    )


if __name__ == "__main__":
    n = 2
    max_vibration = n - 1
    basis_states = generate_basis_states(n, max_vibration)

    print(f"Basis states for n = {n}, max vibration = {max_vibration}:\n")
    for i, basis_state in enumerate(basis_states, start=1):
        print(f"  {i}. {format_basis_state(basis_state)}")

    print(f"\nTotal states: {len(basis_states)}")
    print(f"Formula check:       {expected_count(n, max_vibration)}")

    print("\nScaling:")
    for n in range(2, 6):
        max_vibration = n - 1
        count = len(generate_basis_states(n, max_vibration))
        formula = expected_count(n, max_vibration)
        print(f"  n = {n}, max vibration = {max_vibration}  →  {count} states  (formula: {formula})")
