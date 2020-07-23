# Modo-Quixel-Bridge-Kit
 Quixel Bridge for Modo

This kit will enable a basic "Custom Disk Export" from Quixel Bridge for Modo 14.1 and above.

Please see the original Quixel sammple for more info (python 2.7): 
https://github.com/Quixel/Bridge-Python-Plugin

To use, download the kit and place the QuixelBridge into your Modo Kits directory
Win: %appdata%/Luxology/Kits
OSX: 

Launch Modo + Bridge
In Bridge, in Export Settings, choose Export To > Custom Socket Export, with the port set to 24981 (the default)

There is a config fragment in the kit so it will start automatically, otherwise in the kits menu at the top, press Quixel Bridge > Start
(you can also stop it from there if required.)


Exported meshes will prompt you with the Modo FBX importer dialog.
Note:
The texture locator for surfaces applied to meshes will not correctly set the uv map and polygon tag. So after import, you will need to change the polygon tag on the material to match the mesh, and set the Texture locator for the images to the UV Map and the correct map.

Surfaces will import using the Modo 14.1 PBR loader. Some definitions are supplied as part of the kit, but you may want to adjust / enable these as required. 

Packed maps are not currently supported, and will just import as one shader tree layer.




