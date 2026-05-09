from itertools import product


def format_ket(state: tuple) -> str:
    """Format a state tuple as a Unicode ket: |v1,v2,...,vn⟩"""
    return "|" + ",".join(str(x) for x in state) + "⟩"


def generate_basis_states(num_modes: int, max_vibration: int) -> list:
    """
    Generate per-mode cutoff basis states.

    Each mode vi can independently hold 0..max_vibration quanta.
    Returns all states |v1,...,vn⟩ as Unicode ket strings.

    Total count = (max_vibration + 1) ** num_modes.
    """
    if num_modes <= 0:
        raise ValueError("num_modes must be a positive integer")
    if max_vibration < 0:
        raise ValueError("max_vibration must be >= 0")

    return [
        format_ket(state)
        for state in product(range(max_vibration + 1), repeat=num_modes)
    ]


def count_basis_states(num_modes: int, max_vibration: int) -> int:
    """
    Count per-mode cutoff basis states.

    Formula: (max_vibration + 1) ** num_modes
    """
    if num_modes <= 0:
        raise ValueError("num_modes must be a positive integer")
    if max_vibration < 0:
        raise ValueError("max_vibration must be >= 0")

    return (max_vibration + 1) ** num_modes


if __name__ == "__main__":
    num_modes = 3
    max_vibration = 2
    basis_states = generate_basis_states(num_modes, max_vibration)

    print(f"{len(basis_states)} basis states for n = {num_modes}; max vibration per mode = {max_vibration}")
    print(f"Formula: ({max_vibration}+1)^{num_modes} = {count_basis_states(num_modes, max_vibration)}")
    print()
    for i, state in enumerate(basis_states, start=1):
        print(f"  {i}. {state}")

    print("\nScaling table:")
    for n, v in [(2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 2)]:
        count = count_basis_states(n, v)
        print(f"  n={n}, v={v}  ->  ({v}+1)^{n} = {count} states")
