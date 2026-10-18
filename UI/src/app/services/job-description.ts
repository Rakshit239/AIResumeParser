// import { Service, inject } from '@angular/core';
import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface UploadResponse {

  message: string;

  filename: string;

  matches: {
    [key: string]: number;
  };

  path: string;

}

@Injectable({
  providedIn: 'root'
})
export class JobDescription {
  private readonly apiUrl = 'http://127.0.0.1:9000/api/upload';
  private readonly http = inject(HttpClient);

  uploadResume(file: File): Observable<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post<UploadResponse>(this.apiUrl, formData);
  }
}
