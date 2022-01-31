import os
import fitz
from pathlib import Path


def extract_image():
    path = Path(__file__).parent
    if not path.parent.joinpath("Images").exists():
        os.mkdir(path.parent.joinpath("Images"))

    epaper_dir = path.parent.joinpath("Newspapers")
    indv_dir = os.listdir(epaper_dir)

    for source in indv_dir:
        newspapers = os.listdir(path.joinpath(epaper_dir, source))
        no_of_newspapers = len(newspapers)
        newspaper_count = 0

        for newspaper in newspapers:
            newspaper_count += 1
            print(f"Processing newspaper: {newspaper} ===================[{newspaper_count}/{no_of_newspapers}]")

            if newspaper.endswith(".pdf"):
                with fitz.open(epaper_dir.joinpath(source, newspaper)) as doc:
                    output_path = path.parent.joinpath("Images", newspaper[:-4])

                    if not os.path.exists(output_path):
                        os.mkdir(output_path)

                    for i in range(0, doc.page_count):
                        page = doc.load_page(i)
                        pix = page.get_pixmap(matrix=fitz.Matrix(5, 5))
                        output = newspaper[:-4] + "_pg_" + str(i+1) + ".jpg"
                        print(f"\t==>Image conversion of page [{i + 1}/{doc.page_count}]")
                        pix.save(output_path.joinpath(output))


if __name__ == "__main__":
    extract_image()
