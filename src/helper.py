def Dict_Update(dictionary, words, weight, count_words):
    for word in words:
        if word not in dictionary:
            dictionary[word] = [weight, 0]
        if count_words:
            dictionary[word][1] += 1
    return dictionary