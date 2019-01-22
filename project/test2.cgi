#!/usr/bin/perl -wT

use strict;

use CGI;
#use lib '.';
use CGIBook::Error;
#use HTML::Template;
use CGI::Carp qw/fatalsToBrowser/;
#use DBI;


my $q       = new CGI;
my $action  = " ";
$action = $q->param("action");
my $id    = $q->param("id");

log_in( $q, $id ); # if ( $action eq "log_in" );

sub log_in {
    my( $q, $id ) = @_;
    my $name = $q->param("name");
    my $pswrd = $q->param("password");
    print "Content-type: text/html\n\n";
    print "Name: $name\n";
    print "Password: $pswrd\n";
#    print $q->header, $q->start_html,
#          $q->p("$name"),
#          $q->end_html;
}
