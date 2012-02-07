//
(function($){

$.fn.greyHolder = function(params){
        var defaults = $.extend({
            inactive_class : 'greyHolder',
            active_class : '',
            default_value_attribute : 'default'
        }, params);

        return this.each(function(){
            var existingVal = $(this).val();
            $(this).attr(defaults.default_value_attribute, existingVal);

            if(!$(this).hasClass(defaults.inactive_class))
            {
                $(this).addClass(defaults.inactive_class);
            }

            $(this).focus(function(){
                $(this).val('');
                $(this).addClass(defaults.active_class);
                $(this).removeClass(defaults.inactive_class);
            });

            $(this).blur(function(){
                var value = $(this).val();

                if(value == '')
                {
                    var base = $(this).attr(defaults.default_value_attribute);
                    $(this).addClass(defaults.inactive_class);
                    $(this).removeClass(defaults.active_class);
                    $(this).val(base);
                }
            });
        });
    };
})(jQuery);
