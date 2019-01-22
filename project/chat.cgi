#!/usr/bin/perl -w

use strict;

use CGI;
#use lib '.';
use CGIBook::Error;
#use HTML::Template;
#use CGI::Carp qw/fatalsToBrowser/;
use DBI;

use vars qw( $DATA_DIR );
local $DATA_DIR	= "/disk5/courses/cscie13/sgaray/public_html/project/data";


my $q		= new CGI;

my $action	= $q->param("action") or "undef";

if ( $action eq "log_in" ||
	 $action eq "new_member" || 
	 $action eq "update" ) {
	checkPurgeList();		# make check routine of logged people
}

if ( $action eq "log_in" ) {		# log-in member
    log_in( $q );
}
elsif ( $action eq "new_member" ) {	# create new member
    new_member( $q );
}
elsif ( $action eq "update" ) {		# update member on list
    update_member( $q );			# to keep updated
}
elsif ( $action eq "open_session" ) {	# asks for a connection 
    open_session( $q );					# with a logged member
}
elsif ( $action eq "chk_requests" ) {	# checks for possible 
    check_calls( $q );					# connection requests
}
elsif ( $action eq "post_message" ) {	# sends message to
    post_message( $q );					# connected member
}
elsif ( $action eq "get_message" ) {	# sends message to
    get_message( $q );					# connected member
}
elsif ( $action eq "close_session" ) {	# sends message to
    close_session( $q );				# connected member
}


#--------------------- Actions -------------------------------------

############################################
# tries to log member and sends $id 
# or "NR" / "AR"  message to Shockwave movie
############################################
sub log_in {
	my $q = shift;

		#check first if user already logged
	my @data = file2array("$DATA_DIR/logged");
	my $username = $q->param('name');
	if ($data[0] =~ m/$username/) {
		printMsg('AR');
		return;
	}
		#check in database if user registered
	my $id = log_account( $q );
	if ( $id ) {
		reg_member( $q );
		printMsg($id);				# return member id 
	}else {
		printMsg('NR');				# or error id if
	}								# not found

}

##############################################
# tries to create a member account and 
# sends $id or "NR" message to Shockwave movie
##############################################
sub new_member {
	my $q = shift;
	my $id = create_account( $q );
			
	if ( $id ) {
		reg_member( $q );
		printMsg($id);				# return member id 
	}else {
		printMsg('NR');				# or error id if
	}								# not found
}

#######################################
# Updates a logged member
# in current session - checks first id.
# Returns updated list of logged people
#######################################
sub update_member {
	my $q  = shift;

		# check member id
	unless ( check_id( $q )) {
		printMsg ( "NR" );	# returns 'not registered'
		return;				# to movie
	}
		# update member in log file
	reg_member( $q );	
	

		# get data
	my @people = file2array("$DATA_DIR/logged");
	
		# return logged list to movie
	printMsg( @people );

}

#######################################
# Opens a chat session request from one
# user to the other
# Returns a request confirmation
#######################################
sub open_session {
	my $q  = shift;

		# check member id
	unless ( check_id( $q )) {
		printMsg ( "NR" );	# returns 'not registered'
		return;				# to movie
	}

	my $username = $q->param('name');	
	my $requested = $q->param('data');

		#delete in case there's an old request
	unlink "$DATA_DIR/call_$requested";
		#create new file : 
		# filename, the name of the requested
		# data stored, the name of the requester 
	if (open(CALL, "> $DATA_DIR/call_$requested")) {
		print CALL "$username";
		close CALL;
		printMsg( 'REQ' );	# return 'requested' to movie
	}else {
		printMsg( 'NRE' );	# return 'not requested' to movie
	}
}

##########################################
# Checks for possible connections request
# and returns the requester name.
##########################################
sub check_calls {
	my $q  = shift;

		# check member id
	unless ( check_id( $q )) {
		printMsg ( "NR" );	# returns 'not registered'
		return;				# to movie
	}

	my $username = $q->param('name');	
	my $requester;

		#find a request file
	if (open(DATA, "$DATA_DIR/call_$username")) {
		while(<DATA>) {
			$requester = $_; 
		}
		close DATA;
		printMsg( "$requester" );	# return requester to movie
	}else {
		printMsg( 'NRE' );			# return 'not requested' to movie
	}

}

##########################################
# Posts a message from a member connected
# to another member.
##########################################
sub post_message {

	my $q  = shift;

		# check member id
	unless ( check_id( $q )) {
		printMsg ( "NR" );	# returns 'not registered'
		return;				# to movie
	}

		# get data from sender
	my $username = $q->param('name');
	my $message = $q->param('data');

		# create or append message to message file
		# or return error
	if (open(DATA, ">>$DATA_DIR/msgs_$username")) {
		print DATA "$message\n";
		close DATA;
		printMsg( "PM" );	# return 'posted message' to movie
	}else {
		printMsg( "NP" );	# return 'not posted' to movie
	}

}

#############################################
# Gets a message from a member connected
# with this member or detects session closed.
#############################################
sub get_message {

	my $q  = shift;

		# check member id
	unless ( check_id( $q )) {
		printMsg ( "NR" );	# returns 'not registered'
		return;				# to movie
	}

		# get data from sender
	my $username = $q->param('name');
	my $member = $q->param('data');
	my $message;

		# check if chat session still active
	if (not ( open (DATA, "$DATA_DIR/call_$username") or
		open (DATA, "$DATA_DIR/call_$member") ) ) {
		printMsg( "CL" );		# return 'closed session' to movie
		return;
	}else {
		close DATA; 
	}

		# check if message file exists
	if (open(DATA, "$DATA_DIR/msgs_$member")) {
		while(<DATA>) {
			$message = "$message$_";
		}
		close DATA;
		printMsg( "$message" );	# return 'posted message' to movie
		unlink "$DATA_DIR/msgs_$member";
	}else {
		printMsg( "NM" );		# return 'no message' to movie
	}

}

##########################################
# Closes a connection that has been
# established between this user and 
# a another member. 
##########################################
sub close_session {

	my $q  = shift;

		# check member id
	unless ( check_id( $q )) {
		printMsg ( "NR" );	# returns 'not registered'
		return;				# to movie
	}

		# get data from sender
	my $username = $q->param('name');
	my $member = $q->param('data');
	my $message;

		# try to close connection (delete connection files)
	if (unlink "$DATA_DIR/call_$username" or
		unlink "$DATA_DIR/call_$member") {
			#delete message files
		unlink "$DATA_DIR/msgs_$username";
		unlink "$DATA_DIR/msgs_$member";
		printMsg( "CL" );	# return 'closed' to movie
	}else {
		printMsg( "NC" );	# return 'not closed' to movie
	}

}





# ------------- Main functions -------------------------------------

#################################
# retrieves a saved account info 
# from database and returns id
#################################
sub log_account {
	my $q  = shift;
	my $id = '';

		#get posted name and password
	my $username = $q->param('name');
	my $password = $q->param('password');

		#load values from accounts table
	my $dbh = open_dbase( 'sgaray', 'sgaray', '7132' );
	my $sqlh = exe_dbase( $dbh, qq{
		SELECT password,id FROM accounts WHERE username="$username"
	} );

	if (my @row = $sqlh->fetchrow_array) {
		if ( crypt( $password, $row[0] ) eq $row[0] ) {
			$id = $row[1];
		}
	}
	close_dbase( $sqlh, $dbh );
	return $id;
}


##############################################################
# saves account info in database along with the current id
# Checks for errors in entries.
##############################################################
sub create_account {
	my $q  = shift;
		#get form values
	my $username = $q->param('name');
	
	my $password = $q->param('password');
		my $slt = join '', ('.', '/', 0..9, 'A'..'Z', 'a'..'z')[rand 64, rand 64];
		my $crpwd = crypt( $password, $slt );

	my $id = unique_id();
		#store values in accounts table
	my $dbh = open_dbase( 'sgaray', 'sgaray', '7132' );

	my $sqlh = exe_dbase( $dbh, qq{ INSERT INTO accounts VALUES
		( "$username", "$crpwd", " ", " ", "$id" ) } );

	close_dbase( $sqlh, $dbh );
	return $id;
}

#######################################################
# Register a member in a text file
# of current logged people. Posts time of registration
#######################################################
sub reg_member {
	my $q  = shift;
	my $name = $q->param('name');
	my $regtime = time();		# time of registration


		# get data
	my @oldlist = file2array("$DATA_DIR/logged");		
	my $newdata;

		# check member in last registration log
	if ($oldlist[0] =~ m/$name/) {
		$oldlist[0] =~ s/$name,\d+/$name,$regtime/;
		unlink "$DATA_DIR/logged";		#replace file with a new 
		$newdata = $oldlist[0];			#created file and place new list
	}else {
		$newdata = "$name,$regtime,";	# or append new user
	}									# in existing	list

		#create or append file
	open(LOGIN, ">> $DATA_DIR/logged") or
		return 0;	

		#place data
	print LOGIN "$newdata";
	close LOGIN;

	return 1;
}

#########################################
# Checks if its time to make
# a list purge and updates time of purge
#########################################
sub checkPurgeList() {
	my $now = time();
	my $last;
	
	# get time from text file and check
	# if lapse time for checking users
	# has reached
	if (open (TIME, "$DATA_DIR/updateTime")) {
		while (<TIME> ) {		#get the time
			$last = $_;
			if ( ($now - $last) > 30 ) {
				timeToPurge($now);	# its time to clean
			} else {
				return 0;
			}
		}
		close TIME;
		unlink "$DATA_DIR/updateTime"; # delete file
	}

		#create new file and place new time
	open (TIME, ">$DATA_DIR/updateTime") or return 0;	
	print TIME "$now";
	close TIME;

	return 1;
}

#########################################
# Verifies if every logged person has been
# updating its registration. If not is is
# unregistered from the log file. 
#########################################
sub timeToPurge() {
	my $now = shift;
	my @data = file2array("$DATA_DIR/logged");
	
		# create person-time hash to check time
	my %people_time = $data[0] =~ /(\w+),(\d+)/g;

	foreach my $person ( keys %people_time ) {
		my $histime = $people_time{$person};
			# if time of last registration was mase
			# more than 30 seconds ago then unregister user 
		$data[0] =~ s/$person,\d+,//
			if (($now - $histime) > 30);
	}

		
		# delete not updated file
	unlink "$DATA_DIR/logged";
		#create new file
	open(LOGIN, "> $DATA_DIR/logged") or return 0;	
		#place updated list
	print LOGIN "$data[0]";
	close LOGIN;

	return 1;

}




# ------------------ Helper functions --------------------------------

# sends specified message to Shockwave movie
sub printMsg {
	my $msg = shift;
	print "Content-type: text/html\n\n";
	print "$msg";		# return message
}

##########################
# read data from file and 
# stores it in an array 
##########################
sub file2array {
	my $filename = shift;
	my @data;

	open (DATA, "$filename") or
		return 0;

	while (<DATA> ) {		#get one line

    	push @data, $_;		#load it in the array

	}
	close DATA;

	return @data;			#pass the array

}

#########################################
# Checks if the id and name posted
# are from a registered member
#########################################
sub check_id {

	my $q  = shift;
	my $ret_val;

		#get posted name and password
	my $id = $q->param('id');
	my $username = $q->param('name');

		#load values from accounts table
	my $dbh = open_dbase( 'sgaray', 'sgaray', '7132' );
	my $sqlh = exe_dbase( $dbh, qq{
		SELECT id FROM accounts WHERE username="$username"
	} );

	if (my @row = $sqlh->fetchrow_array) {
		$ret_val = 1  if ( $id eq $row[0] )  or
			$ret_val = 0;
	}

	close_dbase( $sqlh, $dbh );
	return $ret_val;

}

##############################################################
# opens database connection with given parameters
##############################################################
sub open_dbase {
		# Connect to database
	my ( $DB, $USER, $PASSWORD ) = @_;

	my $dbh = DBI->connect("dbi:mysql:$DB", $USER, $PASSWORD);
		die "Can't connect to database" unless $dbh;	
	return $dbh;
}

##############################################################
# executes opened database with given command
##############################################################
sub exe_dbase {
	my ( $dbh, $comm)  = @_;
	
	my $sqlh = $dbh->prepare(qq/$comm/);
		die "Can't connect to database" unless $sqlh;
	$sqlh->execute;
		die "An error: $DBI::errstr" if $DBI::errstr;
	return $sqlh;
}

##############################################################
# closes database connection with given parameters
##############################################################
sub close_dbase {
	my ( $sqlh, $dbh ) = @_;

		# Release the SQL statement	
	$sqlh->finish;
 		# Disconnect from the database
	$dbh->disconnect;	
}


############################################
# generates unique id number for new account
############################################
sub unique_id {
    # Use Apache's mod_unique_id if available
    return $ENV{UNIQUE_ID} if exists $ENV{UNIQUE_ID};
    
    require Digest::MD5;
    
    my $md5 = new Digest::MD5;
    my $remote = $ENV{REMOTE_ADDR} . $ENV{REMOTE_PORT};
    
    # Note this is intended to be unique, and not unguessable
    # It should not be used for generating keys to sensitive data
    my $id = $md5->md5_base64( time, $$, $remote );
    $id =~ tr|+/=|-_.|;  # Make non-word chars URL-friendly
    return $id;
}
