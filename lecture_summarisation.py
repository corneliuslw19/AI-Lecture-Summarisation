import whisper
from keybert import KeyBERT
from pathlib import Path
from transformers import pipeline

def process_audio(audio_path):
    audio_path = Path(audio_path)

    # output files
    transcript_path = Path("output/transcript.txt")
    summary_path = Path("output/summary.txt")
    key_concepts_path = Path("output/key_concepts.txt")
    revision_notes_path = Path("output/revision_notes.txt")

    # error handling for missing audio file
    if not audio_path.exists():
        print("Error: Audio file not found.")
        return

    # create output folder
    transcript_path.parent.mkdir(exist_ok=True)

    # load Whisper
    print("Loading Whisper model...")
    whisper_model = whisper.load_model("base")

    ## generating transcript
    print("Transcribing audio...")
    result = whisper_model.transcribe(str(audio_path), language="en")
    transcript = result["text"]

    transcript_path.write_text(transcript, encoding="utf-8")

    print("Transcription complete.")
    print("Transcript saved to:", transcript_path)

    ## generating summary
    print("Loading summarisation model...")
    summariser = pipeline(
        "summarization",
        model="facebook/bart-large-cnn",
        framework="pt"
    )

    print("Generating summary...")

    ## split text for summary
    def split_text(text, max_chars=2500):
        chunks = []

        while len(text) > max_chars:
            split_position = text.rfind(".", 0, max_chars)

            if split_position == -1:
                split_position = max_chars

            chunk = text[:split_position + 1].strip()
            chunks.append(chunk)

            text = text[split_position + 1:].strip()

        if text:
            chunks.append(text)

        return chunks

    chunks = split_text(transcript)

    print(f"Transcript split into {len(chunks)} chunk(s).")

    chunk_summaries = []

    for i, chunk in enumerate(chunks, start=1):
        print(f"Summarising chunk {i}/{len(chunks)}...")

        summary_result = summariser(
            chunk,
            max_length=120,
            min_length=30,
            do_sample=False
        )

        chunk_summary = summary_result[0]["summary_text"]
        chunk_summaries.append(chunk_summary)

    summary = "\n\n".join(chunk_summaries)

    summary_path.write_text(summary, encoding="utf-8")

    print("Summary complete.")
    print("Summary saved to:", summary_path)

    print("\n--- Transcript ---")
    print(transcript[:800])

    print("\n--- Summary ---")
    print(summary)

    ## generating key concepts
    print ("\nExtracting key concepts..")

    keyword_model = KeyBERT()

    keywords = keyword_model.extract_keywords(
        summary,
        keyphrase_ngram_range=(1, 3),
        stop_words="english",
        use_mmr=True,
        diversity=0.7,
        top_n=10
    )

    key_concepts = [keyword for keyword, score in keywords]

    key_concepts_text = "\n".join(
        f"- {concept}" for concept in key_concepts
    )

    key_concepts_path.write_text(
        key_concepts_text,
        encoding="utf-8"
    )

    print("Key concepts saved to:", key_concepts_path)

    print ("key concept extracted")
    print ("\n ---Key Concepts---")
    for concept in key_concepts:
        print("-", concept)

    print("Generating structured revision notes...")

    summary_sentences = []

    for paragraph in summary.split("\n"):
        paragraph = paragraph.strip()

        if paragraph:
            sentences = paragraph.split(". ")

            for sentence in sentences:
                sentence = sentence.strip()

                if sentence:
                    if not sentence.endswith("."):
                        sentence += "."

                    summary_sentences.append(sentence)


    revision_notes = "LECTURE REVISION NOTES\n\n"

    revision_notes += "KEY CONCEPTS\n"
    for concept in key_concepts:
        revision_notes += f"- {concept}\n"

    revision_notes += "\nIMPORTANT REVISION POINTS\n"
    for sentence in summary_sentences:
        revision_notes += f"- {sentence}\n"

    revision_notes_path.write_text(
        revision_notes,
        encoding="utf-8"
    )

    print("Revision notes saved to:", revision_notes_path)

