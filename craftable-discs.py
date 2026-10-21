
import json
import shutil
import zipfile
from pathlib import Path

PACK_NAME = "craftable_music_discs"
PACK_DESCRIPTION = "Duplicate any music disc with an anvil, diamond, and gilded blackstone."
NAMESPACE = "craftable_music_discs"
OUTPUT_DIR = Path()
OUTPUT_ZIP = Path("Craftable Music Discs by Crimulus.zip")

# All music discs in Minecraft Java Edition 26.3.
DISCS = [
    "13",
    "cat",
    "blocks",
    "chirp",
    "far",
    "mall",
    "mellohi",
    "stal",
    "strad",
    "ward",
    "11",
    "wait",
    "otherside",
    "5",
    "pigstep",
    "relic",
    "creator",
    "creator_music_box",
    "precipice",
    "tears",
    "lava_chicken",
    "bounce",
]

def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2) + "\n",
        encoding="utf-8"
    )

# Remove old output to prevent stale files.
if OUTPUT_ZIP.exists():
    OUTPUT_ZIP.unlink()

# pack.mcmeta goes directly inside the datapack root.
write_json(OUTPUT_DIR / "pack.mcmeta", {
    "pack": {
        "description": f"{PACK_DESCRIPTION}",
        "min_format": [121, 0],
        "max_format": [121, 0]
    }
})

for disc in DISCS:
    item_id = f"minecraft:music_disc_{disc}"
    recipe_id = f"{NAMESPACE}:duplicate_{disc}"
    advancement_id = f"{NAMESPACE}:crafted/{disc}"
    function_id = f"{NAMESPACE}:duplicate/{disc}"

    write_json(
        OUTPUT_DIR / "data" / "recipe" / f"duplicate_{disc}.json",
        {
            "type": "minecraft:crafting_shaped",
            "pattern": [
                " A ",
                " DB",
                " G "
            ],
            "key": {
                "A": "minecraft:anvil",
                "D": "minecraft:diamond",
                "B": item_id,
                "G": "minecraft:gilded_blackstone"
            },
            "result": {
                "id": item_id,
                "count": 1
            }
        }
    )

    write_json(
        OUTPUT_DIR / "data" / "advancement" / "crafted" / f"{disc}.json",
        {
            "criteria": {
                "crafted_disc": {
                    "trigger": "minecraft:recipe_crafted",
                    "conditions": {
                        "recipes": recipe_id
                    }
                }
            },
            "rewards": {
                "function": function_id
            }
        }
    )

    function_path = OUTPUT_DIR / "data" / "function" / "duplicate" / f"{disc}.mcfunction"
    function_path.parent.mkdir(parents=True, exist_ok=True)
    function_path.write_text((
        f"give @s {item_id}\n"
        f"advancement revoke @s only {advancement_id}\n"
    ), encoding="utf-8")

with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as pack:
    for path in sorted(OUTPUT_DIR.rglob("*")):
        if path.is_file():
            pack.write(
                path,
                path.relative_to(OUTPUT_DIR)
            )

print(f"Created ZIP: {OUTPUT_ZIP.resolve()}")
print(f"Created raw datapack directory: {OUTPUT_DIR.resolve()}")
print(f"Generated recipes: {len(DISCS)}")
print(f"Generated advancements: {len(DISCS)}")
print(f"Generated functions: {len(DISCS)}")
