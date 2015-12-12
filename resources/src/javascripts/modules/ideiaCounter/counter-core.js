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

    var ideiaCounter = {
        init: function( elem , options ) {
            var self = this,
                $html = $('html');

            self.elem = elem;
            self.$elem = $( elem );

            self.ckeditor = (self.$elem.attr('id') in CKEDITOR.instances)
                ? CKEDITOR.instances[self.$elem.attr( 'id' )]
                : null;

            if (self.ckeditor) {
                self.ckeditor.on('instanceReady', function() {
                    console.log('tem instance');
                    console.log(self.ckeditor.document.getBody().getText());
                });
            }

            self.count = (self.ckeditor)
                ? self.ckeditor.getData().length
                : self.$elem.val().length;

            self.content = (self.ckeditor)
                ? self.ckeditor.document.getBody().getText()
                : self.$elem.val();

            console.log(self.content);

            self.lang = ( typeof $html.attr( 'lang' ) === "string" )
                ? $html.attr( 'lang' )
                : 'pt-br';

            self.options = $.extend( {}, $.fn.ideiaCounter.options, options );
            self.messages = $.extend( {}, $.fn.ideiaCounter.messages );

            if ( self.options.counterDebug )
                debug( 'Init' );

            if ( self.options.counterHelp )
                self.help.insert( self );

            self.$elem.keydown( function() {
                self.countChar();
                self.calcDiff();

                if ( typeof self.options.counterSlug === "boolean" && self.options.counterSlug == true) {
                    self.createSlug();
                }
            });

            self.$elem.keyup( function() {
                self.countChar();
                self.calcDiff();

                if ( typeof self.options.counterSlug === "boolean" && self.options.counterSlug == true) {
                    self.createSlug();
                }
            });
        },

        countChar: function() {
            var self = this;
            self.count = self.$elem.val().length;

            if ( self.options.counterDebug )
                debug( 'Count Characters - Total: ' + self.count );
        },

        calcDiff: function() {
            var self = this;

            if ( self.count > self.options.counterLimit )
                self.$elem.val( self.$elem.val().substr( 0, self.options.counterLimit ) );
            else
                self.help.update( self );

            if ( self.options.counterDebug )
                debug( 'Calc Diff' );
        },

        help: {
            insert: function( obj ) {
                var self = obj,
                    message = '',
                    remain = null;

                if ( typeof  self.options.counterType === "string" && self.options.counterType == 'min' ) {
                    remain = (self.options.counterMin >= self.count)
                        ? self.options.counterMin - self.count
                        : 0;
                } else {
                    remain = (self.options.counterLimit >= self.count)
                        ? self.options.counterLimit - self.count
                        : 0;
                }

                self.$helpBlock = $( '<span></span>' );
                self.$helpBlock.addClass( 'help-block text-right' );

                if ( remain > 0 )
                    message = ( remain > 1)
                        ? self.messages[ self.lang ].remains.replace( /{countChar}/ig, remain )
                        : self.messages[ self.lang ].remain.replace( /{countChar}/ig, remain );
                else
                    message = self.messages[ self.lang ].nochar.replace( /{countChar}/ig, remain );

                self.$helpBlock.text( message );

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
                    remain = (self.options.counterLimit >= self.count)
                        ? self.options.counterLimit - self.count
                        : 0;

                if ( typeof self.options.counterReplaceTarget === "object" && self.options.counterReplaceTarget.length > 0 ) {
                    for (var i = 0; i < self.options.counterReplaceTarget.length; i++) {
                        $( self.options.counterReplaceTarget[i] ).text( self.$elem.val() || self.content );
                    }
                }

                if ( remain > 0 )
                    message = ( remain > 1)
                        ? self.messages[ self.lang ].remains.replace( /{countChar}/ig, remain )
                        : self.messages[ self.lang ].remain.replace( /{countChar}/ig, remain );
                else
                    message = self.messages[ self.lang ].nochar.replace( /{countChar}/ig, remain );

                if ( self.$helpBlock )
                    self.$helpBlock.text( message );
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
        counterDebug: true
    };

    $.fn.ideiaCounter.messages = {
        'pt-br': {
            remains: 'Restam {countChar} caracteres.',
            remain: 'Resta {countChar} carctere.',
            nochar: 'Não há mais caracteres disponíveis.'

        },
        'en-us': {
            remains: '{countChar} characters left.',
            remain: '{countChar} character left.',
            nochar: 'No more characters available.'
        }
    };


    function debug( msg ) {
        console.log( '[ideiaCounter] ' + msg );
    }


    $( document ).on( 'ready', function () {
        $( '[data-toggle=counter]' ).each( function () {
            var $c = $( this );
            $c.ideiaCounter( $c.data() );
        });
    });


})( jQuery, window, document );