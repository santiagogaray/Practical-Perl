#!/usr/local/bin/perl -w
use CGI qw/:standard/;

#
# Gets a cookie and uses its value
# as the name of a file where the
# the posted data is saved.
#

# ask for the cookie
my $acookie;
$acookie = cookie("sessionID");

# create file using cookie as name
open (OUT,">>/export/home/courses/cscie13/sgaray/logs/$acookie") 
		|| die"can't open file";

#save data posted
my $q = new CGI;
$q->save(OUT);
   
close OUT;

# display states 
my @names = param;

print header();
print start_html(-title=>'HW4 Q2b');
print h2("Thank you");

foreach my $name (@names) {
	my $value = param($name);
	print "$name = $value <BR>";
}

print end_html();

