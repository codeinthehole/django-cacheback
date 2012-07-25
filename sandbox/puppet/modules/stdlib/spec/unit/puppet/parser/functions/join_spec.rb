#!/usr/bin/env rspec
require 'spec_helper'

describe "the join function" do
  before :all do
    Puppet::Parser::Functions.autoloader.loadall
  end

  before :each do
    @scope = Puppet::Parser::Scope.new
  end

  it "should exist" do
    Puppet::Parser::Functions.function("join").should == "function_join"
  end

  it "should raise a ParseError if there is less than 1 arguments" do
    lambda { @scope.function_join([]) }.should( raise_error(Puppet::ParseError))
  end

  it "should join an array into a string" do
    result = @scope.function_join([["a","b","c"], ":"])
    result.should(eq("a:b:c"))
  end

end
