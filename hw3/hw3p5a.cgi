#!/usr/local/bin/perl -w
use CGI qw/:standard/;
use strict;

#
# Parses text file and builds a form
#

print header, start_html;

print_form();

print end_html;


sub print_form {
	#print qq(<FORM METHOD="POST" ACTION="http://elmo.dce.harvard.edu/~sgaray/hw3/hw3p5b.cgi>);

	print start_form("POST","http://elmo.dce.harvard.edu/~sgaray/hw3/hw3p5b.cgi");

	my $id = open(HANDLE, "<  /export/home/courses/cscie13/sgaray/acme.txt")
		or die ("can't open file $!");

	print "<CENTER>", h2("Order Form");

	print "<TABLE BORDER=1>";

	print "<TR><TD><B>Part#</TD><TD><B>Description</TD><TD><B>Price</TD></TR>";

	LINE: while (<HANDLE>) {

		next LINE unless /(\s{2,}\d+)/;	 # skip non-item lines

		print "<TR>";

		my @line = split /\s{2,}/; # divide the line in 3 pieces
					   # not so flexible, we may say

		my $npiece = 0;	# counter to skip first line and place textfield

		foreach my $piece (@line) {
					   		
			if ($npiece == 1) { 	 	# display the first piece of info
				print 	"<TD>",  	# and a textfield whith item as name
					textfield( -name=> $piece, -size=>2 ),
					"$piece</TD>";
			}
			if ($npiece > 1) {		 # display the rest of the
				print "<TD>$piece</TD>"; # product info
			}

			$npiece++;		# next piece
		}

		print "</TR>";
	}
	
	close(HANDLE);

	print "</TABLE>";

	#print qq(<INPUT TYPE="SUBMIT" VALUE="Submit Order"><INPUT TYPE="RESET"></FORM>);
	
	print submit("Submit Order"), reset;
	print "<CENTER>";
	print endform;


}

