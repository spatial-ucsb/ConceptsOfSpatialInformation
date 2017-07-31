/**
 * JavaScript implementation of the core concept 'event'.
 * version: 2.0.0
 * (c) Liangcun Jiang
 * latest change: July 30, 2017.
 * Dev notes:
 */
define([
    "dojo/_base/declare",
    "dojo/domReady!"
], function (declare) {
    //null signifies that this class has no classes to inherit from
    return declare(null, {
        /**
         * Event constructor: Constructs an event instance
         * @param id: the identity of an event.
         * @param period: {start: JS Date object, end: JS Date object}
         * @param participants: an array of participants of this event (e.g. CcField, CcObject, CcNetwork),
         * @param opt: optional parameters
         */
        constructor: function (id, period, participants, opt) {
            this.id = id;
            this.start = period.start;
            this.end = period.end;
            this.participants = participants;
            this.props = opt;
        },

        /**
         * Event function: returns a Period
         */
        within: function () {
            return [this.start, this.end];
        },

        /**
         * Event function: returns the start time of this event
         */
        when: function () {
            return this.start;
        },

        /**
         * Event function: returns true if the event happened during another event e.
         * Return type: Boolean
         */
        during: function (e) {
            return e.start <= this.start && this.end <= e.end;
        },

        /**
         * Event function: returns true if the event happened before another event e.
         * Return type: Boolean
         */
        before: function (e) {
            return this.end <= e.start;
        },

        /**
         * Event function: returns true if the event happened after another event e.
         * Return type: Boolean
         */
        after: function (e) {
            return e.end <= this.start;
        },

        /**
         * Event function: returns true if the event overlaps another event e.
         * Return type: Boolean
         */
        overlap: function (e) {
            return this.end > e.start || e.end > this.start;
        }
    });
});
