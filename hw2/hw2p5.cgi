#!/usr/local/bin/perl -w

# displays the QUERY_STRING enviroment variable

print "Content-type: text/html\n\n";

print "QUERY STRING IS: $ENV{QUERY_STRING}\n";
