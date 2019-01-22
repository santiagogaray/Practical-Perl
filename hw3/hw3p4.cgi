#!/usr/local/bin/perl -w
use CGI qw/:standard/;
use strict;

#
# System Administration
# Displays elmo indicators
#

print header, start_html, h2("Elmo Status");

display_time();

display_best5("Top 5 processes -CPU usage-","ps -Ao 'pcpu, user, pid, tty, etime, time, comm' | ");
display_best5("Top 5 processes -Memory usage-","ps -Ao 'pmem, user, pid, tty, etime, vsz, comm' | ");

display_comm("Last 5 loggins", "last | head -5 | ");
display_comm("Last 5 lines in log file", "tail -5 /var/adm/messages | ");


print end_html;

# Time and average values

sub display_time {

	my @data = split /,/, `uptime`;		#get info and parse it
	

	print h4("Uptime"),
		p("$data[0]"),			#display time
		hr;

	my $activate = 0;

	foreach my $piece (@data) {

		if ($piece =~ m/load average:/) {	# when found 'load average: '
			$activate = 1;			# start displaying
			print h4("Average system load");
			$piece =~ s/load average://;
		}
		if ($activate ==1) {			# the following
			print p("$piece");		# values
		}
	}
	print hr;
}

# Displays the 5 grater values of the 
# first data obtained in input line

sub display_best5 {

	print h4($_[0]);	# Dislpay title of command


	my $id = open(HANDLE, $_[1])
		or die "can't read from it";


	my %data;
	my @titles;

	while (<HANDLE>) {

		if ($. > 1) {			# if not the first line
			/\d+\.\d+/;		# trat it as an input to process
			push @{$data{$&} } , $';
		}
		else { 
			@titles = split /\s+/;	# else are the titles in table
		}
	}
	close(HANDLE);

	print "<TABLE BORDER=1><TR>";

	foreach my $title (@titles) {
		print "<TD>$title</TD>";	# print titles
	}
	print "</TR>";

	my $counter = 0;
	
	LOOP: foreach my $perc (reverse sort keys %data) { # sort and get arrays of processes
							   # starting from the bigger values

		foreach my $proc ( @{ $data{$perc} } ) { 	# get one input process

			my @prinfo = split /\s+/, $proc;	# parse process

			print "<TR><TD>$perc</TD>";		# display value of process

			foreach my $piece ( @prinfo ) {		# dislay rest of process info
				unless ($piece eq "") {		# discard blank lines
					print "<TD>$piece</TD>"; 
				}
			}

			print "</TR>";

			if ($counter++ == 4) { last LOOP; }	# stop when 5 processes have 
		}						# been displayed
	}

	print "</TABLE>", hr;
}

# Displays output of commands

sub display_comm {

	print h4($_[0]);	# diplay title

	my $id = open(HANDLE, $_[1])	# command passed as parameter 
		or die "can't read from it";

	while (<HANDLE>) {
		print p("$_");	#display output line
	}
	close(HANDLE);

	print hr;
}


