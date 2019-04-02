nslocalizer
===========

[![Code Climate](https://img.shields.io/codeclimate/github/samdmarshall/nslocalizer.svg)](https://codeclimate.com/github/samdmarshall/nslocalizer)
[![Test Coverage](https://img.shields.io/codeclimate/coverage/github/samdmarshall/nslocalizer.svg)](https://codeclimate.com/github/samdmarshall/nslocalizer/coverage)
[![CircleCI branch](https://img.shields.io/circleci/project/samdmarshall/nslocalizer/develop.svg)](https://circleci.com/gh/samdmarshall/nslocalizer/tree/develop)
[![Dependency Status](https://dependencyci.com/github/samdmarshall/nslocalizer/badge)](https://dependencyci.com/github/samdmarshall/nslocalizer)

This is a command line tool that is used for discovering missing and unused localization strings in Xcode projects.

## Contributing and Code of Conduct [![License](https://img.shields.io/badge/License-3--Clause%20BSD-blue.svg)](./LICENSE)
This project and related material has a Code of Conduct that is listed in the [contributing.md](./contributing.md) file. This must be read and adhered to when interacting with this project. Additionally this code is released under a 3-clause BSD license that you can read [here](./LICENSE).

## Requirements  ![Python](https://img.shields.io/badge/Python3-3.5.0-brightgreen.svg)
This tool is built and tested against Python 3.5.0.

   Module | Version
----------|-----------
pbPlist   | >=1.0
pyobjc-core | >= 2.5.1
pyobjc-framework-Cocoa | >= 2.5.1
langcodes | >= 1.2.0

## Installation
Via pip and python 3

	$ pip3 install nslocalizer

To install the tool from the repo, clone from Github then run the `make build` command.

## Usage
To use **nslocalizer** to generate warnings about missing or unused NSLocalizedStrings, you will have to pass it a project and target as input:

	$ nslocalizer --project <path to xcodeproj file> --target <names of targets to analyze>

There are a number of flags that can be passed to modify the behavior of **pyconfig**:

   Flags | Usage
-------------------|-----------------------------------------------------------
`--version`        | Displays the version of **nslocalizer** and exits
`--find-missing`   | Finds any strings that are missing translations for any of the supported languages
`--find-unused`    | Finds any strings that are unused in the code
`--quiet`          | Silences all logging output
`--verbose`        | Logs additional information
`--ignore <languages>` | Will silence warnings for any of the languages listed to be ignored

> Note: Both `--find-missing` and `--find-unused` flags can be supplied to the same invocation of `nslocalizer`.

## Example

Find missing translation strings:
```
$ nslocalizer --project Foo.xcodeproj --target MyNewApp --find-missing
/Users/Samantha/Projects/Foo/Foo/Assets/Base.lproj/Localizable.strings:327: warning: String "foo_setup_twitter_integation" missing for: German, Traditional Chinese, European Portuguese, Spanish
/Users/Samantha/Projects/Foo/Foo/Assets/Base.lproj/Localizable.strings:356: warning: String "foo_setup_facebook_integation" missing for: German, Traditional Chinese, European Portuguese, Swedish, Polish, Latin American Spanish, British English, Brazilian Portuguese
```

Find unused translation strings:
```
$ nslocalizer --project Foo.xcodeproj --target MyNewApp --find-unused
/Users/Samantha/Projects/Foo/Foo/Assets/Base.lproj/Localizable.strings:327: warning: String "foo_setup_twitter_integation" is not used
/Users/Samantha/Projects/Foo/Foo/Assets/Base.lproj/Localizable.strings:356: warning: String "foo_setup_facebook_integation" is not used
```


## Integration
**nslocalizer** is intended to be used as part of a build of the Xcode project file. To integrate you will have to add a new "run script" phase to your target and then invoke as such:

```
nslocalizer --project $PROJECT_DIR/YourProject.xcodeproj --target $TARGET_NAME --find-missing --find-unused
```
