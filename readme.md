nslocalizer
===========

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

## Installation [![homebrew](https://img.shields.io/badge/homebrew-v1.0-brightgreen.svg)](https://github.com/samdmarshall/homebrew-formulae) [![homebrew](https://img.shields.io/badge/homebrew-HEAD-orange.svg)](https://github.com/samdmarshall/homebrew-formulae)
Via [homebrew](http://brew.sh):

	$ brew update
	$ brew tap samdmarshall/formulae
	$ brew install samdmarshall/formulae/nslocalizer

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


