
export interface QueryResponseType {
  search_id: string;
  answers: QueryResponseResult[]
}

export interface QueryResponseResult {
  rank: number;
  document_id: string;
  document_name: string;
  categorie: string;
  authors: string[];
  passages: string[];
}
