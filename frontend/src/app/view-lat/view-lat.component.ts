import { Component, OnInit, Input, AfterViewInit, EventEmitter, Output  } from '@angular/core';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-view-lat',
  templateUrl: './view-lat.component.html',
  styleUrls: ['./view-lat.component.css']
})
export class ViewLatComponent implements AfterViewInit  {

 @Output() public childevent = new EventEmitter();

  public is_drawing:boolean = false;
  // public ctx: CanvasRenderingContext2D = this.canvas.getContext("2d");
  constructor(private apiService: ApiService) { }
  public canvas: any;
  public ctx: any;
  apiresult:any;

  // setting a width and height for the canvas
  @Input() public width = 600;
  @Input() public height = 300;

  ngAfterViewInit (): void {
    this.canvas = <HTMLCanvasElement> document.querySelector("#canvas");
    this.ctx = <CanvasRenderingContext2D> this.canvas.getContext("2d");
    this.ctx.fillStyle = 'white';

    // set the width and height
    this.canvas.width = this.width;
    this.canvas.height = this.height;

  }

  startdraw(ev: any){
    this.is_drawing = true;
    var rect = this.canvas.getBoundingClientRect();
    this.ctx.beginPath();
    this.ctx.lineWidth = 5;
    this.ctx.lineCap = 'round';
    this.ctx.strokeStyle = 'red';
    var x = ev.pageX - rect.left;
    var y = ev.pageY - rect.top;
    this.ctx.moveTo(x, y);
    ev.preventDefault();
  }

  logPan(ev:any){
    if(this.is_drawing){
      // console.log("event "+ev);
      // console.log("drawing");
      // console.log("X="+ev.pageX+" Y="+ev.pageY);
      var rect = this.canvas.getBoundingClientRect();
      var x = ev.pageX - rect.left;
      var y = ev.pageY - rect.top;
      this.ctx.lineTo(x, y);
       this.ctx.stroke();
     }
  }

  touchstartdraw(ev: any){
    this.is_drawing = true;
    var rect = this.canvas.getBoundingClientRect();
    this.ctx.beginPath();
    this.ctx.lineWidth = 10;
    this.ctx.lineCap = 'round';
    this.ctx.strokeStyle = 'red';
    var x = ev.touches[0].pageX - rect.left;
    var y = ev.touches[0].pageY - rect.top;
    this.ctx.moveTo(x, y);
    ev.preventDefault();
  }

  touchlogPan(ev:any){
    if(this.is_drawing){
      var rect = this.canvas.getBoundingClientRect();
      var x = ev.touches[0].pageX - rect.left;
      var y = ev.touches[0].pageY - rect.top;
      this.ctx.lineTo(x, y);
       this.ctx.stroke();
     }

  }

  stopdraw(ev: any){
    this.is_drawing = false;
  }

  async saveAsjpg(){
    var img = this.canvas.toDataURL("image/jpg");
    console.log("image "+img);
    var base64data = img.split(",")[1];
    img="";
    // console.log(base64data);
    var newbase64Img = base64data.replace(/\//g, "SLASH");
    // console.log(newbase64Img);
    // console.log(img);
    this.apiresult = await this.apiService.getApiResult(newbase64Img).toPromise();
    console.log("flask response "+ this.apiresult);
    this.childevent.emit(this.apiresult);
    // this.childevent.emit('\\frac{1}{2}+\\sqrt{4}');
  }

}
