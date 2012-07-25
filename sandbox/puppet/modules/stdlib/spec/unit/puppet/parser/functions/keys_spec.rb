#!/usr/bin/env rspec
require 'spec_helper'

describe "the keys function" do
  before :all do
    Puppet::Parser::Functions.autoloader.loadall
  end

  let(:scope) { Puppet::Parser::Scope.new }

  it "should exist" do
    Puppet::Parser::Functions.function("keys").should == "function_keys"
  end

  it "should raise a ParseError if there is less than 1 arguments" do
    lambda { scope.function_keys([]) }.should( raise_error(Puppet::ParseError))
  end

  it "should return an array of keys when given a hash" do
    result = scope.function_keys([{'a'=>1, 'b'=>2}])
    # =~ performs 'array with same elements' (set) matching
    # For more info see RSpec::Matchers::MatchArray
    result.should =~ ['a','b']
  end
end
