<?php

// Your AWS Access Key ID, as taken from the AWS Your Account page
$aws_access_key_id = "XXX ENTER YOUR ID";

// Your AWS Secret Key corresponding to the above ID, as taken from the AWS Your Account page
$aws_secret_key = "XXX ENTER YOUR SECRET";

// The region you are interested in
$endpoint = "webservices.amazon.com";

$uri = "/onca/xml";

$filename = "isbns-read.txt";

$lines = file ($filename, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);

foreach ($lines as $isbn){
	
$params = array(
    "Service" => "AWSECommerceService",
    "Operation" => "ItemLookup",
    "AWSAccessKeyId" => "XXX ENTER YOUR ID",
    "AssociateTag" => "XXX ENTER YOUR TAG",
    "ItemId" => $isbn,
    "IdType" => "ISBN",
    "ResponseGroup" => "Images,ItemAttributes",
    "SearchIndex" => "Books"
);

// Set current timestamp if not set
if (!isset($params["Timestamp"])) {
    $params["Timestamp"] = gmdate('Y-m-d\TH:i:s\Z');
}

// Sort the parameters by key
ksort($params);

$pairs = array();

foreach ($params as $key => $value) {
    array_push($pairs, rawurlencode($key)."=".rawurlencode($value));
}

// Generate the canonical query
$canonical_query_string = join("&", $pairs);

// Generate the string to be signed
$string_to_sign = "GET\n".$endpoint."\n".$uri."\n".$canonical_query_string;

// Generate the signature required by the Product Advertising API
$signature = base64_encode(hash_hmac("sha256", $string_to_sign, $aws_secret_key, true));

// Generate the signed URL
$request_url = 'http://'.$endpoint.$uri.'?'.$canonical_query_string.'&Signature='.rawurlencode($signature);

# echo "Signed URL: \"".$request_url."\"";

$xml = file_get_contents($request_url);
file_put_contents("xml/".$isbn.".xml", $xml);

// Amazon PA-API has 1 request per 1 second throttle
sleep(1.2);

} #end foreach

?>
