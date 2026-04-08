import json
import os

# Base directory relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(BASE_DIR, "en_to_si.json")
HTML_OUTPUT = os.path.join(BASE_DIR, "dictionary.html")
OPF_OUTPUT = os.path.join(BASE_DIR, "kindle_dict.opf")

def sinhala_to_singlish(text):
    """An improved Sinhala to Singlish transliterator."""
    # Special characters
    specials = {
        'ං': 'n',
        'ඃ': 'h',
        '෴': '.',
    }
    
    vowels = {
        'අ': 'a', 'ආ': 'aa', 'ඇ': 'ae', 'ඈ': 'aee', 'ඉ': 'i', 'ඊ': 'ii', 'උ': 'u', 'ඌ': 'uu',
        'එ': 'e', 'ඒ': 'ee', 'ඓ': 'ai', 'ඔ': 'o', 'ඕ': 'oo', 'ඖ': 'au',
        'ඍ': 'ru', 'ඎ': 'ruu'
    }
    
    consonants = {
        'ක': 'ka', 'ඛ': 'kha', 'ග': 'ga', 'ඝ': 'gha', 'ඞ': 'nga', 'ඟ': 'nga',
        'ච': 'cha', 'ඡ': 'chha', 'ජ': 'ja', 'ඣ': 'jha', 'ඤ': 'nya', 'ඥ': 'jnya', 'ඦ': 'nja',
        'ට': 'ta', 'ඨ': 'tha', 'ඩ': 'da', 'ඪ': 'dha', 'ණ': 'na', 'ඬ': 'nda',
        'ත': 'tha', 'ථ': 'thha', 'ද': 'da', 'ධ': 'dha', 'න': 'na', 'ඳ': 'nda',
        'ප': 'pa', 'ඵ': 'pha', 'බ': 'ba', 'භ': 'bha', 'ම': 'ma', 'ඹ': 'mba',
        'ය': 'ya', 'ර': 'ra', 'ල': 'la', 'ව': 'wa', 'ශ': 'sha', 'ෂ': 'sha', 'ස': 'sa', 'හ': 'ha', 'ළ': 'la', 'ෆ': 'fa'
    }
    
    modifiers = {
        'ා': 'aa', 'ැ': 'ae', 'ෑ': 'aee', 'ි': 'i', 'ී': 'ii', 'ු': 'u', 'ූ': 'uu', 'ෙ': 'e', 'ේ': 'ee', 'ෛ': 'ai', 'ො': 'o', 'ෝ': 'oo', 'ෞ': 'au',
        '්': '', 'ෘ': 'ru', 'ෲ': 'ruu', 'ෟ': 'lu', 'ෳ': 'luu'
    }

    # Complex symbols like Zero Width Joiner
    complex_symbols = {
        '\u200d': '', # Zero Width Joiner - ignore
        '\u200c': '', # Zero Width Non-Joiner - ignore
    }

    result = ""
    i = 0
    while i < len(text):
        char = text[i]
        
        if char in specials:
            result += specials[char]
        elif char in vowels:
            result += vowels[char]
        elif char in consonants:
            stem = consonants[char][:-1] # remove the 'a'
            
            # Look ahead for modifiers
            next_char = text[i+1] if i+1 < len(text) else ""
            
            # Handle composite modifiers (e.g., ෙ + ා = o)
            if next_char == '\u0dca': # Halkirima
                result += stem
                i += 1
            elif next_char == '\u0dd9' and i+2 < len(text) and text[i+2] == '\u0dcf': # e + aa = o (ො)
                result += stem + "o"
                i += 2
            elif next_char == '\u0dd9' and i+2 < len(text) and text[i+2] == '\u0ddf': # e + au = au (ෞ)
                result += stem + "au"
                i += 2
            # Special case: Rakaaraanshaya (් + ZWJ + ර)
            elif next_char == '\u0dca' and i+3 < len(text) and text[i+2] == '\u200d' and text[i+3] == '\u0dbb':
                stem += "r"
                i += 3
                next_char = text[i+1] if i+1 < len(text) else ""
                if next_char in modifiers:
                    result += stem + modifiers[next_char]
                    i += 1
                else:
                    result += stem + "a"
            elif next_char in modifiers:
                result += stem + modifiers[next_char]
                i += 1
            else:
                result += consonants[char]
        elif char in modifiers:
            # Standalone modifier (rare but happens in bad data)
            result += modifiers[char]
        elif char in complex_symbols:
            pass # ignore
        else:
            result += char
        i += 1
    
    # Simplify common double vowels for readability
    result = result.replace('aa', 'a').replace('ee', 'e').replace('ii', 'i').replace('uu', 'u').replace('oo', 'o')
    return result.lower().strip()

def generate_kindle_dict():
    print("Loading JSON data...")
    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    grouped_data = {}
    for entry in data:
        for word, meaning in entry.items():
            if word not in grouped_data:
                grouped_data[word] = []
            grouped_data[word].append(meaning)

    print(f"Generating Hybrid Dictionary with improved Transliteration...")

    html_content = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<html xmlns:idx="www.mobipocket.com/idx" xmlns:mbp="www.mobipocket.com/mbp">',
        '<body>',
        '  <mbp:frameset>',
    ]

    for word in sorted(grouped_data.keys()):
        meanings = grouped_data[word]
        hybrid_meanings = []
        for m in meanings:
            singlish = sinhala_to_singlish(m)
            hybrid_meanings.append(f"<b>{singlish}</b> <br/>({m})")
        
        clean_word = word.replace('"', '&quot;')
        entry_html = [
            f'    <idx:entry name="default" scriptable="yes" spell="yes">',
            f'      <idx:orth value="{clean_word}"><b>{word}</b></idx:orth>',
            f'      <p>{" | ".join(hybrid_meanings)}</p>',
            f'    </idx:entry>',
            '    <hr/>'
        ]
        html_content.extend(entry_html)

    html_content.extend(['  </mbp:frameset>', '</body>', '</html>'])

    with open(HTML_OUTPUT, 'w', encoding='utf-8') as f:
        f.write("\n".join(html_content))

    opf_content = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="2.0" unique-identifier="uid">
  <metadata>
    <dc:identifier id="uid">en-si-hybrid-v4</dc:identifier>
    <dc:title>English-Sinhala Hybrid Dictionary Pro</dc:title>
    <dc:language>en-us</dc:language>
    <x-metadata>
      <DictionaryInLanguage>en-us</DictionaryInLanguage>
      <DictionaryOutLanguage>en-us</DictionaryOutLanguage>
      <DefaultLookupIndex>default</DefaultLookupIndex>
    </x-metadata>
  </metadata>
  <manifest>
    <item id="item1" href="dictionary.html" media-type="application/xhtml+xml"/>
  </manifest>
  <spine>
    <itemref idref="item1"/>
  </spine>
</package>
"""
    with open(OPF_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(opf_content)
    print("Done! Improved hybrid dictionary generated.")

if __name__ == "__main__":
    generate_kindle_dict()
