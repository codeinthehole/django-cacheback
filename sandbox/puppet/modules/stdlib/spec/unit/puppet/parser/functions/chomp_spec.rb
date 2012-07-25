#!/usr/bin/env rspec
require 'spec_helper'

describe "the chomp function" do
  before :all do
    Puppet::Parser::Functions.autoloader.loadall
  end

  before :each do
    @scope = Puppet::Parser::Scope.new
  end

  it "should exist" do
    Puppet::Parser::Functions.function("chomp").should == "function_chomp"
  end

  it "should raise a ParseError if there is less than 1 arguments" do
    lambda { @scope.function_chomp([]) }.should( raise_error(Puppet::ParseError))
  end

  it "should chomp the end of a string" do
    result = @scope.function_chomp(["abc\n"])
    result.should(eq("abc"))
  end

end
