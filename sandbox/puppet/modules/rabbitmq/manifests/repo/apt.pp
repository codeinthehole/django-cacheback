# sets up the vmware hosted apt repo
# requires
#   puppetlabs-apt
class rabbitmq::repo::apt(
  $pin = undef
) {

  Class['rabbitmq::repo::apt'] -> Package<| title == 'rabbitmq-server' |>

  apt::source { 'rabbitmq':
    location    => 'http://www.rabbitmq.com/debian/',
    release     => 'testing',
    repos       => 'main',
    include_src => false,
    key         => 'RabbitMQ Release Signing Key <info@rabbitmq.com>',
    key_content => template('rabbitmq/rabbit.pub.key'),
    pin         => $pin,
  }

  if ! ($pin == undef) {
    validate_re($pin, '\d\d\d')
    apt::pin { 'rabbitmq':
      packages => 'rabbitmq-server',
      priority => $pin,
    }
  }
}
