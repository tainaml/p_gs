'use strict';
const $ = require('jquery');
const _ = require('underscore');
const Backbone = require('backbone');

Backbone.$ = $;

const LikeboxModel = Backbone.Model.extend({
    defaults: {
        votes: 0
    },
    incrementVotes: function () {},
    decrementVotes: function () {}
});

module.exports = LikeboxModel;