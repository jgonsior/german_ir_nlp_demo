
export interface QueryResponseType {
  search_id: string;
  answers: QueryResponseResult[]
}

export interface QueryResponseResult {
  rank: number;
  id: string;
  title: string;
  // categorie: string;
  text: string[];
}

export interface QueryResponseDocument {
  headers: string[];
  text: string[];
  title: string;
  image_links: string[]
}
