## Helper Function For determining co-occurences

def co_check(word1, word2, input_text):
    if word1 in input_text and word2 in input_text:
        return 1
    else:
        return 0