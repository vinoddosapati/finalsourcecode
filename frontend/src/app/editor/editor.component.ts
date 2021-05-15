import { Component, Input, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { ApiService } from '../api.service';
declare var tinymce: any;
@Component({
  selector: 'app-editor',
  templateUrl: './editor.component.html',
  styleUrls: ['./editor.component.css']
})
export class EditorComponent implements OnInit {

  // Listen to parent data and load
  @Input() parentData:any;
  public src: any;
  public encodeParentData: any;
  public alt: any;
  calResult: any;
  mathResult: any;

  profileForm: any;

  constructor(private apiService: ApiService) { }

  ngOnInit(): void {

    this.getMathML()

    // Load Calculator Form
    this.profileForm = new FormGroup({
      latexEquation: new FormControl(this.parentData),
      firstName: new FormControl(''),
      lastName: new FormControl(''),
    });

    // Load TinyMCE plugins
    tinymce.init(
      {
        selector: 'textarea',
        base_url: '/tinymce',
        suffix: '.min',
        height: 500,
        menubar: true,
        relative_urls: false,
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

      this.encodeParentData = encodeURIComponent(this.parentData);
      this.alt = this.parentData;
      // Google Chart API
      this.src = "https://chart.googleapis.com/chart?cht=tx&amp;chf=a,s,000000|bg,s,FFFFFF00&amp;chl="+this.encodeParentData;


  }

  // MathML response
  async getMathML(){
    var getmathVal = this.parentData.replace(/\\/g, "FSLASH");
    getmathVal = getmathVal.replace(/\//g, "SLASH");
    this.mathResult = await this.apiService.getMathml(getmathVal).toPromise();
    console.log("Math ML ", this.mathResult);
  }


  // Submit to Calculator and get response
  async onSubmit() {
    console.log("button submit");
    var formgroupval = this.profileForm.value;
    var eq_val = formgroupval.latexEquation
    var y_val = formgroupval.firstName
    var z_val = formgroupval.lastName
    console.warn(this.profileForm.value);
    console.log(eq_val);
    var newCaleq = eq_val.replace(/\\/g, "FSLASH");
    newCaleq = newCaleq.replace(/\//g, "SLASH");
    newCaleq = newCaleq.replace(/y/g, y_val);
    newCaleq = newCaleq.replace(/z/g, z_val);

    console.log("send cal "+ newCaleq);

    this.calResult = await this.apiService.getCalResult(newCaleq).toPromise();
    eq_val="";
    console.log("flask response "+ this.calResult);
  }

}
