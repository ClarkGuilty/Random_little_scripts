#!/usr/bin/perl

#print "Usage: format_sexcat.pl sextractor.cat *.param prefix\n";

if (@ARGV<2) {
        print "Usage: format_sexcat.pl sextractor.cat prefix\n";
        exit;
}

if( $ARGV[0] ne "STDIN" )
{
	open $in, "$ARGV[0]" or die "ERROR opening $ARGV[0]\n";
}
else
{
	$in = *STDIN;
}
@file=<$in>;
close $in;

$prefix=$ARGV[1];
$flag=0;
open(formatcat,">$ARGV[0]");
$nb=0;
foreach(@file)
{
    chomp();
    @line=split();
#    print "$line[0]\n";
    if(substr($line[0],0,1) eq "#")
    {
	if($line[1]!=($nb+1))
	{
	    for($k=2;$k<=($line[1]-$nb);$k++)
	    {
		push (@tableau, "${prefix}_${name}$k");
#		print "$line[1]!=$nb+1 ${name}$k\n";
	    }
	}
	#	else
	#	{
	$name=$line[2];
	$nb=$line[1];
	push (@tableau, "${prefix}_$name");
	print formatcat "$_\n";
	#	}
    }
    else
    {
	if($flag==0)
	{
	    print formatcat "# ";
	    foreach(@tableau)
	    {
		$_=$_."1" if($_=~/APER/ && $_!~/APER\d+/);
		$_=$_."1" if($_=~/RADIUS/ && $_!~/RADIUS\d+/);
#		print ".$_.\n";
		print formatcat "$_ ";
	    }
	    $flag=1;
	    print formatcat "\n";
	}
	print formatcat "$_\n";
    }
}


print "Done!\n";
