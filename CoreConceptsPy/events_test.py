#!/usr/bin/env python

__author__ = "Marc Tim Thiemann"
__copyright__ = "Copyright 2014"
__credits__ = ["Marc Tim Thiemann"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = ""
__email__ = ""
__date__ = "December 2014"
__status__ = "Development"

import unittest
from events_impl import *

class TestEventsX(unittest.TestCase):

	def setUp(self):
		# Events to test
		self.e = PyEvent(10000, 10005) # interval event
		self.f = PyEvent(20100) # date event

		# Events for during tests
		self.g = PyEvent(10001, 10004) # normal case
		self.h = PyEvent(10000, 10003) # edge case: minimum
		self.i = PyEvent(10002, 10005) # edge case: maximum
		self.j = PyEvent(10000, 10005) # edge case: same event  

		# Events for before tests
		self.r = PyEvent(9100, 9200) # normal case
		self.s = PyEvent(8100, 9999) # edge case

		# Events for after tests
		self.t = PyEvent(10010, 11000) # normal case
		self.u = PyEvent(10006, 11111) # edge case

		# Events for overlapping tests
		self.k = PyEvent(9320, 10001) # normal case: beginning before e, ending within e
		self.l = PyEvent(10003, 10020) # normal case: beginning within e, ending after e
		self.m = PyEvent(9317, 10000) # edge case: beginning before e, ending right at the beginning of e
		self.n = PyEvent(10005, 10010) # edge case: beginning right at the end of e, ending after e
		self.o = PyEvent(10000, 10023) # error case: beginning right at the beginning of e, ending after e
		self.p = PyEvent(9100, 10005) # error case: beginning before e, ending right at the ending of e
		self.q = PyEvent(9000, 11000) # error case: beginning before e, ending after e
		
	def test_constructor_with_two_arguments(self):
		''' Test constructor for an interval event '''
		self.assertEqual(self.e.startTime, 10000)
		self.assertEqual(self.e.endTime, 10005)

	def test_constructor_with_one_argument(self):
		''' Test constructor for a date event '''
		self.assertEqual(self.f.startTime, 20100)
		self.assertEqual(self.f.endTime, 20100)

	def test_within(self):
		interval = self.e.within()
		self.assertEqual(interval[0], 10000)
		self.assertEqual(interval[1], 10005)

	def test_when(self):
		self.assertEqual(self.e.when(), 10000)

	def test_during_normal(self):
		''' Normal case: Event g is during Event e '''
		self.assertTrue(self.g.during(self.e)) 

	def test_during_edge_minimum(self):
		''' Edge case: Event h starts at the same time as Event e and ends within Event e '''
		self.assertTrue(self.h.during(self.e)) 

	def test_during_edge_maximum(self):
		''' Edge case: Event i starts during Event e and ends right at the same time as Event e '''
		self.assertTrue(self.i.during(self.e)) 

	def test_during_error_minimum(self):
		''' Error case: Event m starts before Event e and ends right at the beginning of Event e '''
		self.assertFalse(self.m.during(self.e))

	def test_during_error_minimum_2(self):
		''' Error case: Event k starts before Event e and ends during Event e '''
		self.assertFalse(self.k.during(self.e))

	def test_during_error_maximum(self):
		''' Error case: Event n starts right at the end of Event e and ends after Event e '''
		self.assertFalse(self.n.during(self.e))

	def test_during_error_maximum_2(self):
		''' Error case: Event l starts within Event e and ends after Event e '''
		self.assertFalse(self.l.during(self.e))

	def test_during_error_total(self):
		''' Error case: Event q starts before Event e and ends after Event e '''
		self.assertFalse(self.q.during(self.e))

	def test_before_normal(self):
		''' Normal case: Event r ends before Event e starts '''
		self.assertTrue(self.r.before(self.e)) 

	def test_before_edge(self):
		''' Edge case: Event s ends right before Event e starts '''
		self.assertTrue(self.s.before(self.e)) 

	def test_before_error_1(self):
		''' Error case: Event m ends right at the beginning of Event e '''
		self.assertFalse(self.m.before(self.e)) 

	def test_before_error_2(self):
		''' Error case: Event l ends after the beginning of Event e '''
		self.assertFalse(self.l.before(self.e)) 

	def test_after_normal(self):
		''' Normal case: Event t begins after Event e '''
		self.assertTrue(self.t.after(self.e)) 

	def test_after_edge(self):
		''' edge case: Event u begins right after Event e ends '''
		self.assertTrue(self.u.after(self.e)) 

	def test_after_error_1(self):
		''' Error case: Event n starts right at the end of Event e '''
		self.assertFalse(self.n.after(self.e)) 

	def test_after_error_2(self):
		''' Error case: Event k starts before the end of Event e '''
		self.assertFalse(self.k.after(self.e)) 

	def test_overlap_normal_1(self):
		''' Normal Case 1: Event k starts before Event e and ends during Event e '''
		self.assertTrue(self.k.overlap(self.e))

	def test_overlap_normal_2(self):
		''' Normal Case 2: Event l begins during Event e and ends after Event e '''
		self.assertTrue(self.l.overlap(self.e))

	def test_overlap_edge_1(self):
		''' Edge Case 1: Event m starts before Event e and ends right at the beginning of Event e '''
		self.assertTrue(self.m.overlap(self.e))

	def test_overlap_edge_2(self):
		''' Edge Case 1: Event n starts right at the end of Event e and ends after Event e '''
		self.assertTrue(self.n.overlap(self.e))

	def test_overlap_error_1(self):
		''' Error Case 1: Event o starts right at the beginning of Event e and ends after Event e '''
		self.assertFalse(self.o.overlap(self.e))	

	def test_overlap_error_2(self):
		''' Error Case 2: Event p starts before Event e and ends at the same time as Event e '''
		self.assertFalse(self.p.overlap(self.e))

	def test_overlap_error_3(self):
		''' Error Case 3: Event q starts before Event e and ends after Event e '''
		self.assertFalse(self.q.overlap(self.e))

	def test_overlap_error_4(self):
		''' Error case 4: Event j has the same start time and end time as Event e '''
		self.assertFalse(self.j.overlap(self.e))

if __name__ == '__main__':
	unittest.main()