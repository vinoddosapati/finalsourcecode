import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
declare var tinymce: any;
@Component({
  selector: 'app-tinymcecomp',
  templateUrl: './tinymcecomp.component.html',
  styleUrls: ['./tinymcecomp.component.css']
})
export class TinymcecompComponent implements OnInit {

  constructor(private apiservice: ApiService) { }
  // Get equation from child component canvas
  public gotLatEq: any;

  ngOnInit(): void {
    tinymce.init(
      {
        selector: 'textarea',
        base_url: '/tinymce',
        suffix: '.min',
        height: 500,
        menubar: true,
        external_plugins: { tiny_mce_wiris: 'https://www.wiris.net/demo/plugins/tiny_mce/plugin.js' },

        plugins: [
          'advlist autolink lists link image charmap print preview anchor',
          'searchreplace visualblocks code fullscreen',
          'insertdatetime media table paste code help wordcount'
        ],
        toolbar:
          'undo redo | formatselect | bold italic backcolor | \
          alignleft aligncenter alignright alignjustify | \
          bullist numlist outdent indent | removeformat | tiny_mce_wiris_formulaEditor| tiny_mce_wiris_formulaEditorChemistry | help'
      });


  }

}
