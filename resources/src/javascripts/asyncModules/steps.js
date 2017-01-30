import profession from './profession'
import geography from '../components/geography'
import input from '../components/customform/input'
import toggleSelect from '../components/customform/toggle-select'
import toggleCheck from '../components/customform/toggle-check'
import '../vendor/jquery.steps'
import '../vendor/jquery.validate'
import '../vendor/jquery.formset'

const steps = ( root ) => {
  const $root = $( root )
  const $form = $root.parents( 'form' )
  const stepsWithErros = []

  $( '[data-step-part="content"]' ).each((index, element) => {
    if ( element.getAttribute( 'data-error' ) == 'true' ) {
      stepsWithErros.push(index)
    }
  })

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
    enablePagination: false,
    startIndex: stepsWithErros.length ? Math.min(...stepsWithErros) : 0,
    titleTemplate: '#title#',
    onInit: function ( event, currentIndex ) {
      input( $root.find( '[data-toggle="input"]' ))
      toggleSelect( $root.find( '[data-toggle="salary"]' ), 'data-salary' )
      toggleCheck( $root.find( '[data-toggle="location"]' ), 'data-location' )
      $( '[data-toggle="tooltip"]' ).tooltip()
      let formsetLength = $( '[data-toggle="formset"]' ).length
      let professionLength = $( '[data-module="profession"]' ).length
      let geographyLength = $( '[data-component="geography"]' ).length
      if ( !!formsetLength ) {
        let $containerForm = $root.find( '[data-toggle="formset"]' )
        $containerForm.each(( index, value ) => {
          let dataFormset = $( value ).data()
          $( value ).find( '.row' ).formset({
            prefix: dataFormset.prefix,
            formCssClass: `dynamic-formset-${index}`,
            addCssClass: 'customform-button',
            addText: dataFormset.addText,
            deleteTemplate: `<div class="col-sm-1 text-center"><div class="customform customform-error">
              <a class="delete-row text-danger" href="javascript:void(0)"><i class="gsticon gsticon-lg gsticon-minus-circle"></i></a></div></div>`
          })
        })
      }
      if ( !!professionLength ) {
        profession( $root.find( '[data-module="profession"]' ))
      }

      if ( !!geographyLength ) {
        geography( $root.find( '[data-component="geography"]' ))
      }

      $( '[data-step-part="content"]' ).each((index, element) => {
        if ( element.getAttribute( 'data-error' ) == 'true' ) {
          $(`[role=tab]:eq(${index})`).addClass( 'error' )
        }
      })
    },
  })

  $root.find( '[data-step-action="next"]' ).on( 'click', ( event ) => {
    $root.steps( 'next' )
  })
}

export default steps
