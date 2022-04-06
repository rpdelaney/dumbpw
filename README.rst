dumbpw
======================
|LANGUAGE| |VERSION| |LICENSE| |MAINTAINED| |CIRCLECI| |MAINTAINABILITY|
|STYLE|

.. |CIRCLECI| image:: https://img.shields.io/circleci/build/gh/rpdelaney/dumbpw
   :target: https://circleci.com/gh/rpdelaney/dumbpw/tree/main
.. |LICENSE| image:: https://img.shields.io/badge/license-Apache%202.0-informational
   :target: https://www.apache.org/licenses/LICENSE-2.0.txt
.. |MAINTAINED| image:: https://img.shields.io/maintenance/yes/2022?logoColor=informational
.. |VERSION| image:: https://img.shields.io/pypi/v/dumbpw
   :target: https://pypi.org/project/dumbpw
.. |STYLE| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
.. |LANGUAGE| image:: https://img.shields.io/pypi/pyversions/dumbpw
.. |MAINTAINABILITY| image:: https://img.shields.io/codeclimate/maintainability-percentage/rpdelaney/dumbpw
   :target: https://codeclimate.com/github/rpdelaney/dumbpw

To create and remember passwords for online services, the best practice for
most folks online is to use a password management tool such as `Bitwarden
<https://bitwarden.com/>`_ to generate long, cryptographically random
passwords. Then, a very strong passphrase is used to lock the password manager.

Unfortunately, in a misguided attempt to encourage users to choose better
passwords, many websites and apps enforce `restrictive password policies <https://kottke.org/12/06/the-worlds-worst-password-requirements-list>`_
that place restrictions on what sorts of characters must be (or may not be) in
a password. These policies inhibit users from using cryptographically random
password generators: a long, high-entropy password is more likely to
violate such rules, which means a security-savvy user may have to attempt
several "random" passwords before one is accepted. This punishes users
who are trying to follow best practices.

Enter dumbpw. dumbpw allows you to configure a set of rules, and then it will
generate a cryptographically secure password that conforms to those dumb rules.

If all you need is a password generator, **you should not use this**.

Installation
------------

.. code-block :: console

    pip3 install dumbpw

Usage
-----

.. code-block :: console

    $ dumbpw --help
    Usage: dumbpw [OPTIONS] LENGTH

    Options:
      --version                       Show the version and exit.
      --min-uppercase INTEGER         The minimum number of uppercase characters.
      --min-lowercase INTEGER         The minimum number of lowercase characters.
      --min-digits INTEGER            The minimum number of digit characters.
      --min-specials INTEGER          The minimum number of special characters.
      --blocklist TEXT                Characters that may not be in the password.
                                      [default: '";]
      --allow-repeating / --reject-repeating
                                      Allow or reject repeating characters in the
                                      password.  [default: reject-repeating]
      --help                          Show this message and exit.

Known issues
------------
* dumbpw uses `secrets <https://docs.python.org/3/library/secrets.html>`_
  to generate passwords. If the generated string doesn't meet the given
  requirements, dumbpw discards it and generates another, until one passes.
  Therefore, if you ask dumbpw to generate a long password with high minimums,
  it will run for a very long time before terminating.
* Likewise, if your minimums require characters that are banned in the
  blocklist option, dumbpw will run forever.
* The author is neither a cryptographer, nor a security expert. There has
  been no formal, independent, external security review of this software. As
  explained in the LICENSE, the author assumes no responsibility or liability
  for your use of this software.

============
Development
============

To install development dependencies, you will need `poetry <https://docs.pipenv.org/en/latest/>`_
and `pre-commit <https://pre-commit.com/>`_.

.. code-block :: console

    pre-commit install --install-hooks
    poetry install && poetry shell

`direnv <https://direnv.net/>`_ is optional, but recommended for convenience.
