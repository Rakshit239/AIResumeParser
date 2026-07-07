import { Component, signal } from '@angular/core';
import { JobDescriptionUpload } from './components/job-description-upload/job-description-upload';

@Component({
  selector: 'app-root',
  imports: [JobDescriptionUpload],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  protected readonly title = signal('job-description-parser');
}
