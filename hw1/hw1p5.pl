#!/usr/local/bin/perl -w

print "Where is the log? ";
$logfile = <STDIN>;
print "What URL do you want to find: ";
$url = <STDIN>;
$nhits = 0;

open(LOGFILE,"$logfile") or die "Can't open log-file\n";
while ($line = <LOGFILE>) {
	($add, $usr, $auth, $date1, $date2, $req1, $req2, $req3, $stat,
$size) = split(" ", $line);
	if ("$req2\n" eq $url)  {
		$nhits++;
	}
}
print"There was $nhits hits on that URL.\n";
