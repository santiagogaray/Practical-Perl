#!/usr/local/bin/perl -w
use CGI qw/:standard/;

#
# Creates a form and sends it with a session id cookie
# 

# Create and send Cookie
$COOKIE_VALUE = "$ENV{'REMOTE_ADDR'}.$$";

my $cookie;
$cookie = cookie(-name=>"sessionID",-value=>$COOKIE_VALUE,-path=>'/');

# send cookie
print header(-cookie=>$cookie);
print start_html(-title=>'HW4 Q2a');

# Create form 
print start_form("POST","http://elmo.dce.harvard.edu/~sgaray/hw4/hw4p2b.cgi"),
	h3('User Info'),
	"First name <BR>",
	textfield( -name=> "FIRSTNAME", -size=>17 ),"<BR>",
	"Last Name <BR>",
	textfield( -name=> "LASTNAME", -size=>10 ),"<BR>",
	"Office Address <BR>",
	textfield( -name=> "OF_ADDRESS", -size=>50 ),"<BR>",
	"Department <BR>",
	textfield( -name=> "DEPARTMENT", -size=>17 ),"<BR>",
	"Phone Number <BR>",
	textfield( -name=> "PHONE", -size=>10 ),"<BR><BR>",
	submit("Submit Order"), " ", reset;
print endform;

print end_html();