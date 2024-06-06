import {Injectable} from '@angular/core';
import {environment} from "../../environments/environment";
import {HttpClient} from "@angular/common/http";
import {QueryResponseResult, QueryResponseType} from "../types/query-response.type";
import {lastValueFrom} from "rxjs";


@Injectable({
  providedIn: 'root'
})
export class DataService {

  constructor(private httpClient: HttpClient) {
  }

  public async getQueryResults(query: String): Promise<QueryResponseResult[]> {
    const response = await lastValueFrom(this.httpClient.get<QueryResponseType>(`${environment.baseUrl}/search?q=${query}`));

    return response.answers;
  }

  public async getDocomentById(id: number) {
    return await lastValueFrom(this.httpClient.get<String>(`${environment.baseUrl}/document?id=${id}`));
  }
}
