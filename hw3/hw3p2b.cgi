#!/usr/local/bin/perl -w
use CGI qw/:standard/;
use strict;

#
# Random link generator called from hw3p2a.cgi
#

my @urls = get_urls();	 	# loads urls
my $randurl = int(rand 11);	# gets a random number


print "Location: $urls[$randurl]\n\n";  # redirect to the randomly
					# chosen link



sub get_urls {
	my @urlist;
	while (<DATA> ) {		# get the link
    		push @urlist, $_;	# load it in the array
	}
	return @urlist;			# pass the array
}

__DATA__
http://www.mediabuilder.com/softwarevrmlauthor.html
http://liftoff.msfc.nasa.gov/vr/vr.html
http://ww3.cyberworldcorp.com/corpsite/gallery/gallery_main.html
http://www.caip.rutgers.edu/vr2000
http://www.blender.nl/download/index.php
http://www.3deurope.com/page/ImagesPage.php3?randval=71889
http://3dtotal.com/home/home.htm
ftp://ftp.dcs.ed.ac.uk/pub/objects/vrml/sgilogo.wrl.gz
http://graphics.stanford.edu/courses/cs248-99/proj3/
http://www.acm.org/tog/resources/RTR/#speed
http://www.3dgate.com/news_and_opinions/000424/0424bfox.html
