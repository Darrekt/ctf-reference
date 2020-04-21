<?php

# Get the key by exploiting the XOR encoding:
# Msg ^ Key = Cipher
# Msg ^ Cipher = Key
function get_key() {
    $cipher = base64_decode('ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhSRwh6QUcIaAw%3D');
    $text = json_encode(array( "showpassword"=>"no", "bgcolor"=>"#ffffff"));
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
    $outText .= $text[$i] ^ $cipher[$i % strlen($cipher)];
    }
    return $outText;
}

function xor_encrypt($in) {
    $key = 'qw8J';
    $text = $in;
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
    $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}

# Use the key to make our new cookie
    $exploit = array( "showpassword"=>"yes", "bgcolor"=>"#ffffff");
    print get_key();
    print "\n";
    print base64_encode(xor_encrypt(json_encode($exploit)));
?>

