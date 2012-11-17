#!/usr/bin/perl
# This script drives the .cgi backend using text from the URL passed via the "upaddr" field 
# Chris Hokamp 
# Fall 2012

use strict;
use warnings; 
use jsonClient;
use whoknowsClient;

#use Encode;
use CGI '-utf8'; #TODO: ensure that this is necessary
use CGI::Carp 'fatalsToBrowser';

my $query = new CGI; 
my $time = time();

# read the url and from the Web interface
my $search = $query->param("search");
chomp($search);
my $res = &topMatches($search);


#TODO: get query and return JSON
#my $res = &topMatches('natural language processing lit lab computer science Rada Mihalcea');
#print "manager top matches: $res\n";

#$res =~ s/\(//g;
#$res =~ s/\)//g;
#$res =~ s/^\|\(//;
#$res =~ s/\)\|$//;
#my @tuples = split(' ', $res);
#my @ids = ();
#foreach my $tupl (@tuples) {
    #my @id = split(', ', $tupl);
    #push (@ids, $id[0]);
#}
#my $idlist = join(' ', @ids);

#print $res;
#print "$idlist\n";
#my $jsonResult = &getJson($idlist);
my $jsonResult = &getJson($res);


#the site may generate different HTML depending upon the browser



#TEST LOGGING - make sure web server perms are set correctly!
#open LOG, ">>", 'log.txt';
#print LOG "getUrl.pl was called...\n";
#close LOG;

#check if upfile is there - Note that we can only parse the file or the url, not
#both - check for parsable file type as well -
# UPDATE: do this in Javascript(client-side), not CGI

#TODO: set this in the javascript
#my $upfile = $query->param("upfile");


#TESTING - hard coded for now
my $testResult = '{ "Results" : [ { "email" : "proftest@gmail.com","name" : "Professor test","profilepic" : "http://demo.wuddupgames.com/Assets/Textures/negx.jpg","website" : "www.proftest.com"},{ "email" : "proftest@gmail.com","name" : "Professor test2","profilepic" : "http://demo.wuddupgames.com/Assets/Textures/negx.jpg", "website" : "www.proftest.com"} ] }'; 

sub outputPage {
	
    my $result = shift @_;
	#TODO: ensure that this is the proper way to make output UTF8-safe
	print $query->header(-charset => 'UTF-8');
        	
	print $result;
	
	#print CGI::escapeHTML($_[0]);
	#print '<span class="context" style="color: blue;">test test </span>'."\n";
	#print "-- content is finished --";

	#END_TEST
}

&outputPage($jsonResult);
