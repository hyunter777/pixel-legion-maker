# FAQ

**Heroes look blurry.**
Use an orthographic camera with `LegionPixelCamera`, or a camera size that gives an integer pixel scale. Keep sprites on point filtering.

**A part does not show in the editor.**
Check that the file is in the right `Parts/<Slot>/` folder of a pack and that its name is not already used (the Console shows a warning), then run **Tools > Pixel Legion Maker > Build Catalog**.

**Heroes face the wrong way.**
The rig faces left. Set the x scale of the hero root to −1 to face right.

**An attack stays on its last frame.**
One-shot motions hold their last frame by design. Tick **Return To Idle** on `LegionEvents`, or play `idle` from your game code ([Heroes in code](using-heroes.md)).

**The editor buttons do not react.**
The editor adds a UI input module that matches your input settings. If you replaced the EventSystem in the editor scene, keep one in the scene.

**Does it work with URP?**
Yes. The dye shader is a plain sprite shader that renders in both the Built-in pipeline and URP, including the 2D renderer. HDRP is not supported.

**Can I use the heroes outside Unity?**
Yes. [Frame sheets](sheets-and-camera.md) are plain PNG files with JSON metadata.

**Where do I report a bug?**
See [Support and licenses](support-license.md).
