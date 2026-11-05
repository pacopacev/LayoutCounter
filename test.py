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


from PIL import Image
from collections import Counter

def dominant_colors(path, n=5):
    img = Image.open(path).convert("RGB")
    # skip near-white / near-black background pixels
    px = [p for p in img.getdata() if not (min(p) > 230 or max(p) < 30)]
    return Counter(px).most_common(n)

for f in ["Image1.png", "Image2.png"]:
    print(f, dominant_colors(f))