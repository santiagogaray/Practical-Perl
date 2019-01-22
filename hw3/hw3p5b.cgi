#!/usr/local/bin/perl -w
use CGI qw/:standard/;
use strict;

#
# Parses posted order and creates table
#
	my $buffer;
	read(STDIN, $buffer,$ENV{'CONTENT_LENGTH'}); 	# read posted info
  
print header, start_html;

print_order($buffer);	# call subroutine passing buffer

print end_html;


sub print_order {


	print "<CENTER>";
	print h2("Thank you for your order");

	print "<TABLE BORDER=1>";

	print "<TR><TD><B>Quantity</TD><TD><B>Part #</TD></TR>";

	my @orderitem = split /&/, $_[0]; # get each item-value pair

	foreach my $pair (@orderitem) {

		my $value;
		my $item;

		($item, $value) = split /=/, $pair;
		print "<TR><TD>$value</TD><TD>$item</TD></TR>"	 # print each item ordered
			unless ($value eq "" || $value eq "Submit+Order" ); 
								
	}

	print "</TABLE>";
	print "<CENTER>";
}

