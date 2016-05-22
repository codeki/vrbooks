# vrbooks
Collection of 3D models of books and associated scripts to generate them.

## Strategy
* Identify source of book dimensions and cover art, e.g., Amazon Product Advertizing API or scrape
* Data script to generate input file with essential data for modeling: dimensions, cover art and metadata, e.g., links back to product pages 
* Modeling script (python) to generate models in Blender

### Amazon PA-API
Providing an ISBN, the API returns beautiful XML with dimensions like so...
```
<ItemDimensions>
    <Height Units="hundredths-inches">890</Height>
    <Length Units="hundredths-inches">600</Length>
    <Weight Units="hundredths-pounds">194</Weight>
    <Width Units="hundredths-inches">230</Width>
</ItemDimensions>
```
As well as front cover images in mutiple sizes...
```
<LargeImage>
    <URL>http://ecx.images-amazon.com/images/I/41ZwR6HibFL.jpg</URL>
    <Height Units="pixels">500</Height>
    <Width Units="pixels">333</Width>
</LargeImage>
```
Not sure about spine and back cover though...

### Blender and Python
This works beautifully. See ```makeBook.py``` for first example of a simpy Python script that:
* parses a dummy input file with titles and dimensions
* instructs Blender to build each model and export as FBX file

Run the script with ```blender -b -P makeBook.py``` to run Blender in headless mode.  *Note: Filepaths are hardcoded in these initial examples.*
