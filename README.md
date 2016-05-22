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
And backcover may sometimes be provided as one of the ```Category="variant"``` ImageSet results, for example, ```http://ecx.images-amazon.com/images/I/51XqXtcuqbL.jpg```.  Not sure how to know *which* "variant" is the backcover, however, and not sure is spine image is ever provided...

Also relevant to a detailed rendering would be if it's a paperback or hardback. This information is provided in the ```<Binding>``` tag under ```<ItemAttributes>```. Nice!

### Data Scripts
Amazon PA-API provides a PHP snippet from a web form "scratchpad" that can be adapted to start with a list of ISBNs, generate signed URLs for the API query, run the queries, and generate a folder of XML returns.

Another script can then parse those XMLs to generate the input file format for the Blender/Python script to generate the models.

### Blender and Python
This works beautifully. See ```makeBook.py``` for first example of a simple Python script that:
* parses a dummy input file with titles and dimensions
* instructs Blender to build each model and export as FBX file

Run the script with ```blender -b -P makeBook.py``` to run Blender in headless mode.  *Note: Filepaths are hardcoded in these initial examples.*
