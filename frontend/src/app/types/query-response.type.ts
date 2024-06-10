
export interface QueryResponseType {
  search_id: string;
  answers: QueryResponseResult[]
}

export interface QueryResponseResult {
  rank: number;
  id: string;
  title: string;
  // categorie: string;
  passage: string;
}

export interface QueryResponseDocument {
  headers: string[];
  text: string[];
  title: string;
  image_links: string[]
}

export enum ParsedDocumentTextTypes {
  heading,
  normal_text_passage
}

export interface ParsedQueryResponseDocument {
  text: {
    'type': ParsedDocumentTextTypes,
    'depth': number,
    'content': string,
  }[];
  title: string;
}
