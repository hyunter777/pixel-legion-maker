# Slots, dyes and content

## Slots and draw order (within the head)

| Slot | Content | Layer |
|---|---|---|
| Eye | Eye color, glowing eyes | 2 |
| FaceHair | Beards | 4 |
| Mask | Face cloth, masks, faceplates | 5 |
| Hair | Hair styles | 6 |
| Helmet | Helmets, hats, hoods | 8 |
| Ornament | Horns, halo, hair flower (shown over any hair or helmet) | 9 |

Under a helmet that covers the head, tall hairstyles (crests, quiffs, buns, flames) switch to a trimmed version so nothing pokes through. The crown, headband and feather band leave the top open and keep the full hairstyle.

Body slots: Top (`Cloth`), Pants (`Pant`), Armor (`Armor`), Cape (`Back`). Weapon slots: Main hand (`WeaponRight`), Off hand (`WeaponLeft`). Recipes use the names in code font.

## Dye palettes and skin tones

Dyes: `crimson`, `ember`, `gold`, `forest`, `teal`, `azure`, `violet`, `rose`, `brown`, `charcoal`, `ivory`, or `#RRGGBB` for a custom color.

Skin tones: `pale`, `tan`, `brown`, `dark`, `orc`, `undead`, `demon`, `frost`.

Glow colors of the glowing eyes are kept when other parts are dyed, and change when the eyes themselves are dyed.

## Content

| Kind | Count |
|---|---|
| Parts | 187 (Armor 14, Back 15, Top 19, Eyes 16, Beard 10, Hair 34, Helmet 27, Mask 18, Ornament 10, Pants 24) |
| Weapons and shields | 85 |
| Example heroes | 55 |
| Motions | 12 per weapon style, 9 weapon styles |
| Dye palettes | 11, plus any custom color |
| Skin tones | 8 |
| Projectiles | 4 |

## Folder layout

| Folder | Content |
|---|---|
| `Documentation/` | License, notices and a link to this manual |
| `Editor/` | Catalog, animation and export tools (editor only) |
| `Generated/` | Catalog, animator controller and clips, icons, prebuilt weapon turns, dye material |
| `Parts/`, `Weapons/`, `Projectiles/` | Part, weapon and projectile images |
| `Rig/` | Rig definition (`rig.json`), base body, guides, motion data |
| `Runtime/` | Runtime scripts (`PixelUnitStudio.Runtime` assembly) |
| `Samples/` | Game sample and runtime assembly sample |
| `Scenes/` | Hero editor scene and rig preview |
| `Shaders/` | Dye sprite shader |
| `Tests/` | Edit mode tests (needs the Test Framework package) |
| `Units/` | Saved heroes and the custom action library (your saves go here too) |
| `LegionBasePack.asset` | The package's [content pack](content-packs.md) |
