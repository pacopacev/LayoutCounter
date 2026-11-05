# import fitz
# # import pymupdf aka fitz
# from pprint import pprint

# # go here for very good information on using fitz
# # https://pymupdf.readthedocs.io/en/latest/tutorial.html
# path2pdf = 'selectable.pdf'

# doc = fitz.open(path2pdf)
# num_pages = doc.page_count  # 36

# # the first page of the pdf is page 0
# # loop to manipulate each page in turn
# # for page in doc:
# # for now just get 1 page
# page = doc.load_page(0)
# d = page.get_text("dict")  # big because contains images
# blocks = d["blocks"]  # the list of block dictionaries
# # text blocks are type 0
# textblocks = [b for b in blocks if b["type"] == 0]
# # image blocks are type 1
# imgblocks = [b for b in blocks if b["type"] == 1]
# pprint(textblocks[0])
# print(textblocks[0]['lines'][0]['spans'][0]['text'])
# text = page.get_text('text')


# from PIL import Image
# from collections import Counter

# def dominant_colors(path, n=5):
#     img = Image.open(path).convert("RGB")
#     # skip near-white / near-black background pixels
#     px = [p for p in img.getdata() if not (min(p) > 230 or max(p) < 30)]
#     return Counter(px).most_common(n)

# for f in ["Image1.png", "Image2.png"]:
#     print(f, dominant_colors(f))

import pymupdf
import os

OUT_DIR = "screenshots"

os.makedirs(OUT_DIR, exist_ok=True)   # safe to call repeatedly, creates parents

# Open the PDF
doc = pymupdf.open("boarding-pass.pdf")
# print(len(doc))

for i, page in enumerate(doc):
    
    # print(i, page)

# 1. Search for the text. search_for() returns a list of Rect objects.
    needle = ["FR5472", "AKPCWG", "Sofia"]

    for ii in needle:

        rects = page.search_for(ii)
        # print(f"{rects}\n")

# 2. Iterate over all found rectangles
        for iii, rect in enumerate(rects):
    # 3. Capture a screenshot of the rectangular region
    # You can add a margin by expanding the rect if needed:
            rect = rect + (-50, -50, 50, 50) 
            pix = page.get_pixmap(clip=rect, dpi=150) 
    
    # 4. Save the image
            # filename = f"page{i}_{ii}_match{iii}.png"
            filename = os.path.join(OUT_DIR, f"page{i}_{ii}_match{iii}.png")
            pix.save(filename)

            print(f"Saved screenshot for match {iii+1} at {rect}")

doc.close()