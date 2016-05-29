# vrbooks
Collection of 3D models of books and associated scripts to generate them.

## Strategy
* Identify source of book dimensions and cover art, e.g., Amazon Product Advertizing API 
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
Amazon PA-API provides a PHP snippet from a web form "scratchpad" that can be adapted to start with a list of ISBNs, generate signed URLs for the API query, run the queries, and generate a folder of XML returns.  See ```CollectXML_clean.php``` for an example of just such an adaptation. Note this "clean" version has been scrubbed of Amazon PA-API account information. You'll need to replace the XXX-prefixed values with your own account details. This script reads from ```isbns-read.txt``` and grabs an XML file for each ISBN and saves it to the ```xml``` dir (sample files provided).

Next, you can run ```ParseXML.php``` to extract the useful bits from all the XML files you've collected and generate ```book-list.txt``` in a compact format for later processing.  This script relies on the same ```isbns-read.txt``` file to know which files to look up, but it could also be adapted to just grab every XML file in a given dir.

Then, you can run ```CollectImages.php``` to again parse your collection of XML files but this time extract out an image url for each book and save them to an ```img``` dir (sample files provided).

At this point, you have a nicely formated ```book-list.txt``` and a folder of book cover images, all keyed by ISBN. The next task is to script the generation of 3D models from these data.

### Blender and Python
This works beautifully. See ```makeBook.py``` for first example of a simple Python script that:
* parses the ```book-list.txt``` input file with titles and dimensions
* instructs Blender to build each model and export as FBX file

Run the script with ```blender -b -P makeBook.py``` to run Blender in headless mode.  *Note: Filepaths are hardcoded in these initial examples.*
