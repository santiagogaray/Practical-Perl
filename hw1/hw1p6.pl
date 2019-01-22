#!/usr/local/bin/perl -w

$nhits = 0;
open(LOGFILE,"large_access.log") or die "Can't open log-file\n";
while ($line = <LOGFILE>) {
	($add, $usr, $auth, $date1, $date2, $req1, $req2, $req3, $stat,
	$size) = split(" ", $line);
	$subdate = substr($date1,0,7);
	if ($subdate eq "[19/Jan" && $stat == 404)  {
		$nhits++;
	}
}
print"The server responded $nhits times on January 19th with status code 404.\n";
