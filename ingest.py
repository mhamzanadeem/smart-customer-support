import argparse
import asyncio

from pathlib import Path

from pypdf import PdfReader

from dotenv import load_dotenv


load_dotenv()


from src.services.vector_store import (
    VectorStore,
)


def chunk_text(
    text: str,
    size: int = 1200,
    overlap: int = 200,
):

    text = " ".join(
        text.split()
    )


    if not text:

        return []


    chunks = []

    start = 0


    while start < len(text):

        end = min(
            len(text),
            start + size,
        )


        chunks.append(
            text[start:end]
        )


        if end == len(text):

            break


        start = end - overlap


    return chunks


async def ingest_pdf(
    path: Path,
):

    reader = PdfReader(
        str(path)
    )


    store = VectorStore()

    total = 0


    for page_no, page in enumerate(
        reader.pages,
        1,
    ):

        text = (
            page.extract_text()
            or ""
        )


        for idx, chunk in enumerate(
            chunk_text(text),
            1,
        ):

            await store.upsert_document(

                title=(
                    f"{path.stem} — "
                    f"page {page_no} — "
                    f"chunk {idx}"
                ),

                content=chunk,

                source=str(path),
            )


            total += 1


    return total


async def main(
    folder: str,
):

    paths = list(
        Path(folder).glob(
            "*.pdf"
        )
    )


    if not paths:

        print(
            f"No PDFs found in {folder}"
        )

        return


    for path in paths:

        count = await ingest_pdf(
            path
        )

        print(
            f"Ingested {count} "
            f"chunks from {path}"
        )


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--folder",
        default="data",
    )

    args = parser.parse_args()

    asyncio.run(
        main(args.folder)
    )