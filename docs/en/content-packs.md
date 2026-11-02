# Content packs

A content pack is a folder of parts, weapons, projectiles and heroes with a **Content Pack** asset at its top. The package itself is the pack `LegionBasePack.asset`. Keeping your own art in a pack of its own, outside `Assets/PixelUnitStudio`, keeps it apart from the package, so updating the package never touches it. Add-on packs for Pixel Legion Maker are packs too: they hold only art and heroes, and they need this package to work.

## Make a pack

1. Create a folder such as `Assets/MyLegionPack/` and, inside it, **Create > Pixel Legion Maker > Content Pack**.
2. Put images in the same layout as the package: `Parts/<Slot>/`, `Weapons/`, `Projectiles/`, and optionally `WeaponTurns/` (24 pre-rotated turns of a weapon, same file name; without them the weapon art is rotated as is).
3. Name files type first, as the package does (`axe_frost`, `helmet_raider`). The first word picks a weapon's motion style and its filter in the editor. A name the package or an earlier pack already uses is skipped with a warning.
4. Give options card names under **Titles** on the pack asset. An option without one shows its file name, tidied (`axe_frost` → "Axe frost").

The catalog picks up the pack by itself the next time the editor is in focus.

## Pack fields

| Field | Use |
|---|---|
| Title | Shown on the corner of the pack's part cards and over its heroes in the hero list |
| Order | Packs are read in this order (the package is 0, new packs 100) |
| Parts / Weapons / Weapon Turns / Projectiles Folder | Image folders, relative to the pack asset |
| Heroes Folder | Hero prefabs that come with the pack and their `LegionActions.asset`. The editor lists them under the pack's title; loading one and pressing **Save** puts a copy in your save folder. The pack's actions show in the Actions panel to play or copy |
| Generated Folder | Card icons made by the catalog build |
