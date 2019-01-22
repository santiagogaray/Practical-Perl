#!/usr/bin/perl -w

# simple 'Hello World' response to GET HTML command.

print "Content-type: text/html\n\n";
print <<HELLOHTML;
<html>
<body>
<B>Hello World!</B>
</body>
</html>
HELLOHTML
