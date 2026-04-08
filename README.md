# Kindle English-Sinhala Hybrid Dictionary

A high-performance, searchable dictionary for Amazon Kindle devices (including Kindle Colorsoft, Paperwhite, and Oasis). This project transforms a raw English-to-Sinhala JSON dataset into a fully indexed Kindle-compatible dictionary with **Singlish (transliteration) fallbacks** to ensure 100% readability across all device generations.

## 🌟 Features

- **Hybrid Display:** Shows meanings in both Singlish (bold) and native Sinhala script (parentheses).
- **Intelligent Transliteration:** Custom engine handles complex Sinhala Unicode characters, composite vowels (e.g., `ො`, `ෞ`), and consonant clusters (Rakaaraanshaya).
- **Zero-Font Dependency:** By providing Singlish fallbacks, meanings are readable even if the Kindle's system font fails to render complex Sinhala glyphs.
- **Optimized Indexing:** Uses Kindle-specific XHTML tags (`idx:entry`, `idx:orth`) for instant tap-to-translate lookup.
- **Validation Suite:** Includes a test script to verify 100% transliteration coverage across the entire dataset.

## 🛠 Tech Stack

- **Python 3:** Data processing and transliteration engine.
- **Kindle XHTML/OPF:** Amazon's proprietary dictionary indexing format.
- **JSON:** Source data format.

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- [Kindle Previewer 3](https://www.amazon.com/kp/kindlepreviewer) (for final compilation)

### Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/kindle-sinhala-dict.git
   cd kindle-sinhala-dict
   ```

2. **Prepare your data:**
   Ensure your source file `en_to_si.json` is located in the project root.

3. **Generate the dictionary files:**
   Run the conversion script to generate `dictionary.html` and `kindle_dict.opf`:
   ```bash
   python3 convert.py
   ```

4. **Validate the output:**
   Run the validation script to ensure no untransliterated characters remain:
   ```bash
   python3 validate.py
   ```

## 📖 Final Compilation (The Kindle Build)

Once the `.opf` and `.html` files are generated, follow these steps to create the final Kindle file:

1. **Open Kindle Previewer 3.**
2. **Drag and Drop** the `kindle_dict.opf` file into the Previewer window.
3. The software will begin converting the files into a Kindle-compatible format.
4. Once the conversion is complete, click **File > Export** and save the file as a **.mobi** or **.azw3**.
5. **Transfer to Kindle:**
   - Connect your Kindle to your computer via USB.
   - Copy the exported file into the `documents/dictionaries` folder on your Kindle.
6. **Enable on Kindle:**
   - Open any English book.
   - Tap a word to trigger the dictionary.
   - Tap the dictionary name in the popup to switch to your new **English-Sinhala Hybrid Dictionary**.

## 🤝 Contributing

If you find a Sinhala character that doesn't transliterate correctly:
1. Add the character to the `vowels`, `consonants`, or `modifiers` dictionary in `convert.py`.
2. Run `python3 validate.py` to verify the fix.
3. Submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
