#!/usr/bin/env rspec
require 'spec_helper'

describe "the swapcase function" do
  before :all do
    Puppet::Parser::Functions.autoloader.loadall
  end

  before :each do
    @scope = Puppet::Parser::Scope.new
  end

  it "should exist" do
    Puppet::Parser::Functions.function("swapcase").should == "function_swapcase"
  end

  it "should raise a ParseError if there is less than 1 arguments" do
    lambda { @scope.function_swapcase([]) }.should( raise_error(Puppet::ParseError))
  end

  it "should swapcase a string" do
    result = @scope.function_swapcase(["aaBBccDD"])
    result.should(eq('AAbbCCdd'))
  end

end
