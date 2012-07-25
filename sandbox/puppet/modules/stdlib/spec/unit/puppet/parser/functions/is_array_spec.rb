#!/usr/bin/env rspec
require 'spec_helper'

describe "the is_array function" do
  before :all do
    Puppet::Parser::Functions.autoloader.loadall
  end

  before :each do
    @scope = Puppet::Parser::Scope.new
  end

  it "should exist" do
    Puppet::Parser::Functions.function("is_array").should == "function_is_array"
  end

  it "should raise a ParseError if there is less than 1 arguments" do
    lambda { @scope.function_is_array([]) }.should( raise_error(Puppet::ParseError))
  end

  it "should return true if passed an array" do
    result = @scope.function_is_array([[1,2,3]])
    result.should(eq(true))
  end

  it "should return false if passed a hash" do
    result = @scope.function_is_array([{'a'=>1}])
    result.should(eq(false))
  end

  it "should return false if passed a string" do
    result = @scope.function_is_array(["asdf"])
    result.should(eq(false))
  end

end
