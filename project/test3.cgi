#!/usr/bin/perl -w
use strict;

#displays a QUERY_STRING or buffer depending on the form's METHOD type.

my $buffer;

print "Content-type: text/html\n\n";

read(STDIN, $buffer, $ENV{CONTENT_LENGTH});      
print "\nBuffer contains: $buffer\n";		 #prints Bufffer


