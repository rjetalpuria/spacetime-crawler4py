class TextAnalyzer:
    
    # change according to what kinds of "words" we want
    # currently set to be only 0-9 || A-Z || a-z
    def _is_valid_char(self, char) -> bool:
        val = ord(char[0])
        return 48 <= val <= 57 or 65 <= val <= 90 or 97 <= val <= 122
    
    # takes text string
    # returns list of "words"
    # validity of chars in words defined by _is_valid_char
    def tokenize(self, text : 'str') -> 'list':
        # init list
        tokens = []
        # keep track of characters in a "current token"
        token = []
        # check each character
        for i in range(text):
            # if character is a valid alphanumeric, it's part of a token
            if self._is_valid_char(text[i]):
                # add it to the current token
                token.append(text[i])
            # if it's not, then 2 cases:
            # 1) we have a full token
            elif len(token) > 0:
                # add the token to the list
                tokens.append(''.join(token).lower())
                # start up a new current token
                token = []
            # 2) we have yet to find a new token
            else:
                pass
            # go to the next character
            i += 1
        return tokens
    
    # takes list of tokens
    # returns dict of tokens mapped to frequency in list
    def compute_word_frequencies(self, tokens : 'list') -> 'dict':
        # init dict
        freq = dict()
        # loop through all tokens
        for t in tokens:
            # increment frequency of token (setting to 1 if first occurence)
            freq[t] = freq.get(t, 0) + 1
        return freq

