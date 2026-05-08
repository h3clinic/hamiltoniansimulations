from itertools import product


def generate_basis_states(n, max_vibration=None):
    """
    Generate occupation-number (Fock) basis states |n₁,n₂,...,nₙ⟩.

    Each mode can hold 0..max_vibration quanta.
    Total states = (max_vibration + 1) ** n.
    """
    if max_vibration is None:
        max_vibration = n - 1

    basis_states = []
    for occupations in product(range(max_vibration + 1), repeat=n):
        state = "|" + ",".join(str(x) for x in occupations) + "⟩"
        basis_states.append(state)
    return basis_states


def count_basis_states(n, max_vibration=None):
    """Count Fock basis states: (max_vibration + 1) ** n."""
    if max_vibration is None:
        max_vibration = n - 1
    return (max_vibration + 1) ** n


def expected_count(n, max_vibration=None):
    return count_basis_states(n, max_vibration)


if __name__ == "__main__":
    n = 3
    max_vibration = 2
    basis_states = generate_basis_states(n, max_vibration)

    print(f"{len(basis_states)} basis states for n = {n}; max vibration = {max_vibration}")
    for i, state in enumerate(basis_states, start=1):
        print(f"{i}. {state}")

    print("\nScaling:")
    for n in range(2, 6):
        max_vibration = n - 1
        count = count_basis_states(n, max_vibration)
        print(f"  n = {n}, max vibration = {max_vibration}  →  {count} states")
