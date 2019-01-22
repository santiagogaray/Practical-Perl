#!/usr/bin/perl -w

# saves info into a comma delimites file and 
# diplays success message
#

print "Content-type: text/html\n\n";

my $name_value;
my @name_value_pairs = split /&/, $ENV{QUERY_STRING};	#if info POSTED save info in array

if( $ENV{REQUEST_METHOD} eq 'POST' ) {			#if form uses GET method
	my $query = "";					# read buffer and store it in array

	read( STDIN, $query, $ENV{CONTENT_LENGTH} ) == $ENV{CONTENT_LENGTH}
		or error("Error reading buffer");
	push @name_value_pairs, split /&/, $query;
}

open(CSVOUT, ">> hw2p7.csv") || die ("can't open file $!");  #create or append file

foreach $name_value ( @name_value_pairs ) {	# save array info into file
        $value = "" unless defined $value;
        print CSVOUT "$name_value,";
}
close (CSVOUT);

print <<THANKS;					# Success message dispayed
<html>
<head><title>Thank you</title></head>
<body>
<h1>Thank you.  We received your information.</h1>
</body>
</html>
THANKS
