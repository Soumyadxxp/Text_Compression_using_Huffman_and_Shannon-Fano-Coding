# Text Compression Dashboard using Huffman and Shannon-Fano Coding

This project is a Streamlit-based web application that demonstrates and compares two lossless data compression algorithms: Huffman Coding and Shannon-Fano Coding. Users can enter text manually or upload text files, compress the data using both algorithms, compare their performance, and download the compressed output.
<img width="1919" height="907" alt="Screenshot 2026-07-06 214439" src="https://github.com/user-attachments/assets/d8c3eb18-8074-415a-9775-2d168255181b" />
<img width="1914" height="909" alt="Screenshot 2026-07-06 214518" src="https://github.com/user-attachments/assets/fe2e3527-ba74-43b8-8644-8dbbe0e4440f" />

---

## Features

- Compress text using Huffman Coding
- Compress text using Shannon-Fano Coding
- Supports manual text input
- Supports `.txt` and `.rtf` file uploads
- Automatically decompresses and verifies the compressed data
- Displays generated encoding tables
- Compares compression ratios
- Measures execution time for both algorithms
- Visual comparison using bar charts
- Download compressed output files

---

## Technologies Used

- Python
- Streamlit
- Matplotlib
- Collections (Counter)
- Heapq (Priority Queue)
- striprtf
- io
- time

---

## How It Works

1. Enter text manually or upload a `.txt` or `.rtf` file.
2. The application processes the input text.
3. Huffman Coding generates a Huffman Tree and compresses the text.
4. Shannon-Fano Coding generates symbol codes and compresses the text.
5. Both compressed outputs are decompressed for verification.
6. Compression ratios and execution times are calculated.
7. Results are displayed in a comparison dashboard.

---

## Algorithms Used

### Huffman Coding

- Builds a binary tree using character frequencies.
- Generates variable-length prefix codes.
- Frequently occurring characters receive shorter codes.
- Guarantees optimal prefix coding.

### Shannon-Fano Coding

- Sorts characters by frequency.
- Recursively divides symbols into two balanced groups.
- Assigns binary codes based on recursive partitioning.
- Produces efficient variable-length prefix codes.

---

## Requirements

- streamlit
- matplotlib
- striprtf

---

## Run the Application

```bash
streamlit run app.py
```

---

## Usage

1. Launch the Streamlit application.
2. Enter text or upload a `.txt` or `.rtf` file.
3. Click **Run Compression**.
4. View:
   - Original text
   - Huffman encoded output
   - Shannon-Fano encoded output
   - Decoded text
   - Compression ratio
   - Execution time
   - Encoding tables
   - Compression comparison chart
5. Download the compressed output if required.

---

## Output

The application displays:

- Original input text
- Huffman encoded data
- Shannon-Fano encoded data
- Decoded text verification
- Compression percentage
- Execution time comparison
- Character-to-code mapping tables
- Bar chart comparing compression performance

---

## Limitations

- Designed for text compression only.
- Compression effectiveness depends on character frequency distribution.
- Does not perform binary file compression.
- Large files may require additional processing time.

---

## Future Improvements

- Support additional compression algorithms such as LZW and Arithmetic Coding.
- Add binary file compression support.
- Display Huffman Tree visualization.
- Export encoding tables.
- Add compression history and statistics.
- Improve UI with additional interactive visualizations.

---

## Author

Soumyadeep Basu

This project is created for educational purposes to demonstrate and compare lossless text compression algorithms using Python and Streamlit.
