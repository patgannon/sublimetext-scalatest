Sublime Text Scala Test
=======================

Overview
--------

This plug-in for Sublime Text 2 enables you to:
  - Run scala unit tests (all tests in suite / single fixture)
  - Switch between code and test
  - Navigate quickly to scala files within project folder

This project was influenced by, and borrows some code from: https://github.com/maltize/sublime-text-2-ruby-tests

Installation
------------

Go to your Sublime Text 2 `Packages` directory

 - OS X: `~/Library/Application\ Support/Sublime\ Text\ 2/Packages`
 - Windows: `%APPDATA%/Sublime Text 2/Packages/`
 - Linux: `~/.Sublime\ Text\ 2/Packages/`

and clone the repository using the command below:

``` shell
git clone https://github.com/patgannon/sublimetext-scalatest.git ScalaTest
```

Settings
--------

You can specify a different path to the Scala executable. By default, you will need to have Scala in your path, which likely means you will need to run Sublime Text 2 from the [command line](http://www.sublimetext.com/docs/2/osx_command_line.html)

Copy the `ScalaTest.sublime-settings` file to `~/Library/Application Support/Sublime Text 2/Packages/User/` and make your changes there.


Usage
-----

 - Run single scala test fixture: `Command-Shift-X`
 - Run all scala tests in the project folder: `Option-Shift-X`
 - Switch between code and test: `Command-Shift-R`
 - Navigate to scala files in project folder (in quick panel): `Command-Shift-E`

Keys:
- 'Command' (OSX) = 'Ctrl' (Linux / Windows)
- 'Option' (OSX) = 'Alt' (Linux / Windows)


Note
----
This plug-in assumes your project folder is organized as follows:

- implementation files are in src/main/scala/[namespace]/[ImplementationClassName].scala
- test files are in src/test/scala/[namespace]/[ImplementationClassName]Test.scala
- JAR files needed to run tests are either under lib/default or lib/test

If that is not your convention, some of the features won't work.  (Use at your own risk.)  If you make modifications to accomodate your folder structure, go ahead and submit a pull request (bonus points for extensibility!)

Also note that currently this plug-in uses the JUnit test runner.

Work at Bizo
------------
If you want to work on large systems across multiple regions on AWS or on big data problems with passionate developers [email me](mailto:gannon@bizo.com).  Also check out [Bizo's dev blog](http://dev.bizo.com)

