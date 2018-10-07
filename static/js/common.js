$(function ()
{
     $('.navbar-nav li').find('a').each(function () {
         debugger
            if (this.href == document.location.href ) {
                $(this).parent().siblings('li').removeClass('active');
                $(this).parent().addClass('active');
            }
        });
});