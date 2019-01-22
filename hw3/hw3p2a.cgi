#!/usr/local/bin/perl -w
use CGI qw/:standard/;
use strict;

#
# Calls the random link generator in hw3p2b.cgi
#

print header, start_html,
	h2("where you'll go this time?"),
	a({href=>"http://elmo.dce.harvard.edu/~sgaray/hw3/hw3p2b.cgi"}, # call url generator
	img {src=>'lucky.gif',align=>'LEFT'}),
	"Click again to change your destiny",
	end_html;

