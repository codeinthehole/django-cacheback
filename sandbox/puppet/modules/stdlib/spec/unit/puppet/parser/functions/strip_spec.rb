#!/usr/bin/env rspec
require 'spec_helper'

describe "the strip function" do
  before :all do
    Puppet::Parser::Functions.autoloader.loadall
  end

  before :each do
    @scope = Puppet::Parser::Scope.new
  end

  it "should exist" do
    Puppet::Parser::Functions.function("strip").should == "function_strip"
  end

  it "should raise a ParseError if there is less than 1 arguments" do
    lambda { @scope.function_strip([]) }.should( raise_error(Puppet::ParseError))
  end

  it "should strip a string" do
    result = @scope.function_strip([" ab cd "])
    result.should(eq('ab cd'))
  end

end
