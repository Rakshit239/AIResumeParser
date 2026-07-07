import { Component, inject, signal } from '@angular/core';
import { JobDescription } from '../../services/job-description';

const ALLOWED_EXTENSIONS = ['.pdf', '.docx', '.txt'];

@Component({
  selector: 'app-job-description-upload',
  imports: [],
  templateUrl: './job-description-upload.html',
  styleUrl: './job-description-upload.css',
})
export class JobDescriptionUpload {
  private readonly jobDescriptionService = inject(JobDescription);

  selectedFile = signal<File | null>(null);
  extractedText = signal<string>('');
  loading = signal(false);
  errorMessage = signal<string | null>(null);

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0] ?? null;

    this.errorMessage.set(null);
    this.extractedText.set('');

    if (!file) {
      this.selectedFile.set(null);
      return;
    }

    const extension = file.name.slice(file.name.lastIndexOf('.')).toLowerCase();
    if (!ALLOWED_EXTENSIONS.includes(extension)) {
      this.selectedFile.set(null);
      input.value = '';
      this.errorMessage.set('Unsupported file type. Please upload a .pdf, .docx, or .txt file.');
      return;
    }

    this.selectedFile.set(file);
  }

  onUpload(): void {
    const file = this.selectedFile();
    if (!file) {
      this.errorMessage.set('Please choose a file first.');
      return;
    }

    this.loading.set(true);
    this.errorMessage.set(null);
    this.extractedText.set('');

    this.jobDescriptionService.parseFile(file).subscribe({
      next: (response) => {
        this.extractedText.set(response.text);
        this.loading.set(false);
      },
      error: (err) => {
        this.errorMessage.set(
          err.error?.error ?? 'Something went wrong while parsing the file. Please try again.',
        );
        this.loading.set(false);
      },
    });
  }

  reset(): void {
    this.selectedFile.set(null);
    this.extractedText.set('');
    this.errorMessage.set(null);
  }
}
