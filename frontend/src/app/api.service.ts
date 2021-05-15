import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpHeaders} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private _http: HttpClient) { }

  rootURL = 'http://127.0.0.1:5000/';

  flaskURL = this.rootURL+'imgdata/';
  calURL = this.rootURL+'cal/';
  mathURL = this.rootURL+'mathml/';

  getApiResult(data:any){
      this.flaskURL = this.flaskURL+data;
      console.log(this.flaskURL);
      return this._http.get(this.flaskURL, { responseType: 'text' });
  }

  getCalResult(equation: any){
    this.calURL = this.calURL+equation;
    return this._http.get(this.calURL, { responseType: 'text' });
  }

  getMathml(latEq: any){
    this.mathURL = this.mathURL + latEq;
    return this._http.get(this.mathURL, { responseType: 'text' });
  }

}
