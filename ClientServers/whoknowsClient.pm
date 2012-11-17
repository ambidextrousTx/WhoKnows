#!/usr/bin/perl

#This is a client for the LIT SaLSA interface dictionary
#Note that dictServer.pl must be running for the client to work!
#Author: Chris Hokamp
#Fall 2012

use strict;
use warnings;
use IO::Socket;

my $sock = IO::Socket::INET->new(
       		PeerAddr => 'localhost',
       		PeerPort => '5678',
       		Proto => 'tcp',
       		Reuse => 1,
);
die "Could not create socket: $!\n" unless $sock;
$sock->autoflush(1);

sub topMatches {
	#print "inside top synonyms\n";
	my $query = $_[0];	
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
#my $res = &topMatches('epidemiology disease network pandemic bees models virus outbreak computational');
#my $res = &topMatches('human computer interaction');
#my $res = &topMatches('security network networking computer cryptography'); -  GETTING ZEROS
#my $res = &topMatches('architecture computer x86');
#my $res = &topMatches('software testing feasible products research strategy combinatorial');
#my $res = &topMatches('speaking numbers chair experience consulting GDRG citations evaluation game dev');


#print $res."\n";

1;
