#!/usr/local/bin/perl -w

# saves info into a comma delimites file and 
# diplays success message
#

print "Content-type: text/html\n\n";

my $name_value;
my @name_value_pairs;

if( $ENV{REQUEST_METHOD} eq 'POST' ) {			#if form uses POST method
	my $query = "";					# read buffer and store it in array

	read( STDIN, $query, $ENV{CONTENT_LENGTH} ) == $ENV{CONTENT_LENGTH}
		or error("Error reading buffer");
	push @name_value_pairs, split /&/, $query;
}

foreach $name_value ( @name_value_pairs ) {
        print  "Field: $name_value\n";
}