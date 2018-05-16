# Factorio screenshot to OSM tiles converter

This set of hacks converts screenshots from
[Factorio](http://www.factorio.com) into a format that resembles OSM
tiles. I use them to feed the tiles to a
[leaflet](http://leafletjs.com/)-based page, for a nice "map-like"
screenshot feel.

## Requirements

Python 2.x with the Python Imaging Library (PIL) installed.

## Generating the screenshots

The scripts expect screenshots named `s_<x>_<y>.jpg`, where `x` and
`y` are chunk coordinates. You can use the following command in the
Factorio chat/console commandline:

     /c for x=-1000,1000 do for y=-1000,1000 do if game.player.surface.is_chunk_generated{x,y} then game.take_screenshot{show_entity_info=true,zoom=1, resolution={1024,1024}, position={x=32*x+16,y=32*y+16}, path="DIR/s_"..x.."_"..y..".jpg"}; end; end; end

You can choose any `DIR` here. Factorio will even autocreate it if it
does not exist.

This places the screenshots in `<factorio_dir>/script-output/DIR/`.

## Processing into OSM tiles

`slice.py` cuts the 1024x1024 screenshots obtained from factorio into
2x2 tiles of size 256x256 (scaling by 0.5 in the process). Use it like
so:

    cd <factorio_dir>/script-output/DIR/
    ls s_*.jpg | nice xargs -n100 -P8 /path/to/slice.py
	
The `-P8` will run 8 instances in parallel, which is faster if you
have a typical 4-core 2x hyperthreading system. Adjust to taste.

The directory should now contain a subdirectory tree under `11/` that
contains OSM-format tiles for zoom level 11.

Second, `shrink.py` processes that into zoomed-out tiles for the
remaining levels. Use it like so (still in the same directory):

    /path/to/slice.py

It will scan the directory `11/` for tiles and create `10/` by
combining 2x2 tiles and scaling by 0.5, then `9/` from `10/`, etc.

## Making a page with leaflet

`rsync` (or whatever) the tile directories (`11/`, `10/`, etc.) to
your favorite location on a webserver. You can feed that directly into
leaflet; I recommend the following settings:

* Use a tile URL of the form `.../{z}/{x}/{y}.jpg` to match what the
  scripts generate.

* Set `minZoom: 1` and `maxZoom: 11` on every layer, to match what the
  scripts generate.

* I use an `errorTileUrl` pointing to a 256x256 black image, so that
  nonexistent tiles are rendered in black.

* I applied this patch:

        diff --git 1/leaflet.orig/leaflet.css 2/leaflet/leaflet.css
        index ac0cd17..f82278a 100644
        --- 1/leaflet.orig/leaflet.css
        +++ 2/leaflet/leaflet.css
        @@ -181,7 +181,7 @@
         /* visual tweaks */

         .leaflet-container {
        -       background: #ddd;
        +       background: #000;
                outline: 0;
                }
         .leaflet-container a {

  This makes the default background black, instead of having it
  annoyingly flicker `#ddd` before it loads the black "nonexistent
  tile" image.

You can also look at the
[page I wrote this for](http://thomasrast.ch/factorio/).
