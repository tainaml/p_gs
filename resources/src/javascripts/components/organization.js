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
  const $templateOrganizationUser = $('#template-organization-user')
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

  $formset.find('[data-id]').each(( index, element ) => {
    usersId.push( $(element).data( 'id' ))
  })

  $addMember.on( 'click', ( event ) => {
    const $this = $( event.currentTarget )
    const formPrefix = $formset.data( 'name' )
    const formCount = parseInt(totalForms.val())
    let userTemplate = $templateOrganizationUser.clone(true)


    if ($user.val() && $role.val()) {
      userTemplate.find( '[name $='+$user.attr('name')+']' ).val( $user.val() )
      userTemplate.find( '[name $='+$role.attr('name')+']' ).val( $role.val() )
      userTemplate.removeAttr('id')
      userTemplate.removeProp('id')

      if ( !(usersId.indexOf($user.val()) > -1)) {
        userTemplate.find( childElementSelector ).each( (index, element) => {
          updateElementIndex($(element), formPrefix, formCount)
        })
        totalForms.val( formCount + 1)
        $( userTemplate ).find( '[data-target="name"]').text( $user.text())
        $( userTemplate ).find( '[data-target="role"]').text( $role.find('option:selected').text())
        $( userTemplate ).find( 'img').attr( 'src', `${location.origin}/perfil/dinamic-profile-image/${$user.val()}/70/`)
        userTemplate.removeClass( 'hidden' )
        userTemplate.data( 'id', $user.val())
        $formset.append( userTemplate )
        usersId.push($user.val())
      }

    } else {
      alert( 'empty' )
    }
  })

  $formset.on( 'click', '.gsticon.gsticon-close', ( event ) => {
    const $this = $( event.currentTarget )
    const _user = $this.parent().parent();
      usersId.some( user => {
        console.log(user);
        if ( user == _user.data( 'id' )) {
          usersId.splice(usersId.indexOf(user), 1)
          _user.hide()
        }
      })

  })
};

function updateElementIndex(elem, prefix, ndx) {
  const idRegex = new RegExp(prefix + '-(\\d+|__prefix__)-'),
      replacement = prefix + '-' + ndx + '-';
  if (elem.attr("for")) elem.attr("for", elem.attr("for").replace(idRegex, replacement));
  if (elem.attr('id')) elem.attr('id', elem.attr('id').replace(idRegex, replacement));
  if (elem.attr('name')) elem.attr('name', elem.attr('name').replace(idRegex, replacement));
}
