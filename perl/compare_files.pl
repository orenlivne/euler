#!/usr/bin/perl -w
#-----------------------------------------------------
# Given two files with the same number of lines
# and the same format: SNP  a[1] ... a[m] ,
# print the number of differences in the corresponding
# a-vectors in every line.
#------------------------------------------------------
use strict;

open(FILE1, $ARGV[0]) or die;
open(FILE2, $ARGV[1]) or die;

while (defined(my $line1 = <FILE1>) and defined(my $line2 = <FILE2>)) {
    chomp $line1;
    chomp $line2;
    my @a = split(/ /, $line1);
    my @b = split(/ /, $line2);
    my $num_differences = 0;
    for (my $i = 1; $i <= $#a; $i++) {
	$num_differences += int($a[$i] eq $b[$i]);
    }
    printf "%d\n", $num_differences;
}

close(FILE1);
close(FILE2);
