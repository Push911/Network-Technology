use HTTP::Daemon;
use HTTP::Status;  

my $daemon = HTTP::Daemon->new
	(
	LocalAddr => 'localhost',
	LocalPort => 5001,
	Reuse => 1,
	) || die;

print "Server running at: ", $daemon->url, "\n";

while (my $connection = $daemon->accept) 
{
	while (my $request = $connection->get_request) 
	{
		if ($request->method eq 'GET') 
		{
			print "GET ", $request->url, "\n";
			$file_s= "page/index.html";
			$connection->send_file_response($file_s);
		}
		else 
		{
			$connection->send_error(RC_FORBIDDEN)
		}
	}
	$connection->close;
	undef($connection);
}
