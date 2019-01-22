#!/usr/bin/perl -wT

use strict;

use CGI;
use CGI qw/:standard/;
use lib '.';
use CGIBook::Error;
use HTML::Template;
use CGI::Carp qw/fatalsToBrowser/;
use DBI;

BEGIN {
    $ENV{PATH} = "/bin:/usr/bin";
    delete @ENV{ qw( IFS CDPATH ENV BASH_ENV ) };
    sub unindent;
}

use vars qw( $DATA_DIR $SENDMAIL $SALES_EMAIL $MAX_FILES );

local $DATA_DIR     = "/disk5/courses/cscie13/sgaray/public_html/hw5/data";
local $SENDMAIL     = "/usr/lib/sendmail -t -n";
local $SALES_EMAIL  = 'santiagogaray@msn.com';
local $MAX_FILES    = 1000;

	# specifies when to make the calculation in the catalog
our $do_calc = 0;
	# cookie to be sent 
our $newcookie;

my $q       = new CGI;
my $action  = $q->param("action") || 'start';
my $id      = get_id( $q );

if ( $action eq "start" ) {
    start( $q, $id );
}
elsif ( $action eq "account" ) {	# Create account form
    account( $q, $id );
}
elsif ( $action eq "catalog" ) {
    catalog( $q, $id );
}
elsif ( $action eq "cart" ) {
    cart( $q, $id );
}
elsif ( $action eq "checkout" ) {
    checkout( $q, $id );
}
elsif ( $action eq "thanks" ) {
    thanks( $q, $id );
}
else {
    start( $q, $id );
}


#/--------------------------------------------------------------------
# Page Handling subs
# 


sub start {

    my( $q, $id ) = @_;

    print header( $q, "Welcome!" ),
          $q->p( "Welcome! You've arrived at the world famous Tennis Shoppe! ",
                 "Here, you can order videos of famous tennis matches from ",
                 "the ATP and WTA tour. Well, mate, are you are ready? ",
                 "Click on one of the links below:"
          ),
          footer( $q, $id );
}

##############################################################
# Account creation. Displays form.
# Sends values to save_account() function for verification
# and saving.
# Displays error message if entries are invalid.
##############################################################
sub account {
    my( $q, $id ) = @_;
    my $errmessage;
   
    if ( $q->request_method eq "POST" ) {
	$errmessage = save_account( $q, $id );
    }
    
    print header( $q, "Account Creation" ), p("$errmessage"),
          $q->start_form,
          $q->table(
              { -border       => 1,
                -cellspacing  => 1,
                -cellpadding  => 4,
              },
              $q->Tr( [
                  $q->td( [
                      "Username",
                      $q->textfield(
                          -name   => "Username",
                          -size   => 12
                      )                      
                  ] ),
                  $q->td( [
                      "Password",
                      $q->password_field(
                          -name   => "Password",
                          -size   => 32
                      )                      
                  ] ),
                  $q->td( [
                      "Email Address",
                      $q->textfield(
                          -name   => "Email",
                          -size   => 50
                      )                      
                  ] ),
                  $q->td( [
                      "Credit Card Number",
                      $q->textfield(
                          -name   => "CreditCard",
                          -size   => 15
                      )                      
                  ] ),
                  $q->td( { -colspan  => 3,
                            -align    => "right",
                            -bgcolor  => "#CCCCCC"
                          },
                          $q->submit( "Create" )
                  )
              ] ),
          ),
          $q->hidden(
              -name     => "id",
              -default  => $id,
              -override => 1
          ),
          $q->hidden(
              -name     => "action",
              -default  => "account",
              -override => 1
          ),
          $q->end_form,
          footer( $q, $id );
}

##############################################################
# Displays catalog form loaded from database
# Displays Totals when Update is pressed
##############################################################
sub catalog {
    my( $q, $id ) = @_;
    if ( $q->request_method eq "POST" ) {
	save_state( $q );
	$do_calc = 1;
    }

		#database connection and execution
	my $dbh = open_dbase( 'hw5', 'catalog', 'catalog' );
	my $sqlh = exe_dbase( $dbh, "SELECT itemnum,title,price FROM catalog" );

	print header( $q, "Video Catalog" ),
	$q->start_form,
	"<TABLE CELLSPACING=1 BORDER=1 CELLPADDING=4>",
	$q->th( { -bgcolor => "#CCCCCC" }, [
		"Quantity",
		"Video",
		"Item Price",
		"Total Price"
	] );

		# display each line of database table in form
	my $grandTotal = 0;
	while (my @row = $sqlh->fetchrow_array) {

		#calculate total price
		my $totalPrice = 0;
		$totalPrice = $q->param("$row[0]") * $row[2] if $do_calc;
		$grandTotal = $grandTotal + $totalPrice if $do_calc;
		$totalPrice = sprintf("%.2f",$totalPrice);

		print	"<TR>",
			$q->td( [
        			$q->textfield(
				-name   => "$row[0]",
				-size   => 2
				),
				"$row[1]",
				"$row[2]",
				"$totalPrice"
			] ),
		"</TR>";
	}
		# display Total value of products
	$grandTotal = sprintf("%.2f",$grandTotal);
	print	"<TR><TD></TD><TD></TD><TD>Total</TD><TD>$grandTotal</TD></TR>";

	print 	$q->td( { -colspan  => 4,
			  -align    => "right",
			  -bgcolor  => "#CCCCCC"
		},
		$q->submit( "Update" )
	),
	"</TABLE>",
	$q->hidden(
		-name     => "id",
		-default  => $id,
		-override => 1
	),
	$q->hidden(
		-name     => "action",
		-default  => "catalog",
		-override => 1
	),
	$q->end_form,
	footer( $q, $id );

	close_dbase( $sqlh, $dbh );
 

}

sub cart {
    	my( $q, $id ) = @_;

		# update to state previously saved
    	load_state( $q, $id );
	my @items = get_items( $q );

	my @item_rows = @items ?
        map $q->td( $_ ), @items :
        $q->td( { -colspan => 4 }, "Your cart is empty: $id" );
        
    	print header( $q, "Your Shopping Cart" ),
	      $q->table(
              { -border       => 1,
                -cellspacing  => 1,
                -cellpadding  => 4,
              },
              $q->Tr( [
                  $q->th( { -bgcolor=> "#CCCCCC" }, [
                      "Video Title",
                      "Quantity",
		      "Item Price",
		      "Total Price"
                  ] ),
                  @item_rows
              ] )
          ),
	footer( $q, $id );
}


sub checkout {
    my( $q, $id ) = @_;
    
    print header( $q, "Checkout" ),
          $q->start_form,
          $q->table(
              { -border       => 1,
                -cellspacing  => 1,
                -cellpadding  => 4
              },
              $q->Tr( [
                  map( $q->td( [
                          $_,
                          $q->textfield( lc $_ )
                       ] ), qw( Name Email Address City State Zip )
                  ),
                  $q->td( { -colspan  => 2,
                            -align    => "right",
                          },
                          $q->submit( "Checkout" )
                  )
              ] ),
          ),
          $q->hidden(
              -name     => "id",
              -default  => $id,
              -override => 1
          ),
          $q->hidden(
              -name     => "action",
              -default  => "thanks",
              -override => 1
          ),
          $q->end_form,
          footer( $q, $id );
}


sub thanks {
    my( $q, $id ) = @_;
    my @missing;
    my %customer;
    
    my @items = get_items( $q );
    
    unless ( @items ) {
        save_state( $q );
        error( $q, "Please select some items before checking out." );
    }
    
    foreach ( qw( name email address city state zip ) ) {
        $customer{$_} = $q->param( $_ ) || push @missing, $_;
    }
    
    if ( @missing ) {
        my $missing = join ", ", @missing;
        error( $q, "You left the following required fields blank: $missing" );
    }
    
    email_sales( \%customer, \@items );
    unlink cart_filename( $id ) or die "Cannot remove user's cart file: $!";
    
    print header( $q, "Thank You!" ),
          $q->p( "Thanks for shopping with us, $customer{name}. ",
                 "We will contactly you shortly!"
          ),
          $q->end_html;
}


#/--------------------------------------------------------------------
# State subs
# 

##############################################################
# Checks for an id as a file. 
# Checks for the id as a cookie or creates the cookie.		##cookie not working
# Creates an id if not is found
##############################################################
sub get_id {
    my $q = shift;
    my $id;
    
    my $unsafe_id = $q->param( "id" ) || '';
    $unsafe_id =~ s/[^\dA-Fa-f]//g;
    
    if ( $unsafe_id =~ /^(.+)$/ ) {
        $id = $1;
        if (not load_state( $q, $id ) ) {		# file not found? #
		my $acookie = cookie('sessionId');	
		if ( $acookie ) {			# check for cookie #
			$id = $acookie;
        		$q->param( -name => "id", -value => $id ); # check this: not working #
			load_state( $q, $id );			   ###########################
			$do_calc = 1;
		} else {				# create one if not found #				$newcookie = cookie(-name=>'sessionId',-value=>"$id",-path=>'/~sgaray/hw5');
		}
	}
    }
    else {
        $id = unique_id();
        $q->param( -name => "id", -value => $id );
    }
    
    return $id;
}

# Loads the current CGI object's default parameters from the saved state
sub load_state {
    my( $q, $id ) = @_;
    my $saved = get_state( $id );
    $saved or return 1;
    
    foreach ( $saved->param ) {
        $q->param( $_ => $saved->param($_) ) unless defined $q->param($_);
    }
    return 0;
}


# Reads a saved CGI object from disk and return its params as a hash ref
sub get_state {
    my $id = shift;
    my $cart = cart_filename( $id );
    local *FILE;
    
    -e $cart or return;
    open FILE, $cart or die "Cannot open $cart: $!";
    my $q_saved = new CGI( \*FILE ) or
        error( $q, "Unable to restore saved state." );
    close FILE;
    
    return $q_saved;
}


# Saves the current CGI object to disk
sub save_state {
    my $q = shift;
    my $cart = cart_filename( $id );
    local( *FILE, *DIR );
    
    	# Avoid DoS attacks by limiting the number of data files
    my $num_files = 0;
    opendir DIR, $DATA_DIR;
    $num_files++ while readdir DIR;
    closedir DIR;
    
    	# Compare the file count against the max
    if ( $num_files > $MAX_FILES ) {
        error( $q, "We cannot save your request because the directory " .
                   "is full. Please try again later" );
    }
    
    	# Save the current CGI object to disk
    open FILE, "> $cart" or return die "Cannot write to $cart: $!";
    $q->save( \*FILE );
    close FILE;
}

##############################################################
# Creates a list of Products with its titles, quantity, 
# item price, total net price and total global price.
# The table is returned as an array.
##############################################################
sub get_items {
    	my $q = shift;
    	my @items;
    
	my $grandTotal = 0;

		#database connection
	my $dbh = open_dbase( 'hw5', 'catalog', 'catalog' );

    		# Build a sorted list of movie titles, quantities and prices
    	foreach ( $q->param ) {

        my( $id, $quantity) = ( $_, $q->param( $_ ) );
        
        	# Skip cero qauntity items and other keys
        $id =~ m/\d+/ or next;
        $quantity or next;

		#database execution
        my $sqlh = exe_dbase( $dbh, qq/SELECT title,price FROM catalog WHERE itemnum="$id"/ );
	my @row = $sqlh->fetchrow_array;
	my ( $title, $price ) = @row;

		#calculate total price
	my $totalPrice =  $quantity * $price;
	$totalPrice = sprintf("%.2f",$totalPrice);	
	$grandTotal = $grandTotal + $totalPrice;

		#store values
        push @items, [ $title, $quantity, $price, $totalPrice ];
    }
	push @items, [ '', '', 'Total', $grandTotal ];
    return @items;
}


# Separated from other code in case this changes in the future
sub cart_filename {
    my $id = shift;
    return "$DATA_DIR/$id";
}


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


#/--------------------------------------------------------------------
# Other helper subs
#


##############################################################
# saves account info in database along with the current id
# Checks for errors in entries.
##############################################################
sub save_account {
    my( $q, $id ) = @_;
		#get form values
	my $username = $q->param('Username');
		return 'Error in Username field, please reenter text.'
			 if  ($username =~ /\s+/ );
	my $password = $q->param('Password');
	my $email = $q->param('Email');
		return 'Error in Email Address field, please reenter text.'
			 unless ( $email =~ /\@/ );
	my $creditcard = $q->param('CreditCard');
		return 'Error in Credit Card number field, please reenter text.'
			 unless  ($creditcard =~ /\d{15}/ );

		#store values in accounts table
	my $dbh = open_dbase( 'sgaray', 'sgaray', '7132' );
	my $sqlh = exe_dbase( $dbh, qq{
		INSERT INTO accounts VALUES
		( "$username", "$password", "$email", "$creditcard", "$id" )
	} );

	close_dbase( $sqlh, $dbh );
	return 'Account created';
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

# creates page standard header and sends cookie
sub header {
    my( $q, $title ) = @_;

    return $q->header( "text/html", -cookie=>$newcookie ) . # send cookie now
           $q->start_html(
               -title    => "The Tennis Shoppe: $title",
               -bgcolor  => "white"
           ) .
           $q->h2( $title ) .
           $q->hr;
}


sub footer {
    my( $q, $id ) = @_;
    my $url = $q->script_name;

    my $account_link = 
       $q->a( { -href => "$url?action=account&id=$id" }, "Create Account" );
    my $catalog_link = 
       $q->a( { -href => "$url?action=catalog&id=$id" }, "View Catalog" );
    my $cart_link = 
       $q->a( { -href => "$url?action=cart&id=$id" }, "Show Current Cart" );
    my $checkout_link = 
       $q->a( { -href => "$url?action=checkout&id=$id" }, "Checkout" );
    
    return $q->hr .
           $q->p( "[ $account_link | $catalog_link | $cart_link | $checkout_link ]" ) .
           $q->end_html;
}


sub email_sales {
    my( $customer, $items ) = @_;
    my $remote = $ENV{REMOTE_HOST} || $ENV{REMOTE_ADDR};
    local *MAIL;
    
    my @item_rows  = map sprintf( "%-50s     %4d", @$_ ), @$items;
    my $item_table = join "\n", @item_rows;
    
    open MAIL, "| $SENDMAIL" or
        die "Cannot create pipe to sendmail: $!";
    
    print MAIL unindent <<"    END_OF_MESSAGE";
        To: $SALES_EMAIL
        Reply-to: $customer->{email}
        Subject: New Order
        Mime-Version: 1.0
        Content-Type: text/plain; charset="us-ascii"
        X-Mailer: WWW to Mail Gateway
        X-Remote-Host: $remote
        
        Here is a new order from the web site.
        
        Name:       $customer->{name}
        Email:      $customer->{email}
        Address:    $customer->{address}
        City:       $customer->{city}
        State:      $customer->{state}
        Zip:        $customer->{zip}
        
        Title                                               Quantity
        -----                                               --------
    END_OF_MESSAGE
    print MAIL "$item_table\n";
    close MAIL or die "Could not send message via sendmail: $!";
}


sub unindent {
    local $_ = shift;    
    my( $indent ) = sort
                    map /^(\s*)\S/,
                    split /\n/;
    s/^$indent//gm;
    return $_;
}
