def levenshtein_distance(first_string, second_string):
    """
    Calculates the Levenshtein distance between two strings.
    Wikipedia: https://en.wikipedia.org/wiki/Levenshtein_distance
    :param first_string: The first string.
    :param second_string: The second string.
    """

    # If the first string is shorter, switch the strings and try again
    if len(first_string) < len(second_string):
        return levenshtein_distance(second_string, first_string)

    # If the second string is empty, the distance is the length of the first string
    if len(second_string) == 0:
        return len(first_string)

    # Create a list to store the previous row of distances
    previous_row = range(len(second_string) + 1)
    for i, first_char in enumerate(first_string):
        # Create a list to store the current row of distances
        current_row = [i + 1]

        # Calculate the minimum distance for each position
        for j, second_char in enumerate(second_string):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (first_char != second_char)
            current_row.append(min(insertions, deletions, substitutions))

        # Update the previous row
        previous_row = current_row

    # Return the last element of the previous row
    return previous_row[-1]