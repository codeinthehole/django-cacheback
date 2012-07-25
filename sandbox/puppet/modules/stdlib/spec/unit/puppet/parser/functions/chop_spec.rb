#!/usr/bin/env rspec
require 'spec_helper'

describe "the chop function" do
  before :all do
    Puppet::Parser::Functions.autoloader.loadall
  end

  before :each do
    @scope = Puppet::Parser::Scope.new
  end

  it "should exist" do
    Puppet::Parser::Functions.function("chop").should == "function_chop"
  end

  it "should raise a ParseError if there is less than 1 arguments" do
    lambda { @scope.function_chop([]) }.should( raise_error(Puppet::ParseError))
  end

  it "should chop the end of a string" do
    result = @scope.function_chop(["asdf\n"])
    result.should(eq("asdf"))
  end

end
