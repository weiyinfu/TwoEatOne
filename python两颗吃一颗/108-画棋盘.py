from PIL import Image, ImageDraw

img = Image.new("RGBA", (550, 550), "orange")
canvas = ImageDraw.Draw(img)
for i in range(4):
    canvas.line(((50 + i * 150, 50), (50 + i * 150, 500)), fill="black", width=5)
    canvas.line(((50, 50 + i * 150), (500, 50 + i * 150)), fill="black", width=5)
img.save("res/board.jpg")
