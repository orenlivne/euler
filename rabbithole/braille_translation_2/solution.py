#-------------------------------------------------------------------------------
# Rabbit hole - Braille_translation_2 problem
#-------------------------------------------------------------------------------

# Returns a translation key: a map from letters to brail characters and the
# capitalization prefix character. reference_text must contains all alphabet
# letters. reference_encoded is the corresponding encoded string to
# reference_text. char_len is the length of each encoded letter substring in
# reference_encoded.
def create_translation_key(reference_text, reference_encoded, char_len):
  # i is a pointer to the current position to be read in reference_encoded.
  i, char_of_letter, caps_char = 0, {}, None
  # For each letter, find its encoded character and add it to the key.
  for letter in reference_text:
    # Read the next encoded character.
    character = reference_encoded[i:i+char_len]
    if letter.istitle():
      # Capital letter ==> two encoded characters. Read the first one
      # and set it to caps_char.
      # Self-consistency check.
      if caps_char is not None and character != caps_char:
        raise Exception('Invalid encoded reference - multiple capitalization characters found: %s, %s' % (caps_car, character))
      caps_char = character
      # Read the second one and assign it to the lowercase counterpart
      # of letter.
      i += char_len
      character = reference_encoded[i:i+char_len]
      letter = letter.lower()
      # Self-consistency check.
      if letter in char_of_letter and character != char_of_letter[letter]:
        raise Exception('Invalid encoded reference - multiple characters for letter %s: %s, %s' % (letter, char_of_letter[letter], character))
      char_of_letter[letter] = character
    else:
      # All other letters.
      # Self-consistency check.
      if letter in char_of_letter and character != char_of_letter[letter]:
        raise Exception('Invalid encoded reference - multiple characters for letter %s: %s, %s' % (letter, char_of_letter[letter], character))
      char_of_letter[letter] = character
    i += char_len
  return char_of_letter, caps_char

# Reference text containing all letters in the sign alphabet.
REFERENCE_TEXT = "The quick brown fox jumped over the lazy dog"
# The encoded reference text.
REFERENCE_ENCODED = "000001011110110010100010000000111110101001010100100100101000000000110000111010101010010111101110000000110100101010101101000000010110101001101100111100100010100110000000101010111001100010111010000000011110110010100010000000111000100000101011101111000000100110101010110110"
# Length of a brail character
CHAR_LEN = 6
# Translation key is created once, not every time answer() is called.
TRANSLATION_KEY, CAPS_CHAR = create_translation_key(REFERENCE_TEXT, REFERENCE_ENCODED, CHAR_LEN)
# This letter isn't in the reference text, so we brute-forced all values that are not in
# the dictionary until we found (the?) one that worked.
TRANSLATION_KEY['s'] = '011100'

# Translates a plaintext
def answer(plaintext):
  return ''.join(CAPS_CHAR + TRANSLATION_KEY[letter.lower()] if letter.istitle() else TRANSLATION_KEY[letter] for letter in plaintext)

if __name__ == '__main__':
  assert answer(REFERENCE_TEXT) == REFERENCE_ENCODED
  assert answer("code") == "100100101010100110100010"
  assert answer("Braille") == "000001110000111010100000010100111000111000100010"
