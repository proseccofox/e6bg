# pip install e621py-wrapper
import subprocess
import requests
from PIL import Image, ImageFont, ImageDraw
import e621py_wrapper as e621

client = e621.client()
client.login("e621 username", "api key")

# search notes:
# order:favcount
# maximum fav_count is roughly 4189
query_tags = "order:random width:3840 height:2160 favcount:>800 male"
ignore_tags = "animated female"

posts = client.posts.search(query_tags, ignore_tags, 1)
# assert post length
if len(posts) != 1:
    print("error no posts found")
    exit(1)
post = posts[0]


#def pretty(d, indent=0):
#   for key, value in d.items():
#      print('\t' * indent + str(key))
#      if isinstance(value, dict):
#         pretty(value, indent+1)
#      else:
#         print('\t' * (indent+1) + str(value))
#pretty(post)

pid = post['id']
url = post['file']['url']
ext = post['file']['ext']
artist_str = ", ".join(post['tags']['artist'])
tags_str = "\n    ".join(post['tags']['general'])

filename = f"{pid}.{ext}"
filepath = f"/tmp/{filename}"

# fetch the full res images
with open(filepath, "wb") as f:
  f.write(requests.get(url).content)

# add artists to image
img = Image.open(filepath)
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("DejaVuSans.ttf", 16)
draw.text((10, 10), "artists: " + artist_str, (255,255,255), font=font)
draw.text((10, 10+16), "tags: " + tags_str, (255,255,255), font=font)
img.save(filepath)

# set background
subprocess.run(f"feh --bg-fill {filepath}", shell=True)
