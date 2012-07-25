#!/usr/bin/env rspec
require 'spec_helper'

describe "the parseyaml function" do
  before :all do
    Puppet::Parser::Functions.autoloader.loadall
  end

  before :each do
    @scope = Puppet::Parser::Scope.new
  end

  it "should exist" do
    Puppet::Parser::Functions.function("parseyaml").should == "function_parseyaml"
  end

  it "should raise a ParseError if there is less than 1 arguments" do
    lambda { @scope.function_parseyaml([]) }.should( raise_error(Puppet::ParseError))
  end

  it "should convert YAML to a data structure" do
    yaml = <<-EOS
- aaa
- bbb
- ccc
EOS
    result = @scope.function_parseyaml([yaml])
    result.should(eq(['aaa','bbb','ccc']))
  end

end
