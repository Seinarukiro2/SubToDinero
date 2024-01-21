def levenshtein_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for index2, char2 in enumerate(s2):
        new_distances = [index2 + 1]
        for index1, char1 in enumerate(s1):
            if char1 == char2:
                new_distances.append(distances[index1])
            else:
                new_distances.append(1 + min((distances[index1], distances[index1 + 1], new_distances[-1])))
        distances = new_distances

    return distances[-1]

def get_similar_channel_names(db: Session, input_name: str, max_distance=3):
    all_channel_names = [channel.name for channel in get_all_channels(db)]
    similar_names = []

    for channel_name in all_channel_names:
        distance = levenshtein_distance(input_name.lower(), channel_name.lower())
        if distance <= max_distance:
            similar_names.append((channel_name, distance))

    similar_names.sort(key=lambda x: x[1])
    return similar_names
