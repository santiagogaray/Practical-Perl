#!/usr/local/bin/perl -w

print "Content-type: text/html\n\n";
print <<HTML_START;
<HTML>
<BODY>
<H1>CGI Enviroment Variables</H1>
<TABLE BORDER=1>
HTML_START
while (($key,$value) = each %ENV) {
	print "<TR><TD><B>$key</B></TD><TD>$value</TD></TR>\n";
}
print <<HTML_END;
</TABLE>
</BODY>
</HTML>
HTML_END
