import {QueryResponseResult} from "./query-response.type";

export interface WordEmbeddingResponse {
  result: WordEmbedding[];
}
export interface WordEmbedding {
  word: string;
  embedding: number;
}
