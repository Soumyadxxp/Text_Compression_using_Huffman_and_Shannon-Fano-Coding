import streamlit as st
import time
import io
import matplotlib.pyplot as plt
from collections import Counter
import heapq
from striprtf.striprtf import rtf_to_text

# ---------- Huffman ----------
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    freq = Counter(text)
    heap = [Node(ch, f) for ch, f in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
    return heap[0]

def huffman_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = {}
    if node:
        if node.char is not None:
            codebook[node.char] = prefix
        huffman_codes(node.left, prefix + "0", codebook)
        huffman_codes(node.right, prefix + "1", codebook)
    return codebook

def huffman_compress(text):
    root = build_huffman_tree(text)
    codes = huffman_codes(root)
    encoded = ''.join(codes[ch] for ch in text)
    return encoded, codes, root

def huffman_decompress(encoded, root):
    result = ""
    node = root
    for bit in encoded:
        node = node.left if bit == '0' else node.right
        if node.char is not None:
            result += node.char
            node = root
    return result

# ---------- Shannon-Fano ----------
def shannon_fano(symbols, codebook):
    if len(symbols) <= 1:
        return
    total = sum(freq for _, freq in symbols)
    acc = 0
    split = 0
    for i, (_, freq) in enumerate(symbols):
        acc += freq
        if acc >= total / 2:
            split = i
            break
    left = symbols[:split + 1]
    right = symbols[split + 1:]
    for ch, _ in left:
        codebook[ch] += "0"
    for ch, _ in right:
        codebook[ch] += "1"
    shannon_fano(left, codebook)
    shannon_fano(right, codebook)

def shannon_compress(text):
    freq = Counter(text)
    symbols = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    codebook = {ch: "" for ch, _ in symbols}
    shannon_fano(symbols, codebook)
    encoded = ''.join(codebook[ch] for ch in text)
    return encoded, codebook

def shannon_decompress(encoded, codebook):
    reverse = {v: k for k, v in codebook.items()}
    decoded = ""
    temp = ""
    for bit in encoded:
        temp += bit
        if temp in reverse:
            decoded += reverse[temp]
            temp = ""
    return decoded

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Compression Dashboard", layout="centered")
st.title("🚀 Compression Dashboard")

# Input area
col1, col2 = st.columns(2)
with col1:
    text_input = st.text_area("✏️ Enter text here", height=150)
with col2:
    uploaded_file = st.file_uploader("📂 Or upload a file (.txt or .rtf)", type=["txt", "rtf"])

# Collect text
text = ""
if uploaded_file is not None:
    try:
        content = uploaded_file.read().decode("utf-8", errors="ignore")
        if uploaded_file.name.endswith(".rtf"):
            text = rtf_to_text(content)
        else:
            text = content
    except Exception as e:
        st.error(f"Error reading file: {e}")
elif text_input.strip():
    text = text_input.strip()

# Run button
if st.button("🚀 Run Compression"):
    if not text:
        st.warning("Please enter some text or upload a file.")
        st.stop()

    # Show original (truncated)
    st.subheader("📄 Original Text")
    if len(text) > 500:
        st.write(text[:500] + " ... (truncated)")
    else:
        st.write(text)

    # Huffman
    with st.spinner("Compressing with Huffman..."):
        start = time.time()
        huff_encoded, huff_codes, huff_root = huffman_compress(text)
        huff_decoded = huffman_decompress(huff_encoded, huff_root)
        huff_time = round(time.time() - start, 5)
        original_bits = len(text) * 8
        huff_ratio = round(len(huff_encoded) / original_bits, 3)

    # Shannon-Fano
    with st.spinner("Compressing with Shannon-Fano..."):
        start = time.time()
        shan_encoded, shan_codes = shannon_compress(text)
        shan_decoded = shannon_decompress(shan_encoded, shan_codes)
        shan_time = round(time.time() - start, 5)
        shan_ratio = round(len(shan_encoded) / original_bits, 3)

    # Display results in two columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔷 Huffman")
        st.text(f"Encoded: {huff_encoded[:200]}{'...' if len(huff_encoded)>200 else ''}")
        st.text(f"Decoded: {huff_decoded[:200]}{'...' if len(huff_decoded)>200 else ''}")
        st.metric("Compression", f"{huff_ratio*100:.2f}%")
        st.metric("Time", f"{huff_time} sec")
        st.download_button(
            label="⬇️ Download Huffman",
            data=huff_encoded,
            file_name="huffman.txt",
            mime="text/plain"
        )
        with st.expander("📋 Huffman Codes"):
            st.table({"Char": list(huff_codes.keys()), "Code": list(huff_codes.values())})

    with col2:
        st.subheader("🔶 Shannon-Fano")
        st.text(f"Encoded: {shan_encoded[:200]}{'...' if len(shan_encoded)>200 else ''}")
        st.text(f"Decoded: {shan_decoded[:200]}{'...' if len(shan_decoded)>200 else ''}")
        st.metric("Compression", f"{shan_ratio*100:.2f}%")
        st.metric("Time", f"{shan_time} sec")
        st.download_button(
            label="⬇️ Download Shannon-Fano",
            data=shan_encoded,
            file_name="shannon.txt",
            mime="text/plain"
        )
        with st.expander("📋 Shannon-Fano Codes"):
            st.table({"Char": list(shan_codes.keys()), "Code": list(shan_codes.values())})

    # Bar chart comparison
    st.subheader("📊 Compression Comparison")
    fig, ax = plt.subplots()
    labels = ['Huffman', 'Shannon-Fano']
    values = [huff_ratio * 100, shan_ratio * 100]
    bars = ax.bar(labels, values, color=['#22c55e', '#ef4444'])
    ax.set_ylabel('Percentage of Original Size')
    ax.set_ylim(0, max(values) + 10)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f"{val:.1f}%", ha='center', va='bottom', color='white')
    st.pyplot(fig)

    # Verification
    if huff_decoded == text and shan_decoded == text:
        st.success("✅ Both methods decoded correctly!")
    else:
        st.error("❌ Decoding mismatch – please check implementation.")