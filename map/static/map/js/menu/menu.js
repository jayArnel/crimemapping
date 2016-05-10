require([
    'jquery', 'hammerjs', 'jquery-hammerjs', 'materialize',
], function($) {
    $(".button-collapse").sideNav({
       menuWidth: 310,
    });
    $('.collapsible').collapsible();
    $('.datepicker').pickadate({
        onOpen: function() {
            var _this = this.$node;
            var select = this.get('select');
            if (select === null) {
              this.set('select', new Date(_this.data('initial')));
            }
            var start = $('.datepicker#start-date');
            var end = $('.datepicker#end-date');
            var min = start.val() ? start.val() : start.data('initial');
            var max = end.val() ? end.val() : end.data('initial');
            if (_this.is('#start-date')) {
                this.set('max', new Date(max));
            } else if (_this.is('#end-date')) {
                this.set('min', new Date(min));
            }
        },
        onClose: function() {
            $(document.activeElement).blur();
        },
        min: new Date($('.datepicker#start-date').data('initial')),
        max: new Date($('.datepicker#end-date').data('initial')),
        today: false,
        selectYears: 20,
        selectMonths: true,
        format: 'mmmm d, yyyy',
        container: 'body'
    });
});
