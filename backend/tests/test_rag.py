from src.rag.chunker import chunk_text


def test_chunk_text():

    text = "A" * 3000

    chunks = chunk_text(
        text,
        chunk_size=1000,
        overlap=100,
    )

    assert len(chunks) > 1
    assert all(chunks)