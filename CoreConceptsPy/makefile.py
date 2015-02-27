# This is a helper script to run the tests and examples where make does not work seamlessly *caugh* windows *caugh* ...

import fnmatch
import os
import subprocess
import sys
import unittest

examples = {
    'events': [
        'example-1.py',
        'example-2.py',
        'example-3.py'
    ],
    'fields': [],
    'locations': [],
    'networks': [
        'karate.py',
        'fake_weighted_network.py',
        'ucsb.py'
    ],
    'objects': []
}

def usage():
    print 'Usage: python %s test-events|fields|locations|networks|objects|all' % (sys.argv[0])
    print '  or:  python %s example-events|fields|locations|networks|objects|all' % (sys.argv[0])

def clean():
    for root, dirnames, filenames in os.walk('.'):
        for filename in fnmatch.filter(filenames, '*.pyc'):
            os.remove(os.path.join(root, filename))

def test(selector):
    suite = unittest.TestSuite()
    suite.addTest(unittest.defaultTestLoader.discover('test', selector, '..'))
    unittest.TextTestRunner().run(suite)

def example(selector = None):
    for cc in examples:
        if selector == None or cc == selector:
            for f in examples[cc]:
                subprocess.call('python examples/' + cc + '/' + f, shell = True)

if __name__ == '__main__':
    if os.path.dirname(os.path.abspath(__file__)) != os.getcwd():
        print 'This script should be run from inside of ' + os.path.dirname(os.path.abspath(__file__))
    elif len(sys.argv) >= 2:
        clean()
        if sys.argv[1] == 'clean':
            pass
        elif sys.argv[1] == 'test-events':
            test('events')
        elif sys.argv[1] == 'test-fields':
            test('fields')
        elif sys.argv[1] == 'test-locations':
            print "No examples and no tests for locations yet."
        elif sys.argv[1] == 'test-networks':
            test('networks')
        elif sys.argv[1] == 'test-objects':
            test('objects')
        elif sys.argv[1] == 'test-all':
            test('*')
        elif sys.argv[1] == 'example-events':
            example('events')
        elif sys.argv[1] == 'example-fields':
            print "No examples for fields yet. Have a look at the tests."
        elif sys.argv[1] == 'example-locations':
            print "No examples and no tests for locations yet."
        elif sys.argv[1] == 'example-networks':
            example('networks')
        elif sys.argv[1] == 'example-objects':
            print "No examples for objects yet. Have a look at the tests."
        elif sys.argv[1] == 'example-all':
            example()
        else:
            usage()
    else:
        usage()
