import {Injectable} from '@angular/core';
import {environment} from "../../environments/environment";
import {HttpClient} from "@angular/common/http";
import {
  QueryResponseDocument,
  QueryResponseResult,
  QueryResponseType
} from "../types/query-response.type";
import {BehaviorSubject, lastValueFrom} from "rxjs";
import {WordEmbedding} from "../types/word-embedding-response";


@Injectable({
  providedIn: 'root'
})
export class DataService {
  private searchTextSource = new BehaviorSubject<string>('');
  currentSearchText = this.searchTextSource.asObservable();

  constructor(private httpClient: HttpClient) {
  }

  changeSearchText(text: string) {
    this.searchTextSource.next(text);
  }

  public async getQueryResults(query: String): Promise<QueryResponseResult[]> {
    const response = await lastValueFrom(this.httpClient.get<QueryResponseResult[]>(`${environment.baseUrl}/search?q=${query}`));

    return response;
  }

  public async getDocomentById(id: number) {
    return await lastValueFrom(this.httpClient.get<QueryResponseDocument>(`${environment.baseUrl}/document?id=${id}`));
  }

  public async getWordEmbedding(paragraph: String, query: String) {
    return await lastValueFrom(this.httpClient.post<WordEmbedding[]>(`${environment.baseUrl}/word_embeddings`, {'paragraph': paragraph, 'query': query}));
  }
}
