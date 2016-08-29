#!/usr/bin/python

import pylocalizer

def main():
    pylocalizer.main(['--project', '/Users/Samantha/Work/iRobot/aspen.home/ios/aspen.xcodeproj', '--target', 'aspen', '--find-missing'])

if __name__ == "__main__":
    main()