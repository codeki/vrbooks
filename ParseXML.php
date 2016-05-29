<?php
libxml_use_internal_errors(true);

$fn0 = "book-list.txt";
file_put_contents($fn0, "");

$fn1 = "isbns-read.txt";
$books = file($fn1, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
foreach ($books as $isbn){

	$xmlfile = "xml/".$isbn.".xml";
	$xmlDoc = new DOMDocument();
	$xmlDoc->load($xmlfile);
	if (!isset($xmlDoc)){ echo "Could not load XML from ".$isbn.".xml \n"; continue;}

	// Book title
	$titles = $xmlDoc->getElementsByTagName('Title');
	$title = $titles->item(0)->nodeValue;
        if (!isset($title)) {echo "Could not find title in ".$isbn.".xml \n"; continue;}
	
	// Book binding
	$bindingNode = $xmlDoc->getElementsByTagName('Binding');
	$bindingValue = (isset($bindingNode) ? $bindingNode->item(0)->nodeValue : NULL);
	$binding = (isset($bindingValue) ? $bindingValue : "unknown");

	// Book dimensions
	$itemDim =  $xmlDoc->getElementsByTagName('ItemDimensions');
        #if (!isset($itemDim)){echo "Could not find ItemDimensions in ".$isbn.".xml \n"; continue;}
	$h = 0;
	$w = 0;
	$l = 0;
	$hwl = "";
	if (isset($itemDim->item(0)->childNodes)){
	    foreach ($itemDim->item(0)->childNodes AS $dim){
		if ($dim->nodeName == 'Height')
			$h = $dim->nodeValue;
	        if ($dim->nodeName == 'Width') 
		        $w = $dim->nodeValue;
	        if ($dim->nodeName == 'Length') 
			$l = $dim->nodeValue;
	    }
	}	
	$hwl = $h."x".$w."x".$l;

	// Write to file
	file_put_contents($fn0, $isbn."\n", FILE_APPEND);
	file_put_contents($fn0, $title."\n", FILE_APPEND);
	file_put_contents($fn0, $binding. "\n", FILE_APPEND);
	file_put_contents($fn0, $hwl."\n", FILE_APPEND);

} #end foreach

?>
