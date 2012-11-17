#!/usr/bin/perl

#
#Note that dictServer.pl must be running for the client to work!
#Author: Chris Hokamp
#Fall 2012

use strict;
use warnings;
use IO::Socket;

my $sock = IO::Socket::INET->new(
       		PeerAddr => 'localhost',
       		PeerPort => '6789',
       		Proto => 'tcp',
       		Reuse => 1,
);
die "Could not create socket: $!\n" unless $sock;
$sock->autoflush(1);

sub getJson {
	#print "inside top synonyms\n";
	my $query = $_[0];	
    #print "getJson client query $query\n";
	#to be safe
	chomp($query);
	#print "sending $query to server \n";
	if (length($query) > 0) {
		print $sock $query."\n";
	}
	my $res = <$sock>;
	chomp($res);
	#TODO: close the socket properly

	return $res;
}

#TEST
#my $res = &topMatches('natural language processing lit lab computer science Rada Mihalcea');
#my $res = &getJson('');

#print $res."\n";

1;
