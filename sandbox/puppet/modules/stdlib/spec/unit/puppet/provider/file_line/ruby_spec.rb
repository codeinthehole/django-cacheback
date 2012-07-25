require 'puppet'
require 'tempfile'
provider_class = Puppet::Type.type(:file_line).provider(:ruby)
describe provider_class do
  context "add" do
    before :each do
      tmp = Tempfile.new('tmp')
      @tmpfile = tmp.path
      tmp.close!
      @resource = Puppet::Type::File_line.new(
        {:name => 'foo', :path => @tmpfile, :line => 'foo'}
      )
      @provider = provider_class.new(@resource)
    end
    it 'should detect if the line exists in the file' do
      File.open(@tmpfile, 'w') do |fh|
        fh.write('foo')
      end
      @provider.exists?.should be_true
    end
    it 'should detect if the line does not exist in the file' do
      File.open(@tmpfile, 'w') do |fh|
        fh.write('foo1')
      end
      @provider.exists?.should be_nil
    end
    it 'should append to an existing file when creating' do
      @provider.create
      File.read(@tmpfile).chomp.should == 'foo'
    end
  end

  context "remove" do
    before :each do
      tmp = Tempfile.new('tmp')
      @tmpfile = tmp.path
      tmp.close!
      @resource = Puppet::Type::File_line.new(
        {:name => 'foo', :path => @tmpfile, :line => 'foo', :ensure => 'absent' }
      )
      @provider = provider_class.new(@resource)
    end
    it 'should remove the line if it exists' do
      File.open(@tmpfile, 'w') do |fh|
        fh.write("foo1\nfoo\nfoo2")
      end
      @provider.destroy
      File.read(@tmpfile).should eql("foo1\nfoo2")
    end

    it 'should remove the line without touching the last new line' do
      File.open(@tmpfile, 'w') do |fh|
        fh.write("foo1\nfoo\nfoo2\n")
      end
      @provider.destroy
      File.read(@tmpfile).should eql("foo1\nfoo2\n")
    end

    it 'should remove any occurence of the line' do
      File.open(@tmpfile, 'w') do |fh|
        fh.write("foo1\nfoo\nfoo2\nfoo\nfoo")
      end
      @provider.destroy
      File.read(@tmpfile).should eql("foo1\nfoo2\n")
    end
  end
end
