#!/usr/bin/env rspec
require 'spec_helper'

describe "the zip function" do
  before :all do
    Puppet::Parser::Functions.autoloader.loadall
  end

  before :each do
    @scope = Puppet::Parser::Scope.new
  end

  it "should exist" do
    Puppet::Parser::Functions.function("zip").should == "function_zip"
  end

  it "should raise a ParseError if there is less than 1 arguments" do
    lambda { @scope.function_zip([]) }.should( raise_error(Puppet::ParseError))
  end

  it "should be able to zip an array" do
    result = @scope.function_zip([['1','2','3'],['4','5','6']])
    result.should(eq([["1", "4"], ["2", "5"], ["3", "6"]]))
  end

end
