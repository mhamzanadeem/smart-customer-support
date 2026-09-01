import argparse
import asyncio
from pathlib import Path

from pypdf import PdfReader

from src.rag.chunker import chunk_text
from src.services.vector_store import (
    MongoVectorStore,
)


def read_file(path: Path) -> str:

    if path.suffix.lower() == ".pdf":

        reader = PdfReader(
            str(path)
        )

        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    return path.read_text(
        encoding="utf-8"
    )


async def ingest(folder: str):

    folder_path = Path(folder)

    if not folder_path.exists():
        raise FileNotFoundError(
            folder
        )

    store = MongoVectorStore()

    files = [
        path
        for path in folder_path.rglob("*")
        if path.suffix.lower()
        in {".pdf", ".txt", ".md"}
    ]

    total = 0

    for file in files:

        print(
            f"Processing: {file}"
        )

        text = read_file(file)

        chunks = chunk_text(text)

        for index, chunk in enumerate(
            chunks
        ):

            await store.add_document(
                title=(
                    f"{file.stem} - "
                    f"chunk {index + 1}"
                ),
                content=chunk,
                source=file.name,
            )

            total += 1

        print(
            f"  Added {len(chunks)} chunks"
        )

    print(
        f"\nCompleted. "
        f"Inserted {total} chunks."
    )


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--folder",
        required=True,
    )

    args = parser.parse_args()

    asyncio.run(
        ingest(args.folder)
    )


if __name__ == "__main__":
    main()