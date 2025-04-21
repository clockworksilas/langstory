import streamlit as st
import json
import os
import time

# ---------------- Setup ----------------
FULL_TEXT = """Boundlessly, I trudged through the perpetual, labyrinthic pathway. The fluorescent moon illuminated the deserted cemetery, and the overcast sky was enveloped with fevering clouds. Despite all this, I could see the freckles of silver stars hanging from the sky.
The first thing I had noticed when I awoke was the damp grass beneath me, which was quilted with fallen and crumpled weeping willow leaves. When my eyes had adjusted to the epitome of darkness, I took account of my surroundings; I was encircled with towering trees with extending limbs, which guarded a rusty iron gate that steadily creaked open with the support of a gust of wind.
With each step, the path behind me seemed to dissolve into the shadow, as if the forest was trying to swallow the memory of my passing. Branches and roots clawed at my feet and arms, and the air thickened with the stench of damp moss and something far beyond natural.
I stumbled on. It was the memory of sunlight dancing across the kitchen floor, of laughter echoing down a hallway that I could no longer imagine. That fragment of home pulled me together. And then, as summoned by the thought alone, the trees loosened their grip, the darkness cracked – and there it was: a house. Unbelievably bright and cascaded with life, like a poignant memory refusing to fade.
Amid the lifeless wilderness and choking gloom, there stood a house that defied it all, unnaturally radiant like artificial colouring, and almost smug in its place. Its windows glowed like molten gold, spilling warmth onto the earth-ridden ground, and the walls gleamed with a fresh coat of pastel paint. Daisies, absurdly vibrant, bloomed defiantly in neatly trimmed flowerbeds, humming a soft melody of laughter.
A flicker in the upstairs window caught my eye. A girl – or something like one – peered at me from behind the clear glass. Her hair floated around her like ink swirling in water, and her eyes reflected a daring light, unnatural, too bright, too knowing. For a moment we stared at each other; then she vanished into the shadows, leaving only the soft sway of the curtain and the house, still glowing, still smiling."""

def split_chunks(text, max_sentences=1):
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [' '.join(sentences[i:i+max_sentences]) for i in range(0, len(sentences), max_sentences)]

CHUNKS = split_chunks(FULL_TEXT, max_sentences=1)
PROGRESS_FILE = "memory_progress.json"
SHOW_TIME = 4  # seconds

# ---------------- Progress Handling ----------------
def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f).get("progress", 0)
    return 0

def save_progress(index):
    with open(PROGRESS_FILE, "w") as f:
        json.dump({"progress": index}, f)

# ---------------- App Logic ----------------
st.set_page_config(page_title="Memory Challenge", layout="centered")
st.title("🧠 Memory Flash Game")

progress = load_progress()
total_chunks = len(CHUNKS)
current_chunk = CHUNKS[progress]

st.progress(progress / total_chunks)
st.subheader(f"Chunk {progress + 1} of {total_chunks}")

# ------- Initialize session state -------
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

if "chunk_revealed" not in st.session_state:
    st.session_state.chunk_revealed = True

# ------- Timer and logic -------
elapsed = time.time() - st.session_state.start_time

if st.session_state.chunk_revealed and elapsed < SHOW_TIME:
    st.info("⏱ Memorize this quickly!")
    st.code(current_chunk)
    st.caption(f"Disappearing in {int(SHOW_TIME - elapsed)} sec...")
    st.experimental_rerun()

elif st.session_state.chunk_revealed and elapsed >= SHOW_TIME:
    st.session_state.chunk_revealed = False
    st.experimental_rerun()

# ------- Typing from memory -------
user_input = st.text_area("✍️ Type what you remember:")

if st.button("Check"):
    if user_input.strip() == current_chunk:
        st.success("✅ You nailed it!")
        if progress + 1 < total_chunks:
            save_progress(progress + 1)
            st.session_state.start_time = time.time()
            st.session_state.chunk_revealed = True
            st.experimental_rerun()
        else:
            st.balloons()
            st.success("🎉 You've finished memorizing the whole thing!")
    else:
        st.error("❌ Not quite. Try again or view the original below.")

with st.expander("👀 Reveal the correct chunk"):
    st.write(current_chunk)

if st.button("🔁 Reset Progress"):
    save_progress(0)
    st.session_state.start_time = time.time()
    st.session_state.chunk_revealed = True
    st.experimental_rerun()
