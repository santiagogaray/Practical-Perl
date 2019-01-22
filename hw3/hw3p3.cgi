#!/usr/local/bin/perl -w
use CGI qw/:standard/;
use strict;


#
# Virtual website
# Redirects to urls referenced by PATH_INFO
#

my %path_urls = get_urltable();	 	# loads urls from file
my $path = $ENV{PATH_INFO};		# get virtual path
print redirect(	$path_urls{$path});	# redirects to url


sub get_urltable {
	my $path;
	my $url;
	my %urltable;	# a hash to handle paths and its respective urls

	open(URLTABLE, "<  /export/home/courses/cscie13/sgaray/redirect_table.txt") || die ("can't open file $!");  

	while (<URLTABLE>) {
		($path, $url) = split (' ');	# divide in two the input line
		$urltable{$path} = $url;	# place them in a table for easy searching
	}
	close (URLTABLE);

	return %urltable;			# return this table
}
