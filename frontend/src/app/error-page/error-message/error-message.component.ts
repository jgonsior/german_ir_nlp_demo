import { Component, OnInit } from '@angular/core';
import { Location } from '@angular/common';

@Component({
  selector: 'app-error-message',
  templateUrl: './error-message.component.html',
  styleUrls: ['./error-message.component.scss'],
})
export class ErrorMessageComponent implements OnInit {

  currentUrl: string;

  constructor(private location: Location) { }

  ngOnInit() {
    this.currentUrl = this.location.path();
    console.log(this.currentUrl);
  }

}