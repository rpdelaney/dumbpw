dumbpw
======================
|LANGUAGE| |VERSION| |LICENSE| |MAINTAINED| |CIRCLECI| |MAINTAINABILITY|
|STYLE|

.. |CIRCLECI| image:: https://img.shields.io/circleci/build/gh/rpdelaney/dumbpw
   :target: https://circleci.com/gh/rpdelaney/dumbpw/tree/master
.. |LICENSE| image:: https://img.shields.io/badge/license-Apache%202.0-informational
   :target: https://www.apache.org/licenses/LICENSE-2.0.txt
.. |MAINTAINED| image:: https://img.shields.io/maintenance/yes/2021?logoColor=informational
.. |VERSION| image:: https://img.shields.io/pypi/v/dumbpw
   :target: https://pypi.org/project/dumbpw
.. |STYLE| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
.. |LANGUAGE| image:: https://img.shields.io/pypi/pyversions/dumbpw
.. |MAINTAINABILITY| image:: https://img.shields.io/codeclimate/maintainability-percentage/rpdelaney/dumbpw
   :target: https://codeclimate.com/github/rpdelaney/dumbpw

To create and remember passwords for online services, the best practice is to
use a password management tool such as `Bitwarden <https://bitwarden.com/>`_ to
generate long, cryptographically random passwords. Then, a very strong
passphrase is used to lock the password manager.

Unfortunately, in a misguided attempt to encourage users to choose better
passwords, many websites and apps have `very bad password policies <https://kottke.org/12/06/the-worlds-worst-password-requirements-list>`_
that place restrictions on what sorts of characters must be (or may not be) in
a password. These policies inhibit users from using cryptographically random
password generators. In fact, a long, high-entropy password is more likely to
violate such rules, which means a security-savvy user may have to attempt
several "random" passwords before one is accepted.

Enter dumbpw. dumbpw allows you to configure a set of rules, and then it will
generate a cryptographically secure password that conforms to those dumb rules.

Installation
------------

.. code-block :: console

    pip3 install dumbpw

Usage
-----

.. code-block :: console

    $ dumbpw -h
    Not implemented.

dumbpw can be imported into your application. However, you should understand
the implications of using it to create secrets in bulk, as the entropy on your
system may be exhausted rapidly.  dumbpw uses `secrets <https://docs.python.org/3/library/secrets.html>`_
to generate passwords.

============
Development
============

To install development dependencies, you will need `poetry <https://docs.pipenv.org/en/latest/>`_
and `pre-commit <https://pre-commit.com/>`_.

.. code-block :: console

    pre-commit install --install-hooks
    poetry install

`direnv <https://direnv.net/>`_ is optional, but recommended for convenience.
