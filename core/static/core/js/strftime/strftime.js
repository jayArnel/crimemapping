/**
 *  Javascript Date/Time Formatter
 *
 *  Formatting directives based on Python's `strftime` formatting directives at
 *  https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
 *
 *  Sample usage:
 *
 *  (using the returned `strftime` function)
 *      var date = new Date();
 *      var formatted = strftime(date, 'c');
 *
 *  (using the `Date.prototype` method)
 *      var date = new Date();
 *      var formatted = date.strftime('c');
 **/
(function(root, declaration) {
    if (typeof define === 'function' && define.amd) {
        define([], declaration);
    } else {
        root.strftime = declaration();
    }
})(window, function() {
    var weekdaysAbbr = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    var weekdaysFull = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',
        'Friday', 'Saturday'];
    var monthsAbbr = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
        'Sep', 'Oct', 'Nov', 'Dec'];
    var monthsFull = ['January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'];
    var DAY_LENGTH = 1000 * 60 * 60 * 24;
    var WEEK_LENGTH = DAY_LENGTH * 7;


    var decorators = {
        padZero: function(func, length) {
            length = length || 2;
            var context = this;

            return function() {
                var args = Array.prototype.slice.call(arguments);
                var result = func.apply(context, args);
                while (('' + result).length < length) {
                    result = '0' + result;
                }
                return result;
            };
        }
    };


    var directives = {
        a: getWeekdayAbbreviated,
        A: getWeekdayFullname,
        w: getWeekdayDecimal,
        d: decorators.padZero(getDayOfTheMonth),
        b: getMonthAbbreviated,
        B: getMonthFullname,
        m: decorators.padZero(getMonthDecimal),
        y: decorators.padZero(getYearWithoutCentury),
        Y: getYearWithCentury,
        H: decorators.padZero(getHour24Hours),
        I: decorators.padZero(getHour12Hours),
        p: getMeridiem,
        M: decorators.padZero(getMinutes),
        S: decorators.padZero(getSeconds),
        f: decorators.padZero(getMicroseconds, 6),
        z: getTimezoneOffset,
        Z: getTimezoneName,
        j: decorators.padZero(getDayOfTheYear, 3),
        U: decorators.padZero(getWeekNumberSundayFirst),
        W: decorators.padZero(getWeekNumberMondayFirst),
        c: getDateTimeRepresentation,
        x: getDateRepresentation,
        X: getTimeRepresentation
    };


    function getWeekdayAbbreviated(date) {
        return weekdaysAbbr[date.getDay()];
    }


    function getWeekdayFullname(date) {
        return weekdaysFull[date.getDay()];
    }


    function getWeekdayDecimal(date) {
        return date.getDay();
    }


    function getDayOfTheMonth(date) {
        return date.getDate();
    }


    function getMonthAbbreviated(date) {
        return monthsAbbr[date.getMonth()];
    }


    function getMonthFullname(date) {
        return monthsFull[date.getMonth()];
    }


    function getMonthDecimal(date) {
        return date.getMonth() + 1;
    }


    function getYearWithoutCentury(date) {
        return date.getFullYear() % 100;
    }


    function getYearWithCentury(date) {
        return date.getFullYear();
    }


    function getHour24Hours(date) {
        return date.getHours();
    }


    function getHour12Hours(date) {
        var hour = date.getHours() % 12;
        return hour === 0 ? 12 : hour;
    }


    function getMeridiem(date) {
        var hour = date.getHours();
        return hour < 12 ? 'AM' : 'PM';
    }


    function getMinutes(date) {
        return date.getMinutes();
    }


    function getSeconds(date) {
        return date.getSeconds();
    }


    function getMicroseconds(date) {
        return date.getMilliseconds() * 1000;
    }


    function getTimezoneOffset(date) {
        var offset = date.toTimeString().split(' ')[1];
        if (/\w+[+-]\d+/.test(offset)) {
            var index = Math.max(offset.indexOf('+'), offset.indexOf('-'));
            return offset.substring(index);
        }
        return '';
    }


    function getTimezoneName(date) {
        var offset = date.toTimeString().split(' ')[1];
        if (/\w+[+-]\d+/.test(offset)) {
            return offset.split(/[+-]/)[0];
        }
        return '';
    }


    function getDayOfTheYear(date) {
        var startOfYear = _getStartOfYear(date);
        return Math.floor((date - startOfYear) / DAY_LENGTH) + 1;
    }


    function getWeekNumberSundayFirst(date) {
        var startOfYear = _getStartOfYear(date);
        var firstWeek = _getStartOfWeekSundayFirst(startOfYear);
        var currentWeek = _getStartOfWeekSundayFirst(date);
        return Math.floor((currentWeek - firstWeek) / WEEK_LENGTH);
    }


    function getWeekNumberMondayFirst(date) {
        var weekNumber = getWeekNumberSundayFirst(date);
        return getWeekdayDecimal(date) ? weekNumber : weekNumber - 1;
    }


    function getDateTimeRepresentation(date) {
        return strftime(date, 'a b d X Y');
    }


    function getDateRepresentation(date) {
        return strftime(date, 'm/d/Y');
    }


    function getTimeRepresentation(date) {
        return strftime(date, 'H:M:S');
    }


    function _getStartOfYear(date) {
        return new Date(date.getFullYear(), 0, 1);
    }


    function _getStartOfMonth(date) {
        return new Date(date.getFullYear(), date.getMonth(), 1);
    }


    function _getStartOfWeekSundayFirst(date) {
        var startOfWeek = _offsetDateByDays(date, -getWeekdayDecimal(date));
        startOfWeek.setHours(0, 0, 0, 0);
        return startOfWeek;
    }


    function _getStartOfWeekMondayFirst(date) {
        var startOfWeek = _offsetDateByDays(date, 1 - getWeekdayDecimal(date));
        startOfWeek.setHours(0, 0, 0, 0);
        return startOfWeek;
    }


    function _offsetDateByDays(date, days) {
        return new Date(date.getTime() + DAY_LENGTH * days);
    }


    function strftime(date, format) {
        var formatted = '';
        var formatDirectives = format.split('');
        formatDirectives.forEach(function(directive) {
            if (directives.hasOwnProperty(directive)
            && typeof directives[directive] === 'function') {
                formatted += directives[directive](date);
            } else {
                formatted += directive;
            }
        });
        return formatted;
    }


    Date.prototype.strftime = function(format) {
        return strftime(this, format);
    };


    return strftime;
});
