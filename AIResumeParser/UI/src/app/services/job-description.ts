import { Service, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ParseFileResponse {
  filename: string;
  text: string;
}

@Service()
export class JobDescription {
  private readonly apiUrl = 'http://127.0.0.1:9000/api/parse';
  private readonly http = inject(HttpClient);

  parseFile(file: File): Observable<ParseFileResponse> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post<ParseFileResponse>(this.apiUrl, formData);
  }
}
