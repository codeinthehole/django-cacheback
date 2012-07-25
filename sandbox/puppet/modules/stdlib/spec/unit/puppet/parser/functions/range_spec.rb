#!/usr/bin/env rspec
require 'spec_helper'

describe "the range function" do
  before :all do
    Puppet::Parser::Functions.autoloader.loadall
  end

  let :scope do
    Puppet::Parser::Scope.new
  end

  it "should exist" do
    Puppet::Parser::Functions.function("range").should == "function_range"
  end

  it "should raise a ParseError if there is less than 1 arguments" do
    lambda { scope.function_range([]) }.should( raise_error(Puppet::ParseError))
  end

  it "should return a letter range" do
    result = scope.function_range(["a","d"])
    result.should(eq(['a','b','c','d']))
  end

  it "should return a number range" do
    result = scope.function_range(["1","4"])
    result.should(eq([1,2,3,4]))
  end

  it "should work with padded hostname like strings" do
    expected = ("host01".."host10").to_a
    scope.function_range(["host01","host10"]).should eq expected
  end

  it "should coerce zero padded digits to integers" do
    expected = (0..10).to_a
    scope.function_range(["00", "10"]).should eq expected
  end
end
