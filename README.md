# Modo-Quixel-Bridge-Kit
 Quixel Bridge for Modo

This kit will enable a basic "Custom Disk Export" from Quixel Bridge into Modo 14.1 and above.

Please see the original Quixel sample for more info (python 2.7): 
https://github.com/Quixel/Bridge-Python-Plugin

To use, download the kit and place the QuixelBridge folder into your Modo Kits directory
Win: %appdata%/Luxology/Kits

Launch Modo + Bridge
In Bridge, in Export Settings, choose Export To > Custom Socket Export, with the port set to 24981 (the default)

There is a config fragment in the kit so it will start automatically when modo is launched, otherwise in the kits menu at the top, press Quixel Bridge > Start
(you can also stop it from there if required.)

Surfaces will import using the Modo PBR loader. Some definitions are supplied as part of the kit, but you may want to adjust / enable these as required. 

If pushing a mesh, the select mesh option will select the mesh after import. Doing this will set the imported mateirals to be set to the selected UV map.
If the UV map goes wrong, enter setup mode to change it.

The set mask option will set the item mask on any newly added materials to the first selected item.



