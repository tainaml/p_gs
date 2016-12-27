import input from './customform/input'
import formset from '../vendor/jquery.formset'

module.exports = ( name ) => {
  const $root = $( name )

  input( $root.find( '[data-toggle="input"]' ))
  const $tab = $root.find( '[data-toggle="tab"]' )
  const $tabContent = $( '[role=tabpanel]' )
  const $user = $( '[name="user"]' )
  const $role = $( '[name="permission"]' )
  const $formset = $root.find( '[data-toggle="formset"]' )
  const $addMember = $root.find( '[data-toggle="add-member"]' )
  const totalForms = $('#id_' + $formset.data( 'name' ) + '-TOTAL_FORMS')
  const maxForms = $('#id_' + $formset.data( 'name' ) + '-MAX_NUM_FORMS')
  const minForms = $('#id_' + $formset.data( 'name' ) + '-MIN_NUM_FORMS')
  const childElementSelector = 'input,select,textarea,label,div'
  let usersId = []

  $tabContent.not( '.active' ).hide()

  $tab.on( 'click tap', '[role=tab]', ( event ) => {
    event.preventDefault()

    const $this = $( event.currentTarget )
    const target =  $this.attr('href')

    $this.addClass( 'active' )
    $tabContent.fadeOut(() => {
      $( target ).fadeIn()
    })
  })

  $addMember.on( 'click', ( event ) => {
    const $this = $( event.currentTarget )
    const formPrefix = $formset.data( 'name' )
    const formCount = parseInt(totalForms.val())
    let userTemplate = $formset.find( '.hidden.customform' ).clone(true)
    userTemplate.find( childElementSelector ).each( (index, element) => {
      updateElementIndex($(element), formPrefix, formCount)
    })


    if ($user.val() && $role.val()) {
      userTemplate.find( '[name $='+$user.attr('name')+']' ).val( $user.val() )
      userTemplate.find( '[name $='+$role.attr('name')+']' ).val( $role.val() )
      totalForms.val( formCount + 1);
      userTemplate.removeClass( 'hidden' )

      if ( usersId.indexOf($user.val()) > -1) {
        console.log(usersId);
      } else {
        userTemplate.attr('id', $user.val())
        $formset.append( userTemplate )
        usersId.push($user.val());
      }


    } else {
      alert( 'empty' )
    }
  })

  $formset.find( ':checkbox' ).on( 'change', ( event ) => {
    const $this = $( event.currentTarget )
    if ( $this.is( ':checked' )) {
      for (var i = 0; i < usersId.length; i++) {

        console.log(usersId[i],
        $this.parent());
        if ( usersId[i] == $this.parent().attr( 'id' )) {
          usersId.splice(i, 1)
          $this.parent().hide()
        }
      }

    }
  })
};

function updateElementIndex(elem, prefix, ndx) {
  const idRegex = new RegExp(prefix + '-(\\d+|__prefix__)-'),
      replacement = prefix + '-' + ndx + '-';
  if (elem.attr("for")) elem.attr("for", elem.attr("for").replace(idRegex, replacement));
  if (elem.attr('id')) elem.attr('id', elem.attr('id').replace(idRegex, replacement));
  if (elem.attr('name')) elem.attr('name', elem.attr('name').replace(idRegex, replacement));
}
