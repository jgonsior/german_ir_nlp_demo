import {QueryResponseResult} from "./query-response.type";

export interface WordEmbeddingResponse {
  results: WordEmbedding[];
}
export interface WordEmbedding {
  word: string;
  embedded: number[];
}
