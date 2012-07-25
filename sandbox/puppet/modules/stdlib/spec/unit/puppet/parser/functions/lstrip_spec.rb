#!/usr/bin/env rspec
require 'spec_helper'

describe "the lstrip function" do
  before :all do
    Puppet::Parser::Functions.autoloader.loadall
  end

  before :each do
    @scope = Puppet::Parser::Scope.new
  end

  it "should exist" do
    Puppet::Parser::Functions.function("lstrip").should == "function_lstrip"
  end

  it "should raise a ParseError if there is less than 1 arguments" do
    lambda { @scope.function_lstrip([]) }.should( raise_error(Puppet::ParseError))
  end

  it "should lstrip a string" do
    result = @scope.function_lstrip(["  asdf"])
    result.should(eq('asdf'))
  end

end
