#!/usr/bin/env rspec
require 'spec_helper'

describe "the delete function" do
  before :all do
    Puppet::Parser::Functions.autoloader.loadall
  end

  before :each do
    @scope = Puppet::Parser::Scope.new
  end

  it "should exist" do
    Puppet::Parser::Functions.function("delete").should == "function_delete"
  end

  it "should raise a ParseError if there is less than 1 arguments" do
    lambda { @scope.function_delete([]) }.should( raise_error(Puppet::ParseError))
  end

  it "should delete an item from an array" do
    result = @scope.function_delete([['a','b','c'],'b'])
    result.should(eq(['a','c']))
  end

end
