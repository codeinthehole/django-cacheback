#!/usr/bin/env rspec
require 'spec_helper'

describe "the is_integer function" do
  before :all do
    Puppet::Parser::Functions.autoloader.loadall
  end

  before :each do
    @scope = Puppet::Parser::Scope.new
  end

  it "should exist" do
    Puppet::Parser::Functions.function("is_integer").should == "function_is_integer"
  end

  it "should raise a ParseError if there is less than 1 arguments" do
    lambda { @scope.function_is_integer([]) }.should( raise_error(Puppet::ParseError))
  end

  it "should return true if an integer" do
    result = @scope.function_is_integer(["3"])
    result.should(eq(true))
  end

  it "should return false if a float" do
    result = @scope.function_is_integer(["3.2"])
    result.should(eq(false))
  end

  it "should return false if a string" do
    result = @scope.function_is_integer(["asdf"])
    result.should(eq(false))
  end

end
