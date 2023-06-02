def generate_strings(d, l):
    def generate_strings_rec(d, l, idx, current, remaining):
        # If this is the last group of ones
        if idx == len(d):
            # If the remaining cells can be filled with zeros
            if remaining >= 0:
                yield current + [0] * remaining
            return
        # Generate all possible numbers of zeros before this group
        # Should be at least one zero between groups of ones if it is not the first group
        for zeros in range(1 if idx > 0 else 0, remaining - d[idx] + 1):
            yield from generate_strings_rec(d, l, idx + 1, current + [0] * zeros + [1] * d[idx], remaining - zeros - d[idx])

    return [''.join(map(str, b)) for b in generate_strings_rec(d, l, 0, [], l)]

# Uncomment the line below to run the test
#test_generate_strings()

def test_generate_strings():
    # Test with one clue
    d = [1]
    l = 5
    expected_result = ['10000', '01000', '00100', '00010', '00001']
    assert sorted(generate_strings(d, l)) == sorted(expected_result)

    # Test with two clues
    d = [1, 1]
    l = 5
    expected_result = ['10010', '10001', '01001', '10100', '00101', '01010']
    assert sorted(generate_strings(d, l)) == sorted(expected_result)

    # Test with inconsistent description
    d = [3, 3]
    l = 5
    assert generate_strings(d, l) == []

    # Test with multiple clues
    d = [2, 3, 1]
    l = 10
    expected_result = ['1101110100', '1101110010', '1101110001', '1100111010', '1100111001', '1100011101', '0110111010', '0110111001', '0110011101', '0011011101']
    assert sorted(generate_strings(d, l)) == sorted(expected_result)

test_generate_strings()  # Uncomment this line to run the test
