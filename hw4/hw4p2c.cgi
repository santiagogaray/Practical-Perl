#!/usr/local/bin/perl -w
use CGI qw/:standard/;

#
# Gets a cookie and uses its value
# to open and read a previously saved
# file.
#

# ask for the cookie
my $acookie;
$acookie = cookie("sessionID");

print header();
print start_html(-title=>'HW4 Q2c');

# open file with the Cookie's value as filename
open (IN,"/export/home/courses/cscie13/sgaray/logs/$acookie")
	|| die"can't open file";

# Display data
while (<IN>) {
	print "$_<BR>";
}

print end_html();

