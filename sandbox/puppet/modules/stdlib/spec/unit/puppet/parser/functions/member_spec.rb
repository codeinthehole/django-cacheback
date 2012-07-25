#!/usr/bin/env rspec
require 'spec_helper'

describe "the member function" do
  before :all do
    Puppet::Parser::Functions.autoloader.loadall
  end

  before :each do
    @scope = Puppet::Parser::Scope.new
  end

  it "should exist" do
    Puppet::Parser::Functions.function("member").should == "function_member"
  end

  it "should raise a ParseError if there is less than 1 arguments" do
    lambda { @scope.function_member([]) }.should( raise_error(Puppet::ParseError))
  end

  it "should return true if a member is in an array" do
    result = @scope.function_member([["a","b","c"], "a"])
    result.should(eq(true))
  end  

  it "should return false if a member is not in an array" do
    result = @scope.function_member([["a","b","c"], "d"])
    result.should(eq(false))
  end  

end
