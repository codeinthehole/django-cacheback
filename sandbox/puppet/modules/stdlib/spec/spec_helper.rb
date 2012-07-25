dir = File.expand_path(File.dirname(__FILE__))
$LOAD_PATH.unshift File.join(dir, 'lib')

# Don't want puppet getting the command line arguments for rake or autotest
ARGV.clear

require 'puppet'
require 'facter'
require 'mocha'
gem 'rspec', '>=2.0.0'
require 'rspec/expectations'


# So everyone else doesn't have to include this base constant.
module PuppetSpec
  FIXTURE_DIR = File.join(dir = File.expand_path(File.dirname(__FILE__)), "fixtures") unless defined?(FIXTURE_DIR)
end

# TODO: ultimately would like to move these requires into the puppet_spec_helper.rb file, but the namespaces
#  are not currently the same between the two, so tests would need to be modified.  Not ready to undertake that
#  just yet.
require 'puppet_spec/files'

require 'puppet_spec_helper'


RSpec.configure do |config|

  config.before :each do
    GC.disable
  end

  config.after :each do
    GC.enable
  end
end
