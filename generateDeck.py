import os
import re
import sys
from PIL import Image
import tempfile


def parse_deck_file(file_path, path):
    deck = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            match = re.match(r'(\d+)x([A-Z0-9]+-\d+)', line)
            if match:
                quantity = int(match.group(1))
                full_code = match.group(2)
                expansion = full_code.split('-')[0]
                card_image_path = path + "\\" + expansion + "\\" + full_code

                deck.append({
                    'quantity': quantity,
                    'expansion': expansion,
                    'code': full_code,
                    'image_path': card_image_path
                })
    return deck

def save_card_images(deck, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for card in deck:
        if os.path.exists(card['image_path'] + '.png'):
            type = ".png"
        else:
            type = ".jpg"
        for i in range(card['quantity']):
            try:
                img = Image.open(card['image_path'] + type)

                output_name = f"{card['code']}_{i+1}" + type
                output_path = os.path.join(output_folder, output_name)
                img.save(output_path)
                print(f"Saved {output_path}")
            except FileNotFoundError:
                print(f"Image not found: {card['image_path'] + type}")

def create_deck_collage(image_folder, output_path, card_width=480, card_height=671, columns=10):
    image_files = sorted([
        f for f in os.listdir(image_folder)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ])

    if not image_files:
        print("No images found in folder:", image_folder)
        return

    rows = (len(image_files) + columns - 1) // columns
    collage_width = columns * card_width
    collage_height = rows * card_height

    collage = Image.new('RGB', (collage_width, collage_height), color=(0, 0, 0))

    for idx, filename in enumerate(image_files):
        img_path = os.path.join(image_folder, filename)
        try:
            img = Image.open(img_path).resize((card_width, card_height))
        except Exception as e:
            print(f"Could not open {img_path}: {e}")
            continue

        x = (idx % columns) * card_width
        y = (idx // columns) * card_height
        collage.paste(img, (x, y))

    collage.save(output_path)
    print(f"✅ Collage saved to: {output_path}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python generateDeck.py <path to op sim example: D:\Games\op> <name of deck in sim>")
        sys.exit(1)

    path = sys.argv[1] + "\\OPTCGSim_Data\\StreamingAssets\\Cards"
    cardlist = sys.argv[1] + "\\Decks\\" + sys.argv[2] + ".deck"

    if not os.path.exists(path):
        print("Directory " + path + " does not exist")
        sys.exit(1)

    if not os.path.exists(cardlist):
        print("File " + cardlist + " does not exist")
        sys.exit(1)

    temp_dir = tempfile.TemporaryDirectory()
    deck = parse_deck_file(cardlist, path)
    save_card_images(deck, temp_dir.name)
    create_deck_collage(temp_dir.name, sys.argv[2] + "_deck.png")
    temp_dir.cleanup()

if __name__ == "__main__":
    main()