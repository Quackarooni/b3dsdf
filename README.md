# b3dsdf 🧰

b3dsdf (blender signed distance functions) is a toolkit of 2D/3D signed distance functions and operators nodegroups for the shader editor in Blender 2.83+.

These nodes can be used by appending from the .blend file or use them with the addon which adds a menu in the shader editor. They can also be used with the asset browser by adding the .blend as an asset library and marking them as assets.

<p align="center">
  <img src="https://user-images.githubusercontent.com/830253/169821105-1d13020e-6895-4402-aa0c-2c94db69867f.gif">
</p>

## Installation

Download the latest zip file from the [release page](https://github.com/williamchange/b3dsdf/releases) and install as normal. There's no need to unzip before installing. You might have to restart Blender for changes to take effect after installing / uninstalling.

Alternatively you have the option to install directly from source (code > download zip, or via repo cloning) which might include new features/nodes. Do note that the changes might not be finalized before a release.

## Nodegroups

List of available nodegroups can be found in [shader_nodes.json](https://github.com/williamchange/b3dsdf/blob/master/shader_nodes.json). Examples (with images) can be found in the [wiki page](https://github.com/williamchange/b3dsdf/wiki/Examples) (work in progress).

![sdf_nodegroups](https://user-images.githubusercontent.com/830253/169637834-0cbf72b3-7ecc-410a-9f3b-696d529cc761.png)

## References

- [Erindale's Toolkit (original add menu logic)](https://erindale.gumroad.com/l/erintools)
- [D6464 Blender SDF patch](https://developer.blender.org/D6464)
- [Additonal references / Shadertoy playlist](https://www.shadertoy.com/playlist/7cjGR1)
- [Inigo Quilez's 3D Distance Functions](https://iquilezles.org/articles/distfunctions/)
- [Inigo Quilez's 3D SDF Primitves / Shadertoy playlist](https://www.shadertoy.com/playlist/43cXRl)
- [Inigo Quilez's 2D Distance Functions](https://www.iquilezles.org/www/articles/distfunctions2d/distfunctions2d.htm)
- [Inigo Quilez's 2D SDF Primitves / Shadertoy playlist](https://www.shadertoy.com/playlist/MXdSRf)
- [hg_sdf glsl library](https://mercury.sexy/hg_sdf/)

## Learning Resources
- [The Book of Shaders](https://thebookofshaders.com/)
- [The Art of Code's Raymarching for Dummies Tutorial](https://www.youtube.com/watch?v=PGtv-dBi2wE)
- [Electric Square's Raymarching workshop](https://github.com/electricsquare/raymarching-workshop)
- [HotdogNugget's Raymarching Thread (Nodes)](https://twitter.com/HotdogNugget/status/1510464077478256643)
- [Wannes Malfait's Raymarching Tutorial (Nodes)](https://www.youtube.com/watch?v=aBf3FV97rJY)