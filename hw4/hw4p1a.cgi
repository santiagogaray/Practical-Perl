#!/usr/local/bin/perl -w
use CGI qw/:standard/;

#
# Sends a cookie to ~sgaray/hw4 URL
#


# Create the Cookie

my $cookie;
$cookie = cookie(-name=>"USERNAME",-value=>"Santiago Garay",-path=>'/~sgaray/hw4');

# send the Cookie to the Browser

print header(-cookie=>$cookie);
print start_html(-title=>'HW4 Q1a');
print h2('Cookie USERNAME was sent');
print end_html();

