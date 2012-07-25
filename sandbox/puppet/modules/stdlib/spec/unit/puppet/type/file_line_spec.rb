require 'puppet'
require 'tempfile'
describe Puppet::Type.type(:file_line) do
  let :file_line do
    Puppet::Type.type(:file_line).new(:name => 'foo', :line => 'line', :path => '/tmp/path')
  end
  it 'should accept a line and path' do
    file_line[:line] = 'my_line'
    file_line[:line].should == 'my_line'
  end
  it 'should accept posix filenames' do
    file_line[:path] = '/tmp/path'
    file_line[:path].should == '/tmp/path'
  end
  it 'should not accept unqualified path' do
    expect { file_line[:path] = 'file' }.should raise_error(Puppet::Error, /File paths must be fully qualified/)
  end
  it 'should require that a line is specified' do
    expect { Puppet::Type.type(:file_line).new(:name => 'foo', :path => '/tmp/file') }.should raise_error(Puppet::Error, /Both line and path are required attributes/)
  end
  it 'should require that a file is specified' do
    expect { Puppet::Type.type(:file_line).new(:name => 'foo', :line => 'path') }.should raise_error(Puppet::Error, /Both line and path are required attributes/)
  end
  it 'should default to ensure => present' do
    file_line[:ensure].should eq :present
  end
end
