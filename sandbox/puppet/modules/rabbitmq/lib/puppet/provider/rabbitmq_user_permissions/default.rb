Puppet::Type.type(:rabbitmq_user_permissions).provide(:default) do

  def create
    default_fail
  end

  def destroy
    default_fail
  end

  def exists?
    default_fail
  end

  def default_fail
    fail('This is just the default provider for rabbitmq_user, all it does is fail')
  end
end
