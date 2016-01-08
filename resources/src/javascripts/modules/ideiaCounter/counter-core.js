/**
 * Created by raphaelfruneaux on 22/12/14.
 */

if ( typeof Object.create !== 'function' ) {
    Object.create = function( obj ) {
        function F() {}
        F.prototype = obj;
        return new F();
    }
}


(function( $ ) {

    'use strict';

    var COUNT_REGEX = /{counter}/ig;

    var ideiaCounter = {
        init: function( elem , options ) {
            var self = this,
                $html = $('html');

            self.elem = elem;
            self.$elem = $( elem );

            self.ckeditor = (self.$elem.attr('id') in CKEDITOR.instances)
                ? CKEDITOR.instances[self.$elem.attr( 'id' )]
                : null;

            self.lang = ( typeof $html.attr( 'lang' ) === "string" )
                ? $html.attr( 'lang' )
                : 'pt-br';

            self.content = (self.ckeditor)
                ? self.ckeditor.getData()
                : self.$elem.val();

            if ( self.ckeditor ) {
                self.ckeditor.on( 'contentDom', function(e) {
                    self.content = self.ckeditor.document.getBody().getText();
                });
            } else {
                self.content = self.$elem.val();
            }

            self.count = self.content.length;

            self.options = $.extend( {}, $.fn.ideiaCounter.options, options );
            self.messages = $.extend( {}, $.fn.ideiaCounter.messages );

            if ( self.options.counterDebug )
                debug( 'Init' );

            if ( self.options.counterHelp )
                self.help.insert( self );

            if ( self.ckeditor ) {

                self.ckeditor.on('contentDom', function() {
                    self.counter( self );
                    self.limiter( self );

                    self.ckeditor.document.on( 'keydown', function() {
                        self.counter( self );
                        self.limiter( self );
                    });

                    self.ckeditor.document.on( 'keyup', function() {
                        self.counter( self );
                        self.limiter( self );

                        if ( typeof self.options.counterSlug === "boolean" && self.options.counterSlug == true) {
                            self.createSlug();
                        }
                    });
                });

            } else {

                self.$elem.keydown( function(e) {
                    self.counter( self );
                    self.limiter( self );
                });

                self.$elem.keyup( function(e) {
                    self.counter( self );
                    self.limiter( self );

                    if ( typeof self.options.counterSlug === "boolean" && self.options.counterSlug == true ) {
                        self.createSlug();
                    }
                });

            }
        },

        counter: function( obj ) {
            var self = obj;

            self.content = ( self.ckeditor && CKEDITOR.status == "loaded" )
                ? self.ckeditor.document.getBody().getText()
                : self.$elem.val();

            self.count = self.content.length;

            if ( self.options.counterDebug ) {
                debug( 'Method: Counter | Characters - Total: ' + self.count );
            }
        },

        limiter: function( obj ) {
            var self = obj;

            if ( typeof self.counterType === "string" && self.counterType == "max" && self.count > self.options.counterLimit )
                self.$elem.val( self.$elem.val().substr( 0, self.options.counterLimit ) );
            else
                self.help.update( self );

            if ( self.options.counterDebug )
                debug( 'Method: Limiter' );
        },

        help: {
            insert: function( obj ) {
                var self = obj,
                    message = '',
                    remain = null;

                if ( typeof  self.options.counterType === "string" && self.options.counterType == "min" ) {
                    remain = self.count;
                } else {
                    remain = ( self.options.counterLimit >= self.count )
                        ? self.options.counterLimit - self.count
                        : 0;
                }

                self.$helpBlock = $( '<span></span>' );
                self.$helpBlock.addClass( 'help-block text-right' );

                if ( typeof self.options.counterType === "string" && self.options.counterType == "min" ) {

                    var $span = $( '<span/>' );
                    $span.text( remain );

                    var $div = $( '<div/>' );
                    $div.html( $span );

                    if ( self.count < self.options.counterMin )
                        $span.css({'color': self.options.counterStyle.red});
                    else
                        $span.css({'color': self.options.counterStyle.green});

                    message = self.messages[ self.lang ].minimum.message.replace( COUNT_REGEX, $div.html() );

                } else {
                    if ( remain > 0 )
                        message = ( remain > 1)
                            ? self.messages[ self.lang ].limit.remains.replace( COUNT_REGEX, remain )
                            : self.messages[ self.lang ].limit.remain.replace( COUNT_REGEX, remain );
                    else
                        message = self.messages[ self.lang ].limit.nochar.replace( COUNT_REGEX, remain );
                }

                self.$helpBlock.html( message );

                if ( typeof self.options.counterInsert === "string" && self.options.counterInsert == 'before' ) {
                    self.$helpBlock.css({
                        'margin-top': 0,
                        'margin-bottom': 0
                    });

                    self.$helpBlockContainer = $( '<span></span>' );
                    self.$helpBlockContainer
                        .addClass('pull-right')
                        .html( self.$helpBlock );

                    self.$elem.before( self.$helpBlockContainer );
                } else {
                    self.$elem.after( self.$helpBlock );
                }
            },

            update: function( obj ) {
                var self = obj,
                    message = '',
                    remain = null;

                if ( typeof  self.options.counterType === "string" && self.options.counterType == "min" ) {
                    remain = self.count;
                } else {
                    remain = (self.options.counterLimit >= self.count)
                        ? self.options.counterLimit - self.count
                        : 0;
                }

                if ( typeof self.options.counterReplaceTarget === "object" && self.options.counterReplaceTarget.length > 0 ) {
                    for (var i = 0; i < self.options.counterReplaceTarget.length; i++) {
                        $( self.options.counterReplaceTarget[i] ).text( self.$elem.val() || self.content );
                    }
                }

                if ( typeof self.options.counterType === "string" && self.options.counterType == "min" ) {

                    var $span = $( '<span/>' );
                        $span.text( remain );

                    var $div = $( '<div/>' );
                        $div.html( $span );

                    if ( self.count < self.options.counterMin )
                        $span.css({'color': self.options.counterStyle.red});
                    else
                        $span.css({'color': self.options.counterStyle.green});

                    message = self.messages[ self.lang ].minimum.message.replace( COUNT_REGEX, $div.html() );

                } else {
                    if ( remain > 0 )
                        message = ( remain > 1 )
                            ? self.messages[ self.lang ].limit.remains.replace( COUNT_REGEX, remain )
                            : self.messages[ self.lang ].limit.remain.replace( COUNT_REGEX, remain );
                    else
                        message = self.messages[ self.lang ].limit.nochar.replace( COUNT_REGEX, remain );
                }

                if ( self.$helpBlock )
                    self.$helpBlock.html( message );
            }
        },

        createSlug: function() {
            var self = this;

            var slugTarget = ( typeof self.options.counterSlugTarget === "string" && self.options.counterSlugTarget )
                    ? $( self.options.counterSlugTarget )
                    : '#permalink',

                slug = self.$elem.val();

            slug = slug
                .replace(/^\s+|\s+$/g, '')
                .toLowerCase();

            // remove accents, swap Ã± for n, etc
            var from = "Ã£Ã Ã¡Ã¤Ã¢áº½Ã¨Ã©Ã«ÃªÃ¬Ã­Ã¯Ã®ÃµÃ²Ã³Ã¶Ã´Ã¹ÃºÃ¼Ã»Ã±Ã§Â·/_,:;";
            var to   = "aaaaaeeeeeiiiiooooouuuunc------";
            for (var i = 0, l = from.length ; i < l ; i++)
            {
                slug = slug.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));
            }

            slug = slug
                .replace(/[^a-z0-9 -]/g, '') // remove invalid chars
                .replace(/\s+/g, '-') // collapse whitespace and replace by -
                .replace(/-+/g, '-'); // collapse dashes


            slugTarget.html( slug.substr( 0, self.options.counterLimit) );
        }

    };

    $.fn.ideiaCounter = function( options ) {
        return this.each(function() {

            var c = Object.create( ideiaCounter );
            c.init( this, options );
            $.data( this, 'ideiaCounter', c );

        });
    };

    $.fn.ideiaCounter.options = {
        counterType: 'max',
        counterMin: 100,
        counterLimit: 140,
        counterHelp: true,
        counterInsert: 'after',
        counterSlug: false,
        counterSlugTarget: '#permalink',
        counterDebug: false,
        counterStyle: {
            'red': '#E12C2C',
            'green' : 'green'
        }
    };

    $.fn.ideiaCounter.messages = {
        'pt-br': {
            minimum: {
                message: '<p class="article-counter">Número de caracteres: {counter}</p>'
            },
            limit: {
                remains: 'Restam {counter} caracteres.',
                remain: 'Resta {counter} carctere.',
                nochar: 'Não há mais caracteres disponíveis.'
            }
        },
        'en-us': {
            minimum: {
                message: '{counter}'
            },
            limit: {
                remains: '{counter} characters left.',
                remain: '{counter} character left.',
                nochar: 'No more characters available.'
            }
        }
    };


    function debug( msg ) {
        console.log( '[ideiaCounter] ' + msg );
    }


    $( document ).on( 'ready', function () {
        var IdeiaCOUNTER = {
            instances: []
        };

        $( '[data-toggle=counter]' ).each( function () {
            var $c = $( this );
            $c.ideiaCounter( $c.data() );

            IdeiaCOUNTER.instances.push( $c );
        });
    });


})( jQuery, window, document );