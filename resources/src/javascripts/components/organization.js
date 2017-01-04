require('selectize')
import input from './customform/input'
import ajaxselect from '../asyncModules/ajaxselect'
import taxonomy from '../asyncModules/taxonomy'
import dropzoneUploader from '../asyncModules/dropzoneUploader'
import '../vendor/jquery.steps'
import '../vendor/jquery.validate'
module.exports = ( name ) => {
  const $root = $( name )
  const $steps = $root.find( '[data-toggle="steps"]' )
  const $form = $root.find( '[data-toggle="form"]' )
  const $templateOrganizationUser = $('#template-organization-user')
  const childElementSelector = 'input,select,textarea,label,div'
  let usersId = []
  $form.validate({
    errorPlacement: function errorPlacement(error, element) {
      element.after(error)
    }
  })
  $steps.children( '[role="tablist"]' ).steps({
    headerTag: '.organization__register__tab',
    bodyTag: '[role="tabpanel"]',
    transitionEffect: 'slideLeft',
    titleTemplate: '#title#',
    labels: {
        cancel: "Cancelar",
        current: "passo atual:",
        pagination: "Paginação",
        finish: "Criar",
        next: "Avançar",
        previous: "Voltar",
        loading: "Carregando ..."
    },
    onInit: function ( event, currentIndex ) {
      const $user = $( '[name="user"]' )
      const $role = $( '[name="permission"]' )
      const $formset = $root.find( '[data-toggle="formset"]' )
      const totalForms = $('#id_' + $formset.data( 'name' ) + '-TOTAL_FORMS')
      const maxForms = $('#id_' + $formset.data( 'name' ) + '-MAX_NUM_FORMS')
      const minForms = $('#id_' + $formset.data( 'name' ) + '-MIN_NUM_FORMS')
      input( $root.find( '[data-toggle="input"]' ))
      ajaxselect( $('[data-select="ajaxselect"]') )
      taxonomy( $('[data-select="taxonomy"]') )
      dropzoneUploader( $('[data-toggle="dropzoneUploader"]') )
      $root.find( '[data-toggle="add-member"]' ).on( 'click', ( event ) => {
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
      $formset.find('[data-id]').each(( index, element ) => {
        usersId.push( $(element).data( 'id' ))
      })
      $formset.on( 'click', '.gsticon.gsticon-close', ( event ) => {
        const $this = $( event.currentTarget )
        const _user = $this.parent().parent();
        usersId.some( user => {
          if ( user == _user.data( 'id' )) {
            usersId.splice(usersId.indexOf(user), 1)
            _user.hide()
          }
        })
      })
    },
    onStepChanging: function ( event, currentIndex, newIndex ) {
      $form.validate().settings.ignore = ':disabled,:hidden'
      return $form.valid()
    },
    onFinishing: function ( event, currentIndex ) {
      $form.validate().settings.ignore = ':disabled,:hidden'
      return $form.valid()
    },
    onFinished: function ( event, currentIndex ) {
      $form.submit()
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
