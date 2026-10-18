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

  jobDescriptions = [

    'Frontend Developer',

    'Backend Developer',

    'Full Stack Developer',

    'Business Analyst',

    'Machine Learning Engineer'

];

  selectedJob = signal(this.jobDescriptions[0]);

  selectedFile = signal<File | null>(null);
  // matchScore = signal(0);
  matchScore = signal<number | null>(null);
  allMatches: { [key: string]: number } = {};

matchedSkills = signal<string[]>([]);
loading = signal(false);
analysisReady = signal(false);



  selectJob(job: string) {

    this.selectedJob.set(job);

    if (this.allMatches[job] !== undefined) {

        this.matchScore.set(
            this.allMatches[job]
        );

    }

}



  onFileSelected(event: Event): void {

    const input = event.target as HTMLInputElement;

    const file = input.files?.[0] ?? null;

    if (!file){

      this.selectedFile.set(null);

      return;

    }

    const extension = file.name
      .slice(file.name.lastIndexOf('.'))
      .toLowerCase();

    if(!ALLOWED_EXTENSIONS.includes(extension)){

      alert('Only PDF, DOCX and TXT files are allowed.');

      input.value='';

      return;

    }

    this.analysisReady.set(false);
    this.matchScore.set(null);
    this.allMatches = {};

    this.selectedFile.set(file);  
    this.uploadResume(file);

input.value = '';

  }
  uploadResume(file: File): void {

  this.loading.set(true);
  this.analysisReady.set(false);

  this.jobDescriptionService.uploadResume(file).subscribe({

    next: (response: any) => {

      console.log(response);
      this.allMatches = response.matches;
      this.matchScore.set(
        this.allMatches[this.selectedJob()]
      );
      this.matchedSkills.set(response.skills);
      this.analysisReady.set(true);
      this.loading.set(false);

    },

    error: (err: any) => {

      console.log(err);
      
      this.loading.set(false);

    }

  });

}
viewJD(job: string): void {

  const roleMap: { [key: string]: string } = {
    'Frontend Developer': 'frontend',
    'Backend Developer': 'backend',
    'Full Stack Developer': 'fullstack',
    'Business Analyst': 'business',
    'Machine Learning Engineer': 'ml'
  };

  const role = roleMap[job];

  if (role) {
    window.open(
      `http://127.0.0.1:9000/api/jd/${role}`,
      '_blank'
    );
  }

}
getScoreColor(): string {

  const score = this.matchScore() ?? 0;

  if (score >= 70) return '#28a745';
  if (score >= 50) return '#ffc107';

  return '#dc3545';
}

getProgressOffset(): number {

  const score = this.matchScore() ?? 0;

  const radius = 56;
  const circumference = 2 * Math.PI * radius;

  return circumference - (score / 100) * circumference;
}
getCircumference(): number {

  return 2 * Math.PI * 56;

}

getMatchLabel(): string {

  const score = this.matchScore() ?? 0;

  if (score >= 70) return 'Strong Match';
  if (score >= 50) return 'Moderate Match';

  return 'Weak Match';
}

}

