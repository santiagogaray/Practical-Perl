#!/usr/local/bin/perl -w

# gets data from html form and sends it in a comma
# delimited format to a defined address
# 

print "Content-type: text/html\n\n";

my $name_value;
my @name_value_pairs = split /&/, $ENV{QUERY_STRING};	# if method is POST load
							# data in array


if( $ENV{REQUEST_METHOD} eq 'POST' ) {			# if method is GET
	my $query = "";					# load array with Buffer

	read( STDIN, $query, $ENV{CONTENT_LENGTH} ) == $ENV{CONTENT_LENGTH}
		or error("Error reading buffer");

	push @name_value_pairs, split /&/, $query;
}

# send array through email

open(SENDMAIL, "| /usr/lib/sendmail -F sgaray -t")
	|| die ("can't send mail $!\n");

print SENDMAIL <<EMAILHEAD;	# mail heading
To: santiagogaray\@aol.com
Subject: A Test

EMAILHEAD

foreach $name_value ( @name_value_pairs ) {	# data array in comma
        $value = "" unless defined $value;	# delimited format
        print SENDMAIL "$name_value,";

}

print SENDMAIL "\n";				# close email
close (SENDMAIL);

print <<THANKS;					# display successful message
<html>
<head><title>Thank you</title></head>
<body>
<h1>Thank you. Email sent.</h1>
</body>
</html>
THANKS
