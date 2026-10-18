import { ComponentFixture, TestBed } from '@angular/core/testing';

import { JobDescriptionUpload } from './job-description-upload';

describe('JobDescriptionUpload', () => {
  let component: JobDescriptionUpload;
  let fixture: ComponentFixture<JobDescriptionUpload>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [JobDescriptionUpload],
    }).compileComponents();

    fixture = TestBed.createComponent(JobDescriptionUpload);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
