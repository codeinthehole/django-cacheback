require 'puppet'

# We don't need this for the basic tests we're doing
# require 'spec_helper'

# Dan mentioned that Nick recommended the function method call
# to return the string value for the test description.
# this will not even try the test if the function cannot be
# loaded.
describe Puppet::Parser::Functions.function(:validate_string) do

  # Pulled from Dan's create_resources function
  def get_scope
    @topscope = Puppet::Parser::Scope.new
    # This is necessary so we don't try to use the compiler to discover our parent.
    @topscope.parent = nil
    @scope = Puppet::Parser::Scope.new
    @scope.compiler = Puppet::Parser::Compiler.new(Puppet::Node.new("floppy", :environment => 'production'))
    @scope.parent = @topscope
    @compiler = @scope.compiler
  end

  describe 'when calling validate_string from puppet' do

    %w{ foo bar baz }.each do |the_string|

      it "should compile when #{the_string} is a string" do
        Puppet[:code] = "validate_string('#{the_string}')"
        get_scope
        @scope.compiler.compile
      end

      it "should compile when #{the_string} is a bare word" do
        Puppet[:code] = "validate_string(#{the_string})"
        get_scope
        @scope.compiler.compile
      end

    end

    %w{ true false }.each do |the_string|
      it "should compile when #{the_string} is a string" do
        Puppet[:code] = "validate_string('#{the_string}')"
        get_scope
        @scope.compiler.compile
      end

      it "should not compile when #{the_string} is a bare word" do
        Puppet[:code] = "validate_string(#{the_string})"
        get_scope
        expect { @scope.compiler.compile }.should raise_error(Puppet::ParseError, /is not a string/)
      end
    end

    it "should compile when multiple string arguments are passed" do
      Puppet[:code] = <<-'ENDofPUPPETcode'
        $foo = ''
        $bar = 'two'
        validate_string($foo, $bar)
      ENDofPUPPETcode
      get_scope
      @scope.compiler.compile
    end

    it "should compile when an explicitly undef variable is passed (NOTE THIS MAY NOT BE DESIRABLE)" do
      Puppet[:code] = <<-'ENDofPUPPETcode'
        $foo = undef
        validate_string($foo)
      ENDofPUPPETcode
      get_scope
      @scope.compiler.compile
    end

    it "should compile when an undefined variable is passed (NOTE THIS MAY NOT BE DESIRABLE)" do
      Puppet[:code] = <<-'ENDofPUPPETcode'
        validate_string($foobarbazishouldnotexist)
      ENDofPUPPETcode
      get_scope
      @scope.compiler.compile
    end
  end
end

