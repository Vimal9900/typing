"""
Kruti Dev <-> Unicode Devanagari Converter
Handles bidirectional conversion between legacy Kruti Dev font and Unicode
"""

# Kruti Dev to Unicode mapping
# Based on common Kruti Dev 010 mappings
KRUTI_TO_UNICODE = {
    # Vowels
    'v': 'अ', 'v]': 'आ', 'b': 'इ', 'bZ': 'ई', 'm': 'उ', 'Å': 'ऊ', 
    ',': 'ए', ',s': 'ऐ', 'v¨': 'ओ', 'v©': 'औ',
    
    # Consonants
    'd': 'क', '[k': 'ख', 'x': 'ग', '?k': 'घ', 
    'p': 'च', 'N': 'छ', 't': 'ज', 'T': 'झ', 
    'V': 'ट', 'B': 'ठ', 'M': 'ड', 'Z': 'ढ', '.k': 'ण',
    'r': 'त', 'Fk': 'थ', 'n': 'द', 'èk': 'ध', 'u': 'न',
    'i': 'प', 'Q': 'फ', 'c': 'ब', 'Hk': 'भ', 'e': 'म',
    ';': 'य', 'j': 'र', 'y': 'ल', 'o': 'व',
    'k': 'श', 'K': 'ष', 'l': 'स', 'g': 'ह',
    
    # Special characters
    'K': 'क्ष', 'F': 'त्र', 'K': 'ज्ञ',
    
    # Matras (vowel signs)
    'k': 'ा', 'h': 'ि', 'hZ': 'ी', 'q': 'ु', 'w': 'ू',
    's': 'े', 'S': 'ै', 'ks': 'ो', 'kS': 'ौ',
    'a': 'ं', 'H': 'ः',
    
    # Half forms and conjuncts (common ones)
    '~': '्',  # Halant
}

# Reverse mapping for Unicode to Kruti Dev
UNICODE_TO_KRUTI = {v: k for k, v in KRUTI_TO_UNICODE.items()}

# Additional complex mappings
COMPLEX_KRUTI_TO_UNICODE = {
    'dk': 'का', 'dh': 'कि', 'dh': 'की', 'dq': 'कु', 'dw': 'कू',
    'ds': 'के', 'dS': 'कै', 'dk¨': 'को', 'dk©': 'कौ',
    '[kk': 'खा', '[kh': 'खि', 
    'xk': 'गा', 'xh': 'गि',
    'rk': 'ता', 'rh': 'ति', 'rh': 'ती', 'rq': 'तु', 'rw': 'तू',
    # Add more as needed
}

def kruti_to_unicode(text):
    """
    Convert Kruti Dev encoded text to Unicode Devanagari
    
    Args:
        text: String in Kruti Dev encoding
        
    Returns:
        String in Unicode Devanagari
    """
    result = []
    i = 0
    
    while i < len(text):
        # Try to match longer sequences first (for complex characters)
        matched = False
        
        # Try 3-character matches
        if i + 2 < len(text):
            three_char = text[i:i+3]
            if three_char in COMPLEX_KRUTI_TO_UNICODE:
                result.append(COMPLEX_KRUTI_TO_UNICODE[three_char])
                i += 3
                matched = True
        
        # Try 2-character matches
        if not matched and i + 1 < len(text):
            two_char = text[i:i+2]
            if two_char in KRUTI_TO_UNICODE:
                result.append(KRUTI_TO_UNICODE[two_char])
                i += 2
                matched = True
            elif two_char in COMPLEX_KRUTI_TO_UNICODE:
                result.append(COMPLEX_KRUTI_TO_UNICODE[two_char])
                i += 2
                matched = True
        
        # Try single character match
        if not matched:
            char = text[i]
            if char in KRUTI_TO_UNICODE:
                result.append(KRUTI_TO_UNICODE[char])
            else:
                # Keep character as-is if no mapping found
                result.append(char)
            i += 1
    
    return ''.join(result)

def unicode_to_kruti(text):
    """
    Convert Unicode Devanagari text to Kruti Dev encoding
    
    Args:
        text: String in Unicode Devanagari
        
    Returns:
        String in Kruti Dev encoding
    """
    result = []
    
    for char in text:
        if char in UNICODE_TO_KRUTI:
            result.append(UNICODE_TO_KRUTI[char])
        else:
            # Keep character as-is if no mapping found
            result.append(char)
    
    return ''.join(result)

def detect_encoding(text):
    """
    Detect if text is in Kruti Dev or Unicode
    
    Args:
        text: String to detect
        
    Returns:
        'unicode' or 'kruti'
    """
    # Check for Devanagari Unicode range (0x0900-0x097F)
    devanagari_count = sum(1 for char in text if '\u0900' <= char <= '\u097F')
    
    # Check for common Kruti Dev characters
    kruti_chars = set(KRUTI_TO_UNICODE.keys())
    kruti_count = sum(1 for char in text if char in kruti_chars)
    
    if devanagari_count > len(text) * 0.3:
        return 'unicode'
    elif kruti_count > len(text) * 0.3:
        return 'kruti'
    else:
        return 'unknown'

def smart_convert(text, target='unicode'):
    """
    Smart conversion - detects source encoding and converts to target
    
    Args:
        text: Input text
        target: Target encoding ('unicode' or 'kruti')
        
    Returns:
        Converted text
    """
    detected = detect_encoding(text)
    
    if target == 'unicode':
        if detected == 'kruti':
            return kruti_to_unicode(text)
        else:
            return text
    elif target == 'kruti':
        if detected == 'unicode':
            return unicode_to_kruti(text)
        else:
            return text
    
    return text

# Extended Kruti Dev mappings for better coverage
EXTENDED_KRUTI_MAPPINGS = {
    # Numbers
    '0': '०', '1': '१', '2': '२', '3': '३', '4': '४',
    '5': '५', '6': '६', '7': '७', '8': '८', '9': '९',
    
    # Additional consonants and combinations
    'Ø': 'क्क', '×': 'क्त', 'Ù': 'क्र', '¿': 'क्ष',
    'Úk': 'क्षा', 'Û': 'ख्', 'Ü': 'ग्',
    'Pð': 'छ्', 'Ý': 'ज्ञ', 'Þ': 'ट्',
    'ß': 'ठ्', 'à': 'ड्', 'á': 'ढ्', 'â': 'ण्',
    'ã': 'त्त', 'ä': 'त्र', 'å': 'थ्', 'æ': 'द्',
    'ç': 'द्ध', 'è': 'द्य', 'é': 'द्व', 'ê': 'न्',
    'ë': 'प्', 'ì': 'फ्', 'í': 'ब्', 'î': 'भ्',
    'ï': 'म्', 'ð': 'य्', 'ñ': 'र्', 'ò': 'ल्',
    'ó': 'व्', 'ô': 'श्', 'õ': 'ष्', 'ö': 'स्',
    '÷': 'ह्', '¸': 'ह्न', '¹': 'ह्म', 'º': 'ह्य',
}

# Update main mappings with extended ones
KRUTI_TO_UNICODE.update(EXTENDED_KRUTI_MAPPINGS)
UNICODE_TO_KRUTI.update({v: k for k, v in EXTENDED_KRUTI_MAPPINGS.items()})

if __name__ == '__main__':
    # Test the converter
    test_unicode = 'नमस्ते भारत'
    test_kruti = 'ueLrs Hkkjr'
    
    print("Testing Kruti Dev Converter")
    print("="*50)
    print(f"\nOriginal Unicode: {test_unicode}")
    converted_to_kruti = unicode_to_kruti(test_unicode)
    print(f"Converted to Kruti: {converted_to_kruti}")
    
    print(f"\nOriginal Kruti: {test_kruti}")
    converted_to_unicode = kruti_to_unicode(test_kruti)
    print(f"Converted to Unicode: {converted_to_unicode}")
    
    print(f"\nDetected encoding of '{test_unicode}': {detect_encoding(test_unicode)}")
    print(f"Detected encoding of '{test_kruti}': {detect_encoding(test_kruti)}")
