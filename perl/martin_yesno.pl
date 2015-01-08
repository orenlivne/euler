#!/usr/bin/perl -w
#---------------------------------------------------
#LEARNING PERL WITH EXERCISES-----------------------
#Look for nearest neighbor in an array--------------
#--------------------------------------------------

use strict;
use warnings;

#my @chain=(3,4,7,9,12,25,57);  #to check the integerarray

print "Please give in an array of numbers and press ctrl+d if you are ready\n";
my @chain=<STDIN>;
print "You are doing great!!!\n";
print "That is your array:\n	@chain\n\n";

print "Please give in now a number and press return\n";
my $lookat=<STDIN>;
chomp $lookat;
print "Your number is $lookat isn't it?\n";
print "press Y for yes and N for no?";

while (<STDIN> !~ /Y/ ) {
    print "please press Y or N";
}
print "ok I look for the nearest number of $lookat now\n";
print "Yippie, I have an idea, even if I am not sure...,\n but grmmbl grrmbl\n";

my $solution;
my $difference=10000000000; #Doesn't want INF using Strict

foreach my $neighbor(@chain) {
				if (abs($lookat-$neighbor)<$difference) 
								{$solution=$neighbor;
								$difference=abs($lookat-$neighbor);
								print $solution;
								print $difference;
								}
				}
print "...grrrmbl\n...Solution could be: $solution if we use this array:\n @chain and your number $lookat\n";
print "Time for a happy break now???\n";
print "Where do I need the pointer??\n";
