<?php
libxml_use_internal_errors(true);

$fn1 = "isbns-read.txt";
$books = file($fn1, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
foreach ($books as $isbn){

	$xmlfile = "xml/".$isbn.".xml";
	$xmlDoc = new DOMDocument();
	$xmlDoc->load($xmlfile);
	if (!isset($xmlDoc)){ echo "Could not load XML from ".$isbn.".xml \n"; continue;}

	// Book cover image
	$imageUrl = "";
	$largeImageNodes = $xmlDoc->getElementsByTagName('LargeImage');
	if (isset($largeImageNodes->item(0)->childNodes)){
		foreach ($largeImageNodes->item(0)->childNodes AS $tag){
			if ($tag->nodeName == 'URL')
				$imageUrl = $tag->nodeValue;
		}
	}

	if (!isset($imageUrl)){ echo "Could not get image URL for ".$isbn.".xml \n"; continue;}

	// Get extension and save file
	$ext = pathinfo($imageUrl, PATHINFO_EXTENSION);
	copy($imageUrl, "img/".$isbn.".".$ext);

	// Pause to be cool
	sleep(1);

} #end foreach

?>
