

url = "https://cdn.pixabay.com/photo/2016/02/17/21/15/bernese-mountain-dog-1205918_1280.jpg"

print(url)

print(url.split("/")[-1])

if url.endswith("1280.jpg"):
    print("perfect")