'use strict';

import { loadCSS } from 'fg-loadcss'
import '../../node_modules/fg-loadcss/src/onloadCSS'

const ADITIONAL_CSS = $( 'main' ).data( 'asyncstyle' )

loadCSS(ADITIONAL_CSS, $( 'link' )[0] )
