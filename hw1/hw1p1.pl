#!/usr/local/bin/perl -w

open(LOGFILE,"@ARGV") or die "Can't open log-file\n";
while ($line = <LOGFILE>) {
	print "$line/n";
}
 
