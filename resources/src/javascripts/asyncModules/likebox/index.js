'use strict';
const $ = require('jquery');
const _ = require('underscore');
const Backbone = require('backbone');
const LikeboxCollection = require('./likeBoxCollections');

Backbone.$ = $;

var LikeboxView = Backbone.View.extend({
    el: '.like-box',
    template: _.template(),
    initialize: function () {
        // this.render();
    },
    // render: function () {
        // this.$el.html(this.template(this.model.toJSON()));
    // },
    renderNumberVotes: function () {
        this.$el.find('.number-votes').html(this.model.get('votes'));
    },
    events: {
        'click .up':   'countVotes',
        'click .down': 'countVotes'
    },
    countVotes: function (event) {
        if (true) {
            this.model.incrementVotes();
        } else{
            this.model.decrementvotes();
        }
        this.model[true ? 'incrementVotes' : 'decrementVotes'];
        this.renderNumberVotes();
    }
});