import toggleSelect from './customform/toggle-select'

module.exports = (name) => {
  const $root = $( name )
  toggleSelect( $root.find( '[data-toggle="salary"]' ) )

  // console.log( $root )
}
