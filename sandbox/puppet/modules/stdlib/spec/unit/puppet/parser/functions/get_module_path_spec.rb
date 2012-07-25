#!/usr/bin/env rspec
require 'puppet'
require 'fileutils'
require 'spec_helper'
describe Puppet::Parser::Functions.function(:get_module_path) do
  include PuppetSpec::Files

  def get_scope(environment = 'production')
    scope = Puppet::Parser::Scope.new
    scope.compiler = Puppet::Parser::Compiler.new(Puppet::Node.new("floppy", :environment => environment))
    scope
  end
  it 'should only allow one argument' do
    expect { get_scope.function_get_module_path([]) }.should raise_error(Puppet::ParseError, /Wrong number of arguments, expects one/)
    expect { get_scope.function_get_module_path(['1','2','3']) }.should raise_error(Puppet::ParseError, /Wrong number of arguments, expects one/)
  end
  it 'should raise an exception when the module cannot be found' do
    expect { get_scope.function_get_module_path(['foo']) }.should raise_error(Puppet::ParseError, /Could not find module/)
  end
  describe 'when locating a module' do
    let(:modulepath) { tmpdir('modulepath') }
    let(:foo_path) { File.join(modulepath, 'foo') }
    before(:each) { FileUtils.mkdir(foo_path) }
    it 'should be able to find module paths from the modulepath setting' do
      Puppet[:modulepath] = modulepath
      get_scope.function_get_module_path(['foo']).should == foo_path
    end
    it 'should be able to find module paths when the modulepath is a list' do
      Puppet[:modulepath] = modulepath + ":/tmp"
      get_scope.function_get_module_path(['foo']).should == foo_path
    end
    it 'should be able to find module paths from the environment' do
      conf_file = tmpfile('conffile')
      File.open(conf_file, 'w') do |fh|
        fh.write("[dansenvironment]\nmodulepath = #{modulepath}")
      end
      Puppet[:config] = conf_file
      Puppet.parse_config
      get_scope('dansenvironment').function_get_module_path(['foo']).should ==foo_path
    end
  end
end
