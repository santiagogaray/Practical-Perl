#!/usr/local/bin/perl -w

$total = 0;
$ln = 0;
open(LOGFILE,"@ARGV") or die "Can't open log-file\n";
while ($line = <LOGFILE>) {
	($add, $usr, $auth, $date1, $date2, $req1, $req2, $req3, $stat,
$size) = split(" ", $line);
	$ln++;
	print "Read in line #$ln\n";
	$total += $size;
}

print "The total bytes sent by the server is $total\n";
 
