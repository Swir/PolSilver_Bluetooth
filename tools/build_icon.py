from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)

size = 1024
img = Image.new("RGBA", (size, size), (7, 17, 31, 255))
d = ImageDraw.Draw(img)
d.rounded_rectangle((52, 52, 972, 972), radius=210, fill=(7, 17, 31, 255), outline=(37, 99, 235, 255), width=34)
shield = [(512, 130), (790, 230), (790, 498), (760, 692), (642, 812), (512, 874), (382, 812), (264, 692), (234, 498), (234, 230)]
d.polygon(shield, fill=(15, 61, 105, 255), outline=(96, 165, 250, 255))
# Bluetooth rune
line = (219, 234, 254, 255)
w = 42
d.line((500, 222, 680, 392, 500, 540, 500, 222), fill=line, width=w, joint="curve")
d.line((500, 540, 682, 704, 500, 838, 500, 540), fill=line, width=w, joint="curve")
d.line((500, 446, 350, 320), fill=line, width=w)
d.line((500, 614, 350, 744), fill=line, width=w)
for box in ((120,120,904,904),(170,170,854,854)):
    d.arc(box, 208, 332, fill=(56,189,248,180), width=18)
    d.arc(box, 28, 152, fill=(56,189,248,180), width=18)
img.save(OUT / "polsilver.png")
img.save(OUT / "polsilver.ico", sizes=[(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)])
print(OUT / "polsilver.ico")
