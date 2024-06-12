import { Injectable } from '@angular/core';
import {QueryResponseResult} from "../types/query-response.type";

@Injectable({
  providedIn: 'root'
})
export class DataTransferService {
  private data: QueryResponseResult;

  constructor() { }

  setData(data: QueryResponseResult): void {
    this.data = data;
  }

  getData(): QueryResponseResult {
    return this.data;
  }
}
