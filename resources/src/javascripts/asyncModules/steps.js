import input from '../components/customform/input'
import toggleSelect from '../components/customform/toggle-select'
import '../vendor/jquery.steps'
import '../vendor/jquery.validate'

const steps = ( root ) => {
  const $root = $( root )
  const $form = $root.parents( 'form' )

  $form.validate({
    errorPlacement: function errorPlacement(error, element) {
      element.after(error)
    },
    highlight: function(element, errorClass, validClass) {
      $( element ).parents( '.customform' ).addClass( 'customform-error' )
    },
    unhighlight: function(element, errorClass, validClass) {
      $( element ).parents( '.customform' ).removeClass( 'customform-error' )
    },
    submitHandler: function(form) {
      if ($(form).valid()) {
        form.submit()
      }
    }
  })

  $root.steps({
    headerTag: '[data-step-part="header"]',
    bodyTag: '[data-step-part="content"]',
    enableAllSteps: true,
    titleTemplate: '#title#',
    enablePagination: false,
    onInit: function ( event, currentIndex ) {
      input( $root.find( '[data-toggle="input"]' ))
      toggleSelect( $root.find( '[data-toggle="salary"]' ) )
      $( '[data-toggle="tooltip"]' ).tooltip()
    },
    onStepChanging: function ( event, currentIndex, newIndex ) {
      $form.validate().settings.ignore = ':disabled,:hidden'
      return $form.valid()
    },
  })

  $root.find( '[data-step-action="next"]' ).on( 'click', ( event ) => {
    $root.steps( 'next' )
  })
}

export default steps
