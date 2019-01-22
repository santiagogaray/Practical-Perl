#!/usr/local/bin/perl -w

#displays a QUERY_STRING or buffer depending on the form's METHOD type.

print "Content-type: text/html\n\n";

print "QUERY STRING IS: $ENV{QUERY_STRING} \n";	 #prints QUERY_STRING
read(STDIN, $buffer,$ENV{CONTENT_LENGTH});      
print "\nBuffer contains: $buffer\n";		 #prints Bufffer
