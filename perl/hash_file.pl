#!/usr/bin/env perl
#------------------------------------------------------
# Example program for Martin Depner.
# Determine how many times each line occurs in a file
# using a hash table. Prints line occurrences, sorted
# lexicographically.
#------------------------------------------------------

my $file_name = "martin.in";
my $str = "Martin";

my %hash = ();
open(MYINPUTFILE, "<$file_name");
while (<MYINPUTFILE>)
 {
     my($line) = $_;
     chomp($line);
#     print "$line\n";

     if (not exists $hash{$line})
     {
	 # Newly-encountered line
	 $hash{$line} = 1;
     } else {
	 # Line is already in hash
	 $hash{$line} = $hash{$line} + 1;
     }
 }

# Print results
for my $key ( sort keys %hash ) {
    printf "%-12s: %d\n", $key, $hash{$key};
}
