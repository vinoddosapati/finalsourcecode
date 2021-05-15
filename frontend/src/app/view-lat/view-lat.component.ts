import { Component, OnInit, Input, AfterViewInit, EventEmitter, Output  } from '@angular/core';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-view-lat',
  templateUrl: './view-lat.component.html',
  styleUrls: ['./view-lat.component.css']
})
export class ViewLatComponent implements AfterViewInit  {

//  Send latex equation to parent component
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

  // When Mouse is down
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

  // Mouse down and dragging
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

  // Touch start
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

  // Touch and drag
  touchlogPan(ev:any){
    if(this.is_drawing){
      var rect = this.canvas.getBoundingClientRect();
      var x = ev.touches[0].pageX - rect.left;
      var y = ev.touches[0].pageY - rect.top;
      this.ctx.lineTo(x, y);
       this.ctx.stroke();
     }

  }

  // Mouse out or touch end
  stopdraw(ev: any){
    this.is_drawing = false;
  }

  // save canvas image to encoded base64 image
  // Send base64 to flask server
  // Get latex script from flask
  async saveAsjpg(){
    // base64 image
    var img = this.canvas.toDataURL("image/jpg");
    var base64data = img.split(",")[1];
    img="";
    var newbase64Img = base64data.replace(/\//g, "SLASH");
    this.apiresult = await this.apiService.getApiResult(newbase64Img).toPromise();
    console.log("flask response "+ this.apiresult);
    // Emmiting response to parent component
    this.childevent.emit(this.apiresult);
  }

}
