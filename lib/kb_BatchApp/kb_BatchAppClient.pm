package kb_BatchApp::kb_BatchAppClient;

use JSON::RPC::Client;
use POSIX;
use strict;
use Data::Dumper;
use URI;
use Bio::KBase::Exceptions;
my $get_time = sub { time, 0 };
eval {
    require Time::HiRes;
    $get_time = sub { Time::HiRes::gettimeofday() };
};

use Bio::KBase::AuthToken;

# Client version should match Impl version
# This is a Semantic Version number,
# http://semver.org
our $VERSION = "0.1.0";

=head1 NAME

kb_BatchApp::kb_BatchAppClient

=head1 DESCRIPTION


kb_BatchApp
-----------
This contains tools for running batch jobs.
In this first pass, a "batch" is defined as multiple parallel runs of a single job. Each job's inputs and outputs should
be treated as independent of each other. An example might be a parameter sweep for a single app, or importing a list of
files using the same parameters, just being run multiple times.


=cut

sub new
{
    my($class, $url, @args) = @_;
    

    my $self = {
	client => kb_BatchApp::kb_BatchAppClient::RpcClient->new,
	url => $url,
	headers => [],
    };

    chomp($self->{hostname} = `hostname`);
    $self->{hostname} ||= 'unknown-host';

    #
    # Set up for propagating KBRPC_TAG and KBRPC_METADATA environment variables through
    # to invoked services. If these values are not set, we create a new tag
    # and a metadata field with basic information about the invoking script.
    #
    if ($ENV{KBRPC_TAG})
    {
	$self->{kbrpc_tag} = $ENV{KBRPC_TAG};
    }
    else
    {
	my ($t, $us) = &$get_time();
	$us = sprintf("%06d", $us);
	my $ts = strftime("%Y-%m-%dT%H:%M:%S.${us}Z", gmtime $t);
	$self->{kbrpc_tag} = "C:$0:$self->{hostname}:$$:$ts";
    }
    push(@{$self->{headers}}, 'Kbrpc-Tag', $self->{kbrpc_tag});

    if ($ENV{KBRPC_METADATA})
    {
	$self->{kbrpc_metadata} = $ENV{KBRPC_METADATA};
	push(@{$self->{headers}}, 'Kbrpc-Metadata', $self->{kbrpc_metadata});
    }

    if ($ENV{KBRPC_ERROR_DEST})
    {
	$self->{kbrpc_error_dest} = $ENV{KBRPC_ERROR_DEST};
	push(@{$self->{headers}}, 'Kbrpc-Errordest', $self->{kbrpc_error_dest});
    }

    #
    # This module requires authentication.
    #
    # We create an auth token, passing through the arguments that we were (hopefully) given.

    {
	my %arg_hash2 = @args;
	if (exists $arg_hash2{"token"}) {
	    $self->{token} = $arg_hash2{"token"};
	} elsif (exists $arg_hash2{"user_id"}) {
	    my $token = Bio::KBase::AuthToken->new(@args);
	    if (!$token->error_message) {
	        $self->{token} = $token->token;
	    }
	}
	
	if (exists $self->{token})
	{
	    $self->{client}->{token} = $self->{token};
	}
    }

    my $ua = $self->{client}->ua;	 
    my $timeout = $ENV{CDMI_TIMEOUT} || (30 * 60);	 
    $ua->timeout($timeout);
    bless $self, $class;
    #    $self->_validate_version();
    return $self;
}




=head2 run_batch

  $returnVal = $obj->run_batch($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_BatchApp.BatchInput
$returnVal is a kb_BatchApp.BatchResult
BatchInput is a reference to a hash where the following keys are defined:
	module_name has a value which is a string
	method_name has a value which is a string
	service_ver has a value which is a string
	wsid has a value which is a string
	meta has a value which is a kb_BatchApp.MetaInput
	batch_params has a value which is a reference to a list where each element is a kb_BatchApp.ParamsInput
MetaInput is a reference to a hash where the following keys are defined:
	cell_id has a value which is a string
	run_id has a value which is a string
	tag has a value which is a string
ParamsInput is a reference to a hash where the following keys are defined:
	params has a value which is a reference to a list where each element is an UnspecifiedObject, which can hold any non-null object
	source_ws_objects has a value which is a reference to a list where each element is a kb_BatchApp.obj_ref
obj_ref is a string
BatchResult is a reference to a hash where the following keys are defined:
	batch_result has a value which is a reference to a hash where the key is a string and the value is an UnspecifiedObject, which can hold any non-null object
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a kb_BatchApp.BatchInput
$returnVal is a kb_BatchApp.BatchResult
BatchInput is a reference to a hash where the following keys are defined:
	module_name has a value which is a string
	method_name has a value which is a string
	service_ver has a value which is a string
	wsid has a value which is a string
	meta has a value which is a kb_BatchApp.MetaInput
	batch_params has a value which is a reference to a list where each element is a kb_BatchApp.ParamsInput
MetaInput is a reference to a hash where the following keys are defined:
	cell_id has a value which is a string
	run_id has a value which is a string
	tag has a value which is a string
ParamsInput is a reference to a hash where the following keys are defined:
	params has a value which is a reference to a list where each element is an UnspecifiedObject, which can hold any non-null object
	source_ws_objects has a value which is a reference to a list where each element is a kb_BatchApp.obj_ref
obj_ref is a string
BatchResult is a reference to a hash where the following keys are defined:
	batch_result has a value which is a reference to a hash where the key is a string and the value is an UnspecifiedObject, which can hold any non-null object
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description

Runs a batch of the same app with a number of different input parameters.

=back

=cut

 sub run_batch
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function run_batch (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to run_batch:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'run_batch');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_BatchApp.run_batch",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'run_batch',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method run_batch",
					    status_line => $self->{client}->status_line,
					    method_name => 'run_batch',
				       );
    }
}
 
  
sub status
{
    my($self, @args) = @_;
    if ((my $n = @args) != 0) {
        Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
                                   "Invalid argument count for function status (received $n, expecting 0)");
    }
    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
        method => "kb_BatchApp.status",
        params => \@args,
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
                           code => $result->content->{error}->{code},
                           method_name => 'status',
                           data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
                          );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method status",
                        status_line => $self->{client}->status_line,
                        method_name => 'status',
                       );
    }
}
   

sub version {
    my ($self) = @_;
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "kb_BatchApp.version",
        params => [],
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(
                error => $result->error_message,
                code => $result->content->{code},
                method_name => 'run_batch',
            );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(
            error => "Error invoking method run_batch",
            status_line => $self->{client}->status_line,
            method_name => 'run_batch',
        );
    }
}

sub _validate_version {
    my ($self) = @_;
    my $svr_version = $self->version();
    my $client_version = $VERSION;
    my ($cMajor, $cMinor) = split(/\./, $client_version);
    my ($sMajor, $sMinor) = split(/\./, $svr_version);
    if ($sMajor != $cMajor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Major version numbers differ.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor < $cMinor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Client minor version greater than Server minor version.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor > $cMinor) {
        warn "New client version available for kb_BatchApp::kb_BatchAppClient\n";
    }
    if ($sMajor == 0) {
        warn "kb_BatchApp::kb_BatchAppClient version is $svr_version. API subject to change.\n";
    }
}

=head1 TYPES



=head2 obj_ref

=over 4



=item Description

An UPA for a single object.


=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 MetaInput

=over 4



=item Description

Describes the metadata for a single batch run. Passed along to the Narrative Job Service on each child
job started.
----------
cell_id - the unique id for the Narrative cell that starts the batch.
run_id - the unique id assigned to the run from the Narrative.
tag - the version tag (one of "release", "beta" or "dev") for the app being run in batch.


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
cell_id has a value which is a string
run_id has a value which is a string
tag has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
cell_id has a value which is a string
run_id has a value which is a string
tag has a value which is a string


=end text

=back



=head2 ParamsInput

=over 4



=item Description

Describes the parameters for a single run in a batch. This contains both the set of parameters
for a given run, along with the list of object UPAs to be used in setting provenance.
----------
params - an arbitrary list of inputs for the job run.
source_ws_objects - the list of UPAs used as inputs to this job. These should be reflected somewhere in params.


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
params has a value which is a reference to a list where each element is an UnspecifiedObject, which can hold any non-null object
source_ws_objects has a value which is a reference to a list where each element is a kb_BatchApp.obj_ref

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
params has a value which is a reference to a list where each element is an UnspecifiedObject, which can hold any non-null object
source_ws_objects has a value which is a reference to a list where each element is a kb_BatchApp.obj_ref


=end text

=back



=head2 BatchInput

=over 4



=item Description

The inputs for a batch run on a single app.
----------
module_name - the name of the module to run. In an app like "MEGAHIT.run_megahit", this would be "MEGAHIT"
method_name - the name of the method to run in the module. In the above, this would be "run_megahit"
service_ver - the version of the app to run (or a github hash)
wsid - the id of the workspace to associate with the job for sharing purposes
meta - the job metadata
batch_params - the list of input parameters for the app.


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
module_name has a value which is a string
method_name has a value which is a string
service_ver has a value which is a string
wsid has a value which is a string
meta has a value which is a kb_BatchApp.MetaInput
batch_params has a value which is a reference to a list where each element is a kb_BatchApp.ParamsInput

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
module_name has a value which is a string
method_name has a value which is a string
service_ver has a value which is a string
wsid has a value which is a string
meta has a value which is a kb_BatchApp.MetaInput
batch_params has a value which is a reference to a list where each element is a kb_BatchApp.ParamsInput


=end text

=back



=head2 BatchResult

=over 4



=item Description

The results of a batch run.
--------
batch_result - a mapping from a string (child job id) to the result for that child job
report_name - the name of the report for the entire batch run
report_ref - the UPA of the report for the entire batch run


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
batch_result has a value which is a reference to a hash where the key is a string and the value is an UnspecifiedObject, which can hold any non-null object
report_name has a value which is a string
report_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
batch_result has a value which is a reference to a hash where the key is a string and the value is an UnspecifiedObject, which can hold any non-null object
report_name has a value which is a string
report_ref has a value which is a string


=end text

=back



=cut

package kb_BatchApp::kb_BatchAppClient::RpcClient;
use base 'JSON::RPC::Client';
use POSIX;
use strict;

#
# Override JSON::RPC::Client::call because it doesn't handle error returns properly.
#

sub call {
    my ($self, $uri, $headers, $obj) = @_;
    my $result;


    {
	if ($uri =~ /\?/) {
	    $result = $self->_get($uri);
	}
	else {
	    Carp::croak "not hashref." unless (ref $obj eq 'HASH');
	    $result = $self->_post($uri, $headers, $obj);
	}

    }

    my $service = $obj->{method} =~ /^system\./ if ( $obj );

    $self->status_line($result->status_line);

    if ($result->is_success) {

        return unless($result->content); # notification?

        if ($service) {
            return JSON::RPC::ServiceObject->new($result, $self->json);
        }

        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    elsif ($result->content_type eq 'application/json')
    {
        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    else {
        return;
    }
}


sub _post {
    my ($self, $uri, $headers, $obj) = @_;
    my $json = $self->json;

    $obj->{version} ||= $self->{version} || '1.1';

    if ($obj->{version} eq '1.0') {
        delete $obj->{version};
        if (exists $obj->{id}) {
            $self->id($obj->{id}) if ($obj->{id}); # if undef, it is notification.
        }
        else {
            $obj->{id} = $self->id || ($self->id('JSON::RPC::Client'));
        }
    }
    else {
        # $obj->{id} = $self->id if (defined $self->id);
	# Assign a random number to the id if one hasn't been set
	$obj->{id} = (defined $self->id) ? $self->id : substr(rand(),2);
    }

    my $content = $json->encode($obj);

    $self->ua->post(
        $uri,
        Content_Type   => $self->{content_type},
        Content        => $content,
        Accept         => 'application/json',
	@$headers,
	($self->{token} ? (Authorization => $self->{token}) : ()),
    );
}



1;
