#!/usr/bin/env rspec
require 'spec_helper'

describe "the delete_at function" do
  before :all do
    Puppet::Parser::Functions.autoloader.loadall
  end

  before :each do
    @scope = Puppet::Parser::Scope.new
  end

  it "should exist" do
    Puppet::Parser::Functions.function("delete_at").should == "function_delete_at"
  end

  it "should raise a ParseError if there is less than 1 arguments" do
    lambda { @scope.function_delete_at([]) }.should( raise_error(Puppet::ParseError))
  end

  it "should delete an item at specified location from an array" do
    result = @scope.function_delete_at([['a','b','c'],1])
    result.should(eq(['a','c']))
  end

end
