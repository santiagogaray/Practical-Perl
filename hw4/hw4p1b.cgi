#!/usr/local/bin/perl -w
use CGI qw/:standard/;

#
# Gets the Cookie and displays is within a form
# 

# ask for a specific cookie
my $acookie;
$acookie = cookie('USERNAME');

# display a form using the Cookie value
print header();
print start_html(-title=>'HW4 Q1b');

print start_form("POST","http://elmo.dce.harvard.edu/~sgaray/hw4/hw4p1b.cgi"),
	h3('Account Log On'),
	"Username <BR>",
	textfield( -name=> "USERNAME", -default=>$acookie , -size=>17 ),"<BR>",
	"Password <BR>",
	textfield( -name=> "PASSWORD", -size=>10 ),"<BR>",
	checkbox(-name=>'SAVE_USERNAME',
               -label=>'Check here to save username'),"<BR>",
	submit("Submit Order"), reset;
print endform;

print end_html();

