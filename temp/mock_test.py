from mock import Mock

from boto.cloudformation import CloudFormationConnection

# There are three things of interest in this gist:
# 1) Example helper function showing how to mock out boto's connection objects
# 2) Example hardcoded AWS API return
# 3) Example use of 1 and 2 in a unit test

def make_cloudformation_cnx(payload_return_value="", status_code=200):
    """
    Unit test helper. Pass in payload and return value. Mocks out the return
    of the AWS API Call.

    Args:
      payloadd_return_value (str): AWS API Response
      status_code (int): HTTP Status code

    Returns:
      boto.cloudformation.CloudFormationConnection: Connection ready to be used.
    """
    cnx = CloudFormationConnection()
    cnx.make_request = Mock()
    response = Mock()
    response.read.return_value = payload_return_value
    response.status = status_code
    cnx.make_request.return_value = response
    return cnx

## PAYLOAD
EXAMPLE_PAYLOAD=\
"""
<DescribeStacksResult>
  <Stacks>
    <member>
      <StackName>MyStack</StackName>
      <StackId>arn:aws:cloudformation:us-east-1:123456789:stack/MyStack/aaf549a0-a413-11df-adb3-5081b3858e83</StackId>
      <CreationTime>2010-07-27T22:28:28Z</CreationTime>
      <StackStatus>CREATE_COMPLETE</StackStatus>
      <DisableRollback>false</DisableRollback>
      <Outputs>
        <member>
          <OutputKey>StartPage</OutputKey>
          <OutputValue>http://my-load-balancer.amazonaws.com:80/index.html</OutputValue>
        </member>
      </Outputs>
    </member>
  </Stacks>
</DescribeStacksResult>
"""

## EXAMPLE UNIT TEST
def test_boto_describe_stacks_one_stack(self):
	cnx = make_cloudformation_cnx(EXAMPLE_PAYLOAD)
	stacks = cnx.describe_stacks()
	assert len(stacks) == 1
	stack = stacks[0]
        # Ensure the object is well formed
	assert stack.stack_id == "arn:aws:cloudformation:us-east-1:123456789:stack/MyStack/aaf549a0-a413-11df-adb3-5081b3858e83"
	assert stack.stack_name == "MyStack"
        # And etc. ...