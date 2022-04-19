stopwords = { "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves" }

def validate(word): # O(n) where n is the length of the word
    valid_last_chars = ['.', ',', ';', ':', '?', '!', '\"', '\'']
    begin_punct = False
    end_punct = False
    double_end_punct = False
    for i,c in enumerate(word):
        # check if the character is alphaneumeric
        if (c >= '0' and c <= '9') or (c >= 'A' and c <= 'Z') or (c >= 'a' and c <= 'z'):
            continue
        # if it is the last character, and it is a valid ending character, then it token is valid w/o it
        # ex: 'Hello, world' --> here 'Hello,' ends with a comma, so 'Hello' (w/o comma) is valid
        elif (i == len(word)-1) and (c in valid_last_chars):
            end_punct = True
        # sentences with quotations generally end with a punctuation followed by quotes, so we need
        # to remove 2 punctions from the last word
        # ex: Bob said, "This is cool." --> here 'cool."' has 2 punctuations and so the valid token is 'cool'
        elif (i == len(word)-2) and (c in valid_last_chars) and (word[i+1] in ['\"', '\'']):
            double_end_punct = True
        # sentences with quotations also have a starting quote attached with the first word, so we
        # need to remove those from the word to get a valid token
        # ex: Bob said, "This is cool." --> here '"This' has a quote attached to it and 'This' is valid
        # also just a quote by itself is not a valid token, so we make sure that the word length > 1
        elif (i == 0 and len(word) > 1) and (c in ['\"', '\'']):
            begin_punct = True
        # check for hypenated words
        # also hypen is not a valid starting or ending character so we need to check for that
        elif (i != 0 and i != len(word)-1) and (c == '-'):
            continue;
        # if it is none of the conditions above, we return false
        else:
            return False;
    
    if double_end_punct:
        word = word[:-2] # remove 2 chars from the back
    elif end_punct:
        word = word[:-1] # remove 1 char from the back
    if begin_punct:
        word = word[1:] # remove 1 char from the front
    word = word.lower()
    if word in stopwords:
        return False
    return word


# Read the file line-by-line and process each word and return a list of valid alphanumeric 
# tokens found in the file
def tokenize(file): # O(w * n) = O(w) where w is the number of words in the file and n is the length of the word
    words = []
    for line in file: # read file line-by-line
        for word in line.split(): # process each line word-by-word
            result = validate(word) # validate each word
            if result != False: # if the word is valid
                words.append(result) #append word to the list
    return words

# returns a dictionary filled with words as key and their frequency as their value
def computeWordFrequencies(words): # O(w) where w is the number of words in the file
    freq = {}
    for word in words:
        if word in freq.keys(): # if the word is already in the dictionary
            freq[word] = freq[word] + 1
        else: # word is not in dictionary, create a new key, value pair
            freq[word] = 1
    return freq

# prints the words and frequencies in a sorted descendingly based on values and breaking ties
# with alphabetical order
def printFreq(frequencies): # O(m log m) where m is the number of unique words in the file
    frequencies = dict(sorted(frequencies.items())) # sort by alphabetical order first
    # sort by frequency in descending order
    frequencies = dict(sorted(frequencies.items(), key=lambda tup: tup[1], reverse=True)) 
    # print
    for word, freq in frequencies.items(): 
        print(word + "\t" + str(freq))


