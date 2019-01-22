#!/usr/local/bin/perl -w
use CGI qw/:standard/;
use DBI;

$DB = 'hw4';
$USER = 'sgaray';
$PASSWORD = 7132;

# Connect to database

$dbh = DBI->connect("dbi:mysql:$DB", $USER, $PASSWORD);
	die "Can't connect to database" unless $dbh;

$sqlh = $dbh->prepare("SELECT * FROM rooms");
	die "Can't connect to database" unless $sqlh;

$sqlh->execute;
	die "An error: $DBI::errstr" if $DBI::errstr;

print header();
print start_html(-title=>'H4p3');
print "<TABLE BORDER=1>";
$count = 0;
while (@row = $sqlh->fetchrow_array) {
	$count++;
	print "<TR><TD>Row $count: </TD><TD> @row </TD></TR>";
}
print "</TABLE>";
print end_html();

	# Release the SQL statement				
$sqlh->finish; 		
	# Disconnect from the database
$dbh->disconnect;	