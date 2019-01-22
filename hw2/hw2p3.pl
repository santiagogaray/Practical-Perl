#!/usr/local/bin/perl -w

# displays all the enviroment variables

while (($key,$value) = each %ENV) {
 	print "$key=$value\n";
}   