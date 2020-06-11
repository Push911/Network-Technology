use HTTP::Daemon;
use HTTP::Status;  

my $daemon = HTTP::Daemon->new(
        LocalAddr => 'localhost',
        LocalPort => 5000,
        Reuse => 1,
    ) || die;

print "Server running at: ", $daemon->url, "\n";

while (my $connection = $daemon->accept) 
{
	while (my $request = $connection->get_request) 
	{
		if ($request->method eq 'GET') 
		{
			my $uri = $request->uri;
			print "GET ", $uri, "\n";

			if ($uri eq "/") 
			{
				$uri = "/index.html";
			}

			my $requested_file = "page" . $uri;

			if(-e $requested_file) 
			{
				$connection->send_file_response($requested_file);
			} 
			else 
			{
				$connection->send_error(RC_NOT_FOUND);
			}
		}
		else 
		{
			$connection->send_error(RC_FORBIDDEN)
		}
	}
}


