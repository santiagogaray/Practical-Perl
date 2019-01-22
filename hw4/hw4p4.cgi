#!/usr/local/bin/perl -w
use CGI qw/:standard/;
use CGI::Carp qw/fatalsToBrowser/;
use DBI;

# Inserts posted data in database
# Loads the inserted record and
# displays contents.

	#Stores posted data in array
@names = param;
@values;
$n = 0;
foreach $name (@names) {
	$values[$n] = param($name);
	$n++;
}

	# Connects to databases
$DB = 'sgaray';
$USER = 'sgaray';
$PASSWORD = 7132;

$dbh = DBI->connect("dbi:mysql:$DB", $USER, $PASSWORD);
	die "Can't connect to database" unless $dbh;

	#Inserts data
$sqlh = $dbh->prepare( qq{
	INSERT INTO staff (first,last,address,department,phone,email)
	VALUES ("$values[0]","$values[1]","$values[2]","$values[3]","$values[4]","$values[5]")
	} );
	die "Can't connect to database" unless $sqlh;
$sqlh->execute;
	die "An error: $DBI::errstr" if $DBI::errstr;

	#Reads all the table
$sqlh = $dbh->prepare("SELECT * FROM staff");
	die "Can't connect to database" unless $sqlh;
$sqlh->execute;
	die "An error: $DBI::errstr" if $DBI::errstr;


	# Keeps the last record in array
@lastRow;
while (@row = $sqlh->fetchrow_array) {
	@lastRow = @row;
}

	# Release the SQL statement				
$sqlh->finish; 		
	# Disconnect from the database
$dbh->disconnect;	

	#Display last record inserted in database
print header();
print start_html(-title=>'HW4 Q4');
print h2("Posted Data");

foreach $field (@lastRow) {
	print " $field<BR>";
}

print end_html();

