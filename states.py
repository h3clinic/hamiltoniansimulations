from itertools import combinations, product


def generate_basis_states(n, max_total_vibration=None):
    """
    Generate all valid basis states for n particles across configurable vibrational levels.

    Rules:
    - Each particle can occupy vibration levels 0..max_total_vibration.
    - No duplicate particle in the same basis state.
    - Vibrational levels can repeat across different particles.
    - Include only single states and pairwise mixed states.
    - Total vibrational excitation in one basis state is configurable.
    - Pairwise mixed states with no vibration are redundant and removed.

    For n = 3, |1,1;3',1⟩ is valid because 1 + 1 = 2,
    while |1,1;3',2⟩ is excluded when max_total_vibration = 2.
    Also, |1,0;2',0⟩ is excluded because it carries no mixed vibration.
    """
    if max_total_vibration is None:
        max_total_vibration = n - 1

    particles = list(range(1, n + 1))
    vibration_levels = list(range(max_total_vibration + 1))

    basis_states = []

    for k in range(1, min(n, 2) + 1):
        for chosen_particles in combinations(particles, k):
            for assigned_levels in product(vibration_levels, repeat=k):
                if sum(assigned_levels) > max_total_vibration:
                    continue
                if is_redundant_mixed_state(assigned_levels):
                    continue
                basis_state = tuple(zip(chosen_particles, assigned_levels))
                basis_states.append(basis_state)

    return basis_states


def is_redundant_mixed_state(assigned_levels):
    """A mixed state with all zero vibrations adds no new basis state."""
    return len(assigned_levels) > 1 and all(level == 0 for level in assigned_levels)


def format_basis_state(basis_state):
    ordered_pairs = sorted(basis_state, key=lambda pair: pair[1]) if len(basis_state) > 1 else basis_state
    entries = []

    for index, (particle, level) in enumerate(ordered_pairs):
        particle_label = f"{particle}'" if index > 0 else str(particle)
        entries.append(f"{particle_label},{level}")

    return "|" + ";".join(entries) + "⟩"


def expected_count(n, max_total_vibration=None):
    """Count pairwise basis states with configurable total vibrational cap."""
    if max_total_vibration is None:
        max_total_vibration = n - 1

    return len(generate_basis_states(n, max_total_vibration))


if __name__ == "__main__":
    n = 2
    max_total_vibration = n - 1
    basis_states = generate_basis_states(n, max_total_vibration)

    print(f"Basis states for n = {n}, max total vibration = {max_total_vibration}:\n")
    for i, basis_state in enumerate(basis_states, start=1):
        print(f"  {i}. {format_basis_state(basis_state)}")

    print(f"\nTotal states: {len(basis_states)}")
    print(f"Formula check:       {expected_count(n, max_total_vibration)}")

    print("\nScaling:")
    for n in range(2, 6):
        max_total_vibration = n - 1
        count = len(generate_basis_states(n, max_total_vibration))
        formula = expected_count(n, max_total_vibration)
        print(f"  n = {n}, max vibration = {max_total_vibration}  →  {count} states  (formula: {formula})")
