# Frame sheets and camera

## Frame sheet export

**Export** in the editor, or **Tools > Pixel Legion Maker > Export Saved Hero Sheets**, writes `Exports/Heroes/HERO_<NAME>.png` and a `.json` file next to it, in the project folder (outside `Assets`).

- One row per motion, one column per frame, at 1:1 pixel size. Frames grow to fit large weapons.
- The JSON lists `fps`, `frameWidth`, `frameHeight`, the foot origin (`originX` from the left, `groundPx` from the bottom) and `clips` (name, row, frame count, loop, and `events` with the `hit`, `cast` and `end` frames).

The sheets do not depend on Unity, so you can use them in other engines or tools.

## Pixel-perfect camera

Add **LegionPixelCamera** to an orthographic camera.

| Field | Meaning |
|---|---|
| Pixels Per Unit | 32 for hero art |
| Reference Resolution | The smallest view in art pixels. The screen always shows an integer multiple of it. |
| Upscale Render Texture | In play mode, render at art resolution and scale up by an integer factor. Rotated limbs and weapons then snap to the pixel grid. |

It works the same in the Built-in pipeline and URP. The game and assembly samples use it at 384×216.
