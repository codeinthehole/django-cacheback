Puppet::Type.type(:file_line).provide(:ruby) do

  def exists?
    lines.find do |line|
      line.chomp == resource[:line].chomp
    end
  end

  def create
    File.open(resource[:path], 'a') do |fh|
      fh.puts resource[:line]
    end
  end

  def destroy
    local_lines = lines
    File.open(resource[:path],'w') do |fh|
      fh.write(local_lines.reject{|l| l.chomp == resource[:line] }.join(''))
    end
  end

  private
  def lines
    @lines ||= File.readlines(resource[:path])
  end

end
