#!/usr/bin/env rspec
require 'spec_helper'

describe "the upcase function" do
  before :all do
    Puppet::Parser::Functions.autoloader.loadall
  end

  before :each do
    @scope = Puppet::Parser::Scope.new
  end

  it "should exist" do
    Puppet::Parser::Functions.function("upcase").should == "function_upcase"
  end

  it "should raise a ParseError if there is less than 1 arguments" do
    lambda { @scope.function_upcase([]) }.should( raise_error(Puppet::ParseError))
  end

  it "should upcase a string" do
    result = @scope.function_upcase(["abc"])
    result.should(eq('ABC'))
  end

  it "should do nothing if a string is already upcase" do
    result = @scope.function_upcase(["ABC"])
    result.should(eq('ABC'))
  end

end
